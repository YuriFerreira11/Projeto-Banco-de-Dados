import flet as ft


def tela_selecao_torneio(lista_torneios, ao_selecionar):
    def criar_card_torneio(torneio):
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.EMOJI_EVENTS, size=40, color=ft.colors.AMBER),
                ft.Text(torneio.nome.upper(), weight="bold", size=18, text_align="center"),
                ft.Text(f"{torneio.data_inicio} até {torneio.data_fim}", size=12, color=ft.colors.WHITE54),
                ft.ElevatedButton(
                    "Entrar",
                    on_click=lambda _: ao_selecionar(torneio),
                    style=ft.ButtonStyle(color=ft.colors.WHITE, bgcolor=ft.colors.AMBER_900)
                )
            ], horizontal_alignment="center", spacing=10),
            bgcolor="#1E1E1E",
            padding=30,
            border_radius=15,
            border=ft.border.all(1, ft.colors.WHITE10),
            width=250
        )

    return ft.Column([
        ft.Container(height=80),  # Espaço superior para não colar no header
        # Título Principal
        ft.Text("BEM-VINDO AO TORNEIO MANAGER", size=40, weight="w900", text_align="center"),
        # Subtítulo (Instrução atualizada)
        ft.Text("Selecione o torneio que quer visualizar", size=18, color=ft.colors.WHITE70, italic=True),

        ft.Container(height=40),  # Espaçador entre texto e cards

        # Grid de Torneios
        ft.Row(
            [criar_card_torneio(t) for t in lista_torneios],
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
            spacing=20
        )
    ], horizontal_alignment="center", scroll=ft.ScrollMode.ADAPTIVE, expand=True)