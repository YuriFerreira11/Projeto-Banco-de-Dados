import flet as ft
from ui.components.time_card import criar_card_times
from ui.views.time_view import tela_detalhes_time
from ui.views.torneio_view import tela_detalhes_torneio
from ui.views.classificacao_view import tela_classificacao
from ui.views.selecao_torneio_view import tela_selecao_torneio
from ui.views.partida_view import RodadasView, AdminRodadasView
from ui.views.criar_torneio_view import tela_criar_torneio
from repository.torneio_repository import TorneioRepository
from repository.time_repository import TimeRepository
from repository.jogador_repository import JogadorRepository
class Router:
    def __init__(self, content_container, page: ft.Page):
        self.container     = content_container
        self.page          = page
        self.torneio_ativo = None
        self.botao_trocar  = None
        self._rodada_atual = 1

        self.routes = {
            "selecao_torneio": self.show_selecao,
            "classificacao":   self.show_classificacao,
            "partidas":        self.show_partidas,
            "times":           self.show_times,
        }

    def _configurar_navbar(self):
        self.page.navigation_bar = ft.NavigationBar(
            selected_index=0,
            destinations=[
                ft.NavigationDestination(icon=ft.icons.EMOJI_EVENTS,  label="Classificação"),
                ft.NavigationDestination(icon=ft.icons.SPORTS_SOCCER, label="Partidas"),
                ft.NavigationDestination(icon=ft.icons.TABLE_ROWS,    label="Times"),
            ],
            on_change=lambda e: self.navigate(
                ["classificacao", "partidas", "times"][e.control.selected_index]
            )
        )
        self.page.update()

    def navigate(self, route_key):
        if route_key in ["classificacao", "partidas", "times"] and not self.torneio_ativo:
            route_key = "selecao_torneio"

        if route_key == "partidas":
            self._rodada_atual = 1

        self.container.controls.clear()

        if route_key == "selecao_torneio":
            self.page.navigation_bar = None
            self.torneio_ativo = None
            if self.botao_trocar:
                self.botao_trocar.visible = False

        if route_key in self.routes:
            view = self.routes[route_key]()
            self.container.controls.append(view)

        if self.page.navigation_bar and route_key in ["classificacao", "partidas", "times"]:
            indices = {"classificacao": 0, "partidas": 1, "times": 2}
            self.page.navigation_bar.selected_index = indices.get(route_key, 0)

        self.page.update()

    def navigate_rodadas(self, id_torneio: int, rodada: int):
        self._rodada_atual = rodada
        self.container.controls.clear()
        self.container.controls.append(
            RodadasView(self, self.page, id_torneio=id_torneio, rodada=rodada).build()
        )
        if self.page.navigation_bar:
            self.page.navigation_bar.selected_index = 1
        self.page.update()

    def navigate_admin_rodadas(self, id_torneio: int, rodada: int):
        self._rodada_atual = rodada
        self.container.controls.clear()
        self.container.controls.append(
            AdminRodadasView(self, self.page, id_torneio=id_torneio, rodada=rodada).build()
        )
        self.page.update()

    def show_admin_rodadas(self):
        if not self.torneio_ativo: return
        self.container.controls.clear()
        self.container.controls.append(
            AdminRodadasView(self, self.page,
                             id_torneio=self.torneio_ativo.id_torneio, rodada=1).build()
        )
        self.page.update()

    # --- Rotas principais ---
    def show_selecao(self):
        return tela_selecao_torneio(
            TorneioRepository.get_torneios(),
            self.definir_torneio,
            ao_criar=self.show_criar_torneio
        )

    def show_criar_torneio(self):
        self.container.controls.clear()
        self.container.controls.append(
            tela_criar_torneio(ao_concluir=lambda: self.navigate("selecao_torneio"))
        )
        self.page.update()

    def definir_torneio(self, torneio_obj):
        self.torneio_ativo = torneio_obj
        self._rodada_atual = 1
        if self.botao_trocar:
            self.botao_trocar.visible = True
        self._configurar_navbar()
        self.navigate("classificacao")

    def show_classificacao(self):
        dados = TorneioRepository.get_classificacao_completa(self.torneio_ativo.id_torneio)
        return tela_classificacao(
            dados_classificacao=dados,
            ao_clicar_torneio=lambda: self.show_torneio_view(self.torneio_ativo)
        )

    def show_partidas(self):
        return RodadasView(
            self, self.page,
            id_torneio=self.torneio_ativo.id_torneio,
            rodada=self._rodada_atual
        ).build()

    def show_times(self):
        return criar_card_times(
            TimeRepository.get_times_por_torneio(self.torneio_ativo.id_torneio),
            ao_clicar_no_time=self.show_time_view
        )

    def show_time_view(self, time_obj):
        self.container.controls.clear()
        jogadores = JogadorRepository.get_jogadores_por_time(time_obj.id_time)
        stats     = TimeRepository.get_detalhes_temporada(time_obj.nome)
        self.container.controls.append(
            tela_detalhes_time(time_obj, stats, jogadores, lambda: self.navigate("times"))
        )
        self.page.update()

    def show_torneio_view(self, torneio_obj):
        self.container.controls.clear()
        self.container.controls.append(
            tela_detalhes_torneio(torneio_obj, lambda: self.navigate("classificacao"))
        )
        self.page.update()
