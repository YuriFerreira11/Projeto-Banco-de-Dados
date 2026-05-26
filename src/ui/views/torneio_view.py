import flet as ft


def tela_detalhes_torneio(torneio_obj, ao_voltar):
    return ft.Column([
        ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: ao_voltar()),
            ft.Text("DETALHES DO CAMPEONATO", size=24, weight="bold")
        ]),

        ft.Divider(height=20, color=ft.colors.WHITE10),

        # CARD PRINCIPAL DO TORNEIO
        ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.EMOJI_EVENTS, size=80, color=ft.colors.AMBER),
                ft.Text(torneio_obj.nome.upper(), size=40, weight="w900"),
                ft.Container(
                    content=ft.Text("EM ANDAMENTO", color=ft.colors.BLACK, weight="bold"),
                    bgcolor=ft.colors.GREEN_ACCENT,
                    padding=ft.padding.symmetric(horizontal=15, vertical=5),
                    border_radius=20
                ),
                ft.Container(height=20),
                ft.Row([
                    ft.Column([
                        ft.Text("DATA DE INÍCIO", size=12, color=ft.colors.WHITE54),
                        ft.Text(f"{torneio_obj.data_inicio}", size=18, weight="bold"),
                    ], horizontal_alignment="center"),
                    ft.VerticalDivider(width=40, color=ft.colors.WHITE10),
                    ft.Column([
                        ft.Text("DATA DE TÉRMINO", size=12, color=ft.colors.WHITE54),
                        ft.Text(f"{torneio_obj.data_fim}", size=18, weight="bold"),
                    ], horizontal_alignment="center"),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ], horizontal_alignment="center"),
            bgcolor="#1E1E1E",
            padding=50,
            border_radius=25,
            border=ft.border.all(1, ft.colors.WHITE10),
            alignment=ft.alignment.center
        ),

        ft.Container(height=30),

        # NOTA DE RODAPÉ
        ft.Text(
            "Os dados de classificação são atualizados automaticamente após o término de cada partida.",
            italic=True,
            color=ft.colors.WHITE38,
            text_align=ft.TextAlign.CENTER
        )
    ], scroll=ft.ScrollMode.ADAPTIVE, horizontal_alignment=ft.CrossAxisAlignment.CENTER)