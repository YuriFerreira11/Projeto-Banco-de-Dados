import flet as ft
from src.repository.torneio_repository import TorneioRepository


def tela_selecao_torneio(lista_torneios, ao_selecionar, ao_criar=None, modo_admin=False, router=None):
    def confirmar_remover_torneio(torneio):
        def remover(e):
            try:
                TorneioRepository.deletar_torneio(torneio.id_torneio)
                dialog.open = False
                router.page.update()
                router.refresh_current_view()
            except Exception as ex:
                router.page.show_snack_bar(
                    ft.SnackBar(ft.Text(f"Erro ao remover: {ex}"), bgcolor=ft.colors.RED_700)
                )

        def cancelar(e):
            dialog.open = False
            router.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Remover Torneio", weight="bold"),
            content=ft.Text(f"Tem certeza que deseja apagar o torneio '{torneio.nome}'?\nEsta ação não pode ser desfeita e apagará todos os dados vinculados."),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar, style=ft.ButtonStyle(color=ft.colors.WHITE54)),
                ft.ElevatedButton(
                    "Remover", bgcolor=ft.colors.RED_700, color=ft.colors.WHITE, on_click=remover
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        if dialog not in router.page.overlay:
            router.page.overlay.append(dialog)
        dialog.open = True
        router.page.update()

    def criar_card_torneio(torneio):
        conteudo_card = ft.Container(
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
            width=250,
            height=240
        )

        if modo_admin and router:
            btn_deletar = ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.EDIT_ROUNDED,
                    icon_size=18,
                    icon_color=ft.colors.AMBER,
                    tooltip="Excluir/Editar Torneio",
                    on_click=lambda _: confirmar_remover_torneio(torneio)
                ),
                top=5,
                right=5
            )
            return ft.Stack([conteudo_card, btn_deletar], width=250, height=240)

        return conteudo_card

    criar_btn = ft.ElevatedButton(
        "＋  Criar Novo Torneio",
        icon=ft.icons.ADD_CIRCLE_OUTLINE,
        bgcolor=ft.colors.AMBER,
        color=ft.colors.BLACK,
        on_click=lambda _: ao_criar(),
    ) if (ao_criar and modo_admin) else ft.Container()

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