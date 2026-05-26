import flet as ft


def tela_detalhes_partida(partida_obj, time_m, time_v, ao_voltar):
    # Fallback para caso os objetos de time não sejam encontrados
    nome_m = time_m.nome if time_m else "Mandante"
    escudo_m = time_m.escudo if time_m else ""
    nome_v = time_v.nome if time_v else "Visitante"
    escudo_v = time_v.escudo if time_v else ""

    return ft.Column([
        # Cabeçalho
        ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: ao_voltar()),
            ft.Text("DETALHES DA PARTIDA", size=24, weight="bold")
        ]),

        ft.Divider(height=30, color=ft.colors.WHITE10),

        # PLACAR ESTILO TRANSMISSÃO
        ft.Container(
            content=ft.Row([
                # Mandante
                ft.Column([
                    ft.Image(src=escudo_m, width=100, height=100, fit=ft.ImageFit.CONTAIN),
                    ft.Text(nome_m.upper(), size=20, weight="bold"),
                    ft.Text("MANDANTE", size=12, color=ft.colors.WHITE54)
                ], horizontal_alignment="center", expand=True),

                # Placar Central
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"{partida_obj.gols_m}", size=60, weight="w900"),
                        ft.Text("X", size=24, color=ft.colors.GREEN_ACCENT, weight="bold"),
                        ft.Text(f"{partida_obj.gols_v}", size=60, weight="w900"),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
                    bgcolor=ft.colors.BLACK38,
                    padding=ft.padding.symmetric(horizontal=30, vertical=10),
                    border_radius=15
                ),

                # Visitante
                ft.Column([
                    ft.Image(src=escudo_v, width=100, height=100, fit=ft.ImageFit.CONTAIN),
                    ft.Text(nome_v.upper(), size=20, weight="bold"),
                    ft.Text("VISITANTE", size=12, color=ft.colors.WHITE54)
                ], horizontal_alignment="center", expand=True),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=40,
            bgcolor="#1E1E1E",
            border_radius=20,
            border=ft.border.all(1, ft.colors.WHITE10)
        ),

        ft.Container(height=20),

        # INFORMAÇÕES DA PARTIDA (DATA E LOCAL)
        ft.ResponsiveRow([
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.icons.EVENT_AVAILABLE, color=ft.colors.GREEN_ACCENT),
                        ft.Text(f"DATA E HORA: {partida_obj.data_hora}", size=16)
                    ]),
                    ft.Row([
                        ft.Icon(ft.icons.LOCATION_ON, color=ft.colors.RED_ACCENT),
                        ft.Text(f"LOCAL: {partida_obj.local}", size=16)
                    ]),
                ], spacing=15),
                col={"md": 12},
                bgcolor="#2C2C2C",
                padding=25,
                border_radius=15
            )
        ])
    ], scroll=ft.ScrollMode.ADAPTIVE, expand=True)