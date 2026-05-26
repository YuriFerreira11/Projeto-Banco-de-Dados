import flet as ft
from src.ui.components.classificacao_tabela import criar_tabela_classificacao
from src.ui.components.time_card import criar_card_times
from src.ui.views.time_view import tela_detalhes_time
from src.ui.views.torneio_view import tela_detalhes_torneio
from src.ui.views.classificacao_view import tela_classificacao
from src.ui.views.selecao_torneio_view import tela_selecao_torneio
from src.database.db_queries import DBQueries
from src.ui.components.partidas_card import criar_card_partidas


class Router:
    def __init__(self, content_container, page: ft.Page):
        self.container = content_container
        self.page = page
        self.torneio_ativo = None
        self.botao_trocar = None

        self.routes = {
            "selecao_torneio": self.show_selecao,
            "classificacao": self.show_classificacao,  # Nova Ordem
            "partidas": self.show_partidas,
            "times": self.show_times
        }

    def _configurar_navbar(self):
        # Invertendo a ordem dos ícones e labels
        self.page.navigation_bar = ft.NavigationBar(
            selected_index=0,  # Começa na Classificação agora
            destinations=[
                ft.NavigationDestination(icon=ft.icons.EMOJI_EVENTS, label="Classificação"),
                ft.NavigationDestination(icon=ft.icons.SPORTS_SOCCER, label="Partidas"),
                ft.NavigationDestination(icon=ft.icons.TABLE_ROWS, label="Times"),
            ],
            on_change=lambda e: self.navigate(
                ["classificacao", "partidas", "times"][e.control.selected_index]
            )
        )
        self.page.update()

    def navigate(self, route_key):
        self.container.controls.clear()

        if route_key in self.routes:
            if route_key == "selecao_torneio":
                self.page.navigation_bar = None
                self.torneio_ativo = None
                if self.botao_trocar: self.botao_trocar.visible = False

            view = self.routes[route_key]()
            self.container.controls.append(view)

        self.page.update()

    def show_selecao(self):
        torneios = DBQueries.get_torneios()
        return tela_selecao_torneio(torneios, self.definir_torneio)

    def definir_torneio(self, torneio_obj):
        self.torneio_ativo = torneio_obj
        if self.botao_trocar: self.botao_trocar.visible = True
        self._configurar_navbar()
        self.navigate("classificacao")  # Agora entra direto na Classificação

    def show_times(self):
        return criar_card_times(
            DBQueries.get_times_por_torneio(self.torneio_ativo.id_torneio),
            ao_clicar_no_time=self.show_time_view
        )

    def show_partidas(self):
        return criar_tabela_classificacao(
            DBQueries.get_partidas(self.torneio_ativo.id_torneio)
        )

    def show_classificacao(self):
        dados = DBQueries.get_classificacao_completa(self.torneio_ativo.id_torneio)
        return tela_classificacao(
            dados_classificacao=dados,
            ao_clicar_torneio=lambda: self.show_torneio_view(self.torneio_ativo)
        )

    # --- Sub-views de Detalhes ---
    def show_time_view(self, time_obj):
        self.container.controls.clear()
        jogadores = DBQueries.get_jogadores_por_time(time_obj.id_time)
        stats = DBQueries.get_detalhes_temporada(time_obj.nome)
        view = tela_detalhes_time(time_obj, stats, jogadores, lambda: self.navigate("times"))
        self.container.controls.append(view)
        self.page.update()

    def show_partidas(self):
        dados_partidas = DBQueries.get_partidas(self.torneio_ativo.id_torneio)

        # Título da seção
        titulo = ft.Column([
            ft.Text("PRÓXIMOS CONFRONTOS", size=28, weight="w900", text_align="center"),
            ft.Text("Resultados atualizados em tempo real", size=14, color=ft.colors.WHITE54, text_align="center"),
            ft.Container(height=20),
        ], horizontal_alignment="center")

        return ft.Column([
            titulo,
            criar_card_partidas(dados_partidas)
        ], scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment="center", expand=True)

    def show_torneio_view(self, torneio_obj):
        self.container.controls.clear()
        view = tela_detalhes_torneio(torneio_obj, lambda: self.navigate("classificacao"))
        self.container.controls.append(view)
        self.page.update()