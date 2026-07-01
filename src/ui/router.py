import flet as ft

from src.repository.torneio_repository import TorneioRepository
from src.repository.time_repository import TimeRepository
from src.repository.jogador_repository import JogadorRepository

from src.ui.views.selecao_torneio_view import tela_selecao_torneio
from src.ui.views.criar_torneio_view import tela_criar_torneio
from src.ui.views.time_view import time_view
from src.ui.views.torneio_view import tela_detalhes_torneio
from src.ui.views.classificacao_view import tela_classificacao
from src.ui.views.partida_view import RodadasView

FUNCOES_JOGADOR = ["Goleiro", "Zagueiro", "Lateral", "Volante", "Meia", "Atacante"]

# Rotas que só fazem sentido com um torneio selecionado.
# Se o usuário cair aqui sem torneio_ativo, o router redireciona pra seleção.
ROTAS_REQUEREM_TORNEIO = {"times", "time_detalhe", "partidas", "classificacao", "torneio"}


class Router:
    def __init__(self, main_content, page: ft.Page):
        self.main_content = main_content
        self.page = page

        self.modo_admin = False
        self.torneio_ativo = None
        self.time_ativo = None
        self.rodada_atual = 1

        self.botao_trocar = None
        self.current_route = None

        self.btn_gerar_partidas = None

        self._rotas = {
            "selecao_torneio": self.view_selecao_torneio,
            "criar_torneio": self.view_criar_torneio,
            "times": self.view_times,
            "time_detalhe": self.view_time_detalhe,
            "partidas": self.view_partidas,
            "classificacao": self.view_classificacao,
            "torneio": self.view_torneio,
        }

    # ------------------------------------------------------------------ #
    # Núcleo de navegação
    # ------------------------------------------------------------------ #
    def navigate(self, rota: str, **kwargs):
        """Troca o conteúdo principal pela view correspondente à rota."""
        if rota in ROTAS_REQUEREM_TORNEIO and self.torneio_ativo is None:
            rota = "selecao_torneio"

        self.current_route = rota

        if self.botao_trocar is not None:
            self.botao_trocar.visible = (rota != "selecao_torneio")

        builder = self._rotas.get(rota)
        if builder is None:
            self.main_content.controls = [
                ft.Text(f"Rota '{rota}' não encontrada.", color=ft.colors.RED_400)
            ]
        else:
            self.main_content.controls = [builder(**kwargs)]

        self.main_content.update()
        self.page.update()

    def navigate_rodadas(self, id_torneio, rodada):
        """Usado pelo RodadasView para trocar de rodada sem perder o torneio ativo."""
        self.rodada_atual = max(1, rodada)
        self.navigate("partidas")

    def refresh_current_view(self):
        """Re-renderiza a rota atual (usado ao alternar modo_admin, salvar placar etc.)."""
        if self.current_route:
            self.navigate(self.current_route)

    # ------------------------------------------------------------------ #
    # Sub-navegação (Times / Partidas / Classificação / Info do torneio)
    # ------------------------------------------------------------------ #
    def _com_subnav(self, conteudo):
        def botao(rota, label, icon):
            ativo = self.current_route == rota
            return ft.TextButton(
                content=ft.Row(
                    [
                        ft.Icon(icon, size=16, color=ft.colors.AMBER if ativo else ft.colors.WHITE54),
                        ft.Text(
                            label,
                            color=ft.colors.AMBER if ativo else ft.colors.WHITE54,
                            weight="bold" if ativo else "normal",
                            size=13,
                        ),
                    ],
                    tight=True,
                    spacing=6,
                ),
                on_click=lambda _, r=rota: self.navigate(r),
            )

        subnav = ft.Row(
            [
                botao("classificacao", "CLASSIFICAÇÃO", ft.icons.LEADERBOARD),
                botao("partidas", "PARTIDAS", ft.icons.SPORTS_SOCCER),
                botao("times", "TIMES", ft.icons.SHIELD_ROUNDED),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

        return ft.Column(
            [subnav, ft.Divider(color=ft.colors.WHITE10), conteudo],
            expand=True,
            spacing=10,
        )

    # ------------------------------------------------------------------ #
    # Seleção / criação de torneio
    # ------------------------------------------------------------------ #
    def view_selecao_torneio(self):
        torneios = TorneioRepository.get_torneios()
        return tela_selecao_torneio(torneios, self.selecionar_torneio, self.ir_criar_torneio)

    def selecionar_torneio(self, torneio):
        self.torneio_ativo = torneio
        self.time_ativo = None
        self.rodada_atual = 1
        self.navigate("classificacao")

    def ir_criar_torneio(self):
        self.navigate("criar_torneio")

    def view_criar_torneio(self):
        return tela_criar_torneio(self._concluir_criacao, lambda: self.navigate("selecao_torneio"))

    def _concluir_criacao(self):
        self.navigate("selecao_torneio")

    # ------------------------------------------------------------------ #
    # Times
    # ------------------------------------------------------------------ #
    def view_times(self):
        times = TimeRepository.get_times_por_torneio(self.torneio_ativo.id_torneio)
        conteudo = time_view(self.page, self._abrir_time, times)
        return self._com_subnav(conteudo)

    def _abrir_time(self, time):
        self.time_ativo = time
        self.navigate("time_detalhe")

    def view_time_detalhe(self):
        time = self.time_ativo
        if time is None:
            self.navigate("times")
            return ft.Container()

        jogadores = JogadorRepository.get_jogadores_por_time(time.id_time)
        temporada = TimeRepository.get_detalhes_temporada(time.nome)

        lista = ft.ListView(expand=True, spacing=8)
        if not jogadores:
            lista.controls.append(
                ft.Text(
                    "Nenhum jogador relacionado a este elenco até o momento.",
                    italic=True,
                    color=ft.colors.WHITE54,
                )
            )

        for jog in jogadores:
            acoes = []
            if self.modo_admin:
                acoes = [
                    ft.IconButton(
                        icon=ft.icons.EDIT_ROUNDED,
                        icon_size=18,
                        icon_color=ft.colors.AMBER,
                        tooltip="Editar jogador",
                        on_click=lambda _, j=jog: self._abrir_dialog_jogador(j),
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINE,
                        icon_size=18,
                        icon_color=ft.colors.RED_400,
                        tooltip="Remover jogador",
                        on_click=lambda _, j=jog: self._confirmar_remover_jogador(j),
                    ),
                ]

            lista.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.icons.PERSON, color=ft.colors.WHITE54),
                            ft.Column(
                                [
                                    ft.Text(jog.nome, weight="bold"),
                                    ft.Text(
                                        jog.funcao or "Posição não informada",
                                        size=12,
                                        color=ft.colors.WHITE54,
                                    ),
                                ],
                                spacing=0,
                                expand=True,
                            ),
                            *acoes,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    bgcolor=ft.colors.WHITE10,
                    border_radius=8,
                )
            )

        acoes_header = []
        if self.modo_admin:
            acoes_header.append(
                ft.ElevatedButton(
                    "Adicionar Jogador",
                    icon=ft.icons.PERSON_ADD_ALT_1,
                    bgcolor=ft.colors.AMBER,
                    color=ft.colors.BLACK,
                    on_click=lambda _: self._abrir_dialog_jogador(None),
                )
            )

        posicao = getattr(temporada, "posicao", "-")
        if posicao not in (None, "-", 0):
            badge_colocacao = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.EMOJI_EVENTS, size=16, color=ft.colors.AMBER),
                        ft.Text(f"{posicao}º colocado", size=12, weight="bold", color=ft.colors.AMBER),
                        ft.Text(f"·  {getattr(temporada, 'pontos', 0)} pts", size=12, color=ft.colors.WHITE54),
                    ],
                    spacing=6,
                    tight=True,
                ),
                bgcolor=ft.colors.WHITE10,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
            )
        else:
            badge_colocacao = ft.Container(
                content=ft.Text("Sem partidas disputadas no torneio", size=12, color=ft.colors.WHITE38),
                bgcolor=ft.colors.WHITE10,
                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                border_radius=20,
            )

        cabecalho = ft.Row(
            [
                ft.Row(
                    [
                        ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: self.navigate("times")),

                        # Bloco corrigido para carregar a imagem ou o ícone padrão
                        ft.Image(
                            src=time.escudo if getattr(time, "escudo", None) else None,
                            width=32,
                            height=32,
                            fit=ft.ImageFit.CONTAIN,
                        ) if getattr(time, "escudo", None) else ft.Icon(
                            ft.icons.SHIELD_ROUNDED, size=32, color=ft.colors.PRIMARY
                        ),

                        ft.Text(getattr(time, "nome", "Time"), size=24, weight="bold"),
                        badge_colocacao,
                    ],
                    spacing=10,
                ),
                ft.Row(acoes_header),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        return ft.Column(
            [
                cabecalho,
                ft.Divider(color=ft.colors.WHITE10),
                ft.Text("Jogadores Cadastrados", size=18, weight="bold"),
                lista,
            ],
            expand=True,
            spacing=10,
        )

    # ---- dialogs de edição de elenco (só chamados em modo_admin) ----
    def _abrir_dialog_jogador(self, jogador):
        eh_edicao = jogador is not None

        campo_nome = ft.TextField(
            label="Nome do Jogador",
            value=jogador.nome if eh_edicao else "",
            width=280,
            border_color=ft.colors.AMBER,
            autofocus=True,
        )
        campo_funcao = ft.Dropdown(
            label="Função",
            value=(jogador.funcao if (eh_edicao and jogador.funcao) else "Meia"),
            width=280,
            border_color=ft.colors.WHITE24,
            options=[ft.dropdown.Option(f) for f in FUNCOES_JOGADOR],
        )
        erro = ft.Text("", color=ft.colors.RED_400, size=12)

        def salvar(e):
            nome = campo_nome.value.strip()
            if not nome:
                erro.value = "⚠️ Informe o nome do jogador."
                erro.update()
                return
            try:
                if eh_edicao:
                    JogadorRepository.atualizar_jogador(jogador.id_jogador, nome, campo_funcao.value)
                else:
                    JogadorRepository.criar_jogador(nome, campo_funcao.value, self.time_ativo.id_time)
                dialog.open = False
                self.page.update()
                self.refresh_current_view()
            except Exception as ex:
                erro.value = f"❌ Erro ao salvar: {ex}"
                erro.update()

        def cancelar(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Jogador" if eh_edicao else "Adicionar Jogador", weight="bold"),
            content=ft.Column([campo_nome, campo_funcao, erro], tight=True, spacing=12),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar, style=ft.ButtonStyle(color=ft.colors.WHITE54)),
                ft.ElevatedButton("Salvar", bgcolor=ft.colors.AMBER, color=ft.colors.BLACK, on_click=salvar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        if dialog not in self.page.overlay:
            self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def _confirmar_remover_jogador(self, jogador):
        def remover(e):
            try:
                JogadorRepository.deletar_jogador(jogador.id_jogador)
                dialog.open = False
                self.page.update()
                self.refresh_current_view()
            except Exception as ex:
                self.page.show_snack_bar(
                    ft.SnackBar(ft.Text(f"Erro ao remover: {ex}"), bgcolor=ft.colors.RED_700)
                )

        def cancelar(e):
            dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Remover Jogador", weight="bold"),
            content=ft.Text(f"Remover {jogador.nome} do elenco?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar, style=ft.ButtonStyle(color=ft.colors.WHITE54)),
                ft.ElevatedButton(
                    "Remover", bgcolor=ft.colors.RED_700, color=ft.colors.WHITE, on_click=remover
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        if dialog not in self.page.overlay:
            self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    # ------------------------------------------------------------------ #
    # Partidas / Rodadas
    # ------------------------------------------------------------------ #
    def view_partidas(self):
        rv = RodadasView(
            router=self,
            page=self.page,
            id_torneio=self.torneio_ativo.id_torneio,
            rodada=self.rodada_atual,
            modo_admin=self.modo_admin,
        )
        return self._com_subnav(rv.build())

    # ------------------------------------------------------------------ #
    # Classificação
    # ------------------------------------------------------------------ #
    def view_classificacao(self):
        dados = TorneioRepository.get_classificacao_completa(self.torneio_ativo.id_torneio)
        conteudo = tela_classificacao(dados, lambda: self.navigate("torneio"))
        return self._com_subnav(conteudo)

    # ------------------------------------------------------------------ #
    # Info do torneio
    # ------------------------------------------------------------------ #
    def view_torneio(self):
        conteudo = tela_detalhes_torneio(self.torneio_ativo, lambda: self.navigate("classificacao"))
        return self._com_subnav(conteudo)
