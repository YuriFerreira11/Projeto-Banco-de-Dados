import flet as ft
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.ui.router import Router


def main(page: ft.Page):
    page.title = "Súmula Digital - Torneio Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 850
    page.window_center()

    main_content = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ADAPTIVE,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    )

    router = Router(main_content, page)

    btn_voltar = ft.Container(
        content=ft.TextButton(
            content=ft.Row([
                ft.Icon(ft.icons.ARROW_BACK_IOS_NEW, size=16, color=ft.colors.AMBER),
                ft.Text("TROCAR TORNEIO", color=ft.colors.AMBER, size=12, weight="bold"),
            ], tight=True),
            on_click=lambda _: router.navigate("selecao_torneio"),
        ),
        visible=False,
    )

    btn_admin = ft.Container(
        content=ft.TextButton(
            content=ft.Row([
                ft.Text("MODO ADMIN", color=ft.colors.WHITE70, size=12, weight="bold"),
                ft.Icon(ft.icons.LOCK_OUTLINED, size=16, color=ft.colors.WHITE70),
            ], tight=True),
            on_click=lambda _: page.open(
                ft.SnackBar(ft.Text("Módulo administrativo será habilitado em breve."))
            ),
        ),
        alignment=ft.alignment.center_right,
    )

    router.botao_trocar = btn_voltar

    header = ft.Container(
        content=ft.Row([
            ft.Container(content=btn_voltar, expand=1, alignment=ft.alignment.center_left),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.icons.EMOJI_EVENTS, color=ft.colors.AMBER, size=30),
                    ft.Text("TORNEIO MANAGER", size=24, weight="bold"),
                ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
                expand=2,
                alignment=ft.alignment.center
            ),
            ft.Container(content=btn_admin, expand=1, alignment=ft.alignment.center_right)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=25, vertical=15),
        bgcolor=ft.colors.BLACK26
    )

    page.add(
        header,
        ft.Divider(height=1, color=ft.colors.WHITE10),
        ft.Container(
            content=main_content,
            expand=True,
            padding=10
        )
    )

    router.navigate("selecao_torneio")


if __name__ == "__main__":
    ft.app(target=main)