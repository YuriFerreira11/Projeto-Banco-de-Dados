# src/ui/router.py
import flet as ft
from src.ui.components.data_table import criar_tabela_dados
from src.ui.mock_factory import MockFactory

class Router:
    def __init__(self, content_container):
        self.container = content_container
        self.routes = {
            "times": lambda: criar_tabela_dados(MockFactory.get_times()),
            "jogadores": lambda: criar_tabela_dados(MockFactory.get_jogadores()),
            "partidas": lambda: criar_tabela_dados(MockFactory.get_partidas()),
            "classificacao": lambda: ft.Text("Aqui entrará a VIEW_CLASSIFICACAO do banco", size=20)
        }

    def navigate(self, route_key):
        self.container.controls.clear()
        if route_key in self.routes:
            view = self.routes[route_key]()
            self.container.controls.append(view)
        self.container.page.update()