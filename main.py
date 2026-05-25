import flet as ft
from src.ui.router import Router


def main(page: ft.Page):
    page.title = "Súmula Digital - Torneio"
    page.theme_mode = ft.ThemeMode.DARK

    page.window_width = 1100
    page.window_height = 800
    page.window_center()

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    main_content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    router = Router(main_content)

    # Na versão 0.21.2 o nome é NavigationDestination (sem o 'Bar' no meio)
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationDestination(icon=ft.icons.TABLE_ROWS, label="Times"),
            ft.NavigationDestination(icon=ft.icons.GROUPS, label="Jogadores"),
            ft.NavigationDestination(icon=ft.icons.SPORTS_SOCCER, label="Partidas"),
            ft.NavigationDestination(icon=ft.icons.EMOJI_EVENTS, label="Classificação"),
        ],
        on_change=lambda e: router.navigate(
            ["times", "jogadores", "partidas", "classificacao"][int(e.data)]
        )
    )

    page.add(
        ft.Container(
            content=ft.Row(
                [
                    ft.Text("🏆 Torneio Manager", size=32, weight="bold"),
                    ft.VerticalDivider(width=20),
                    ft.Text("Preview Mode (Mock)", color=ft.colors.AMBER, weight="bold")
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=20
        ),
        ft.Divider(),
        ft.Container(content=main_content, expand=True, alignment=ft.alignment.center)
    )

    router.navigate("times")


if __name__ == "__main__":
    ft.app(target=main)