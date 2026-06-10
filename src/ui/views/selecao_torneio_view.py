import flet as ft


def tela_selecao_torneio(lista_torneios, ao_selecionar, ao_criar=None):
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

    criar_btn = ft.ElevatedButton(
        "＋  Criar Novo Torneio",
        icon=ft.icons.ADD_CIRCLE_OUTLINE,
        bgcolor=ft.colors.AMBER,
        color=ft.colors.BLACK,
        on_click=lambda _: ao_criar(),
    ) if ao_criar else ft.Container()

    sem_torneios = ft.Text(
        "Nenhum torneio cadastrado. Crie o primeiro!",
        size=16, color=ft.colors.WHITE54, italic=True
    ) if not lista_torneios else ft.Container()

    return ft.Column([
        ft.Container(height=80),
        ft.Text("BEM-VINDO AO TORNEIO MANAGER", size=40, weight="w900", text_align="center"),
        ft.Text("Selecione o torneio que quer visualizar", size=18, color=ft.colors.WHITE70, italic=True),
        ft.Container(height=20),
        criar_btn,
        sem_torneios,
        ft.Container(height=20),
        ft.Row(
            [criar_card_torneio(t) for t in lista_torneios],
            alignment=ft.MainAxisAlignment.CENTER,
            wrap=True,
            spacing=20
        )
    ], horizontal_alignment="center", scroll=ft.ScrollMode.ADAPTIVE, expand=True)
