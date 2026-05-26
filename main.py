import flet as ft
import sys
import os

# FORÇA O PYTHON A ACHAR A PASTA SRC
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.ui.router import Router

def main(page: ft.Page):
    page.title = "Súmula Digital - Torneio"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1100
    page.window_height = 800
    page.window_center()

    # Container onde o conteúdo das abas será injetado
    main_content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Inicializa o Router passando o container
    router = Router(main_content)

    # --- Barra de Navegação ---
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.TABLE_ROWS, label="Times"),
            ft.NavigationDestination(icon=ft.icons.GROUPS, label="Jogadores"),
            ft.NavigationDestination(icon=ft.icons.SPORTS_SOCCER, label="Partidas"),
            ft.NavigationDestination(icon=ft.icons.EMOJI_EVENTS, label="Classificação"),
        ],
        on_change=lambda e: router.navigate(
            ["times", "jogadores", "partidas", "classificacao"][e.control.selected_index]
        )
    )

    # --- Estrutura Fixa (Header + Conteúdo) ---
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Text("🏆 Torneio Manager", size=32, weight="bold"),
                    ft.VerticalDivider(width=20),
                    ft.Text("Banco de Dados Ativo", color=ft.colors.GREEN_ACCENT, weight="bold")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=20
        ),
        ft.Divider(height=1, color=ft.colors.OUTLINE_VARIANT),
        ft.Container(content=main_content, expand=True, padding=20)
    )

    # Carrega a tela inicial
    router.navigate("times")

if __name__ == "__main__":
    ft.app(target=main)