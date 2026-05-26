import flet as ft
from src.ui.components.data_table import criar_tabela_dados
from src.ui.components.data_grid import criar_grid_times
from src.ui.views.time_detail import tela_detalhes_time
from src.database.db_queries import DBQueries  # Troca Mock por DBQueries


class Router:
    def __init__(self, content_container):
        self.container = content_container
        self.routes = {
            "times": self.show_times,
            "jogadores": lambda: criar_tabela_dados(DBQueries.get_jogadores()),
            "partidas": lambda: ft.Text("Aqui você pode criar criar_tabela_dados(DBQueries.get_partidas())", size=20),
            "classificacao": lambda: criar_tabela_dados(DBQueries.get_classificacao_completa())
        }

    def navigate(self, route_key):
        self.container.controls.clear()
        if route_key in self.routes:
            view = self.routes[route_key]()
            self.container.controls.append(view)
        self.container.page.update()

    def show_times(self):
        return criar_grid_times(
            DBQueries.get_times(),
            ao_clicar_no_time=self.show_time_details
        )

    def show_time_details(self, time_obj):
        self.container.controls.clear()

        # BUSCA REAL NO BANCO POR TIME
        jogadores = DBQueries.get_jogadores_por_time(time_obj.id_time)
        stats = DBQueries.get_detalhes_temporada(time_obj.nome)

        view = tela_detalhes_time(
            time_obj=time_obj,
            dados_classificacao=stats,
            jogadores=jogadores,
            ao_voltar=lambda: self.navigate("times")
        )

        self.container.controls.append(view)
        self.container.page.update()