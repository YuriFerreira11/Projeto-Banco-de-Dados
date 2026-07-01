import flet as ft
from src.repository.torneio_repository import TorneioRepository
from src.ui.router import Router
from src.services.partidas_logic import PartidasLogic

ADMIN_SENHA = TorneioRepository.obter_senha_admin()


def main(page: ft.Page):
    page.title = "Súmula Digital - Torneio Manager"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 850
    page.window_center()

    main_content = ft.Column(
        expand=True,
        scroll=None,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH
    )

    router = Router(main_content, page)
    acao_pendente = {"valor": "gerar"}

    senha_field = ft.TextField(
        label="Senha do Admin", password=True, can_reveal_password=True,
        autofocus=True, width=300, border_color=ft.colors.AMBER,
    )
    erro_senha = ft.Text("", color=ft.colors.RED_400, size=12)
    dialog_desc = ft.Text("", color=ft.colors.WHITE70, size=13)

    def confirmar_admin(e):
        if senha_field.value == ADMIN_SENHA:
            admin_dialog.open = False
            page.update()
            if acao_pendente["valor"] == "gerar":
                _executar_geracao_tabela()
            elif acao_pendente["valor"] == "toggle_admin":
                router.modo_admin = True
                atualizar_visual_botao_admin()
                router.refresh_current_view()
        else:
            erro_senha.value = "Senha incorreta."
            senha_field.value = ""
            page.update()

    def fechar_dialog(e):
        admin_dialog.open = False
        senha_field.value = ""
        erro_senha.value = ""
        page.update()

    admin_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([ft.Icon(ft.icons.LOCK, color=ft.colors.AMBER), ft.Text("Acesso Restrito", weight="bold")]),
        content=ft.Column([dialog_desc, ft.Container(height=8), senha_field, erro_senha], tight=True, spacing=4),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_dialog, style=ft.ButtonStyle(color=ft.colors.WHITE54)),
            ft.ElevatedButton("Confirmar", icon=ft.icons.CHECK, bgcolor=ft.colors.AMBER, color=ft.colors.BLACK,
                              on_click=confirmar_admin),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(admin_dialog)

    def _abrir_dialog(acao: str, descricao: str):
        if not router.torneio_ativo:
            page.show_snack_bar(ft.SnackBar(ft.Text("Selecione um torneio primeiro!")))
            return
        acao_pendente["valor"] = acao
        dialog_desc.value = descricao
        senha_field.value = ""
        erro_senha.value = ""
        admin_dialog.open = True
        page.update()

    def _executar_geracao_tabela():
        try:
            total = PartidasLogic.gerar_e_salvar(router.torneio_ativo.id_torneio)
            page.show_snack_bar(
                ft.SnackBar(ft.Text(f"{total} jogos criados com sucesso!"), bgcolor=ft.colors.GREEN_700))
            router.navigate("partidas")
        except Exception as ex:
            page.show_snack_bar(ft.SnackBar(ft.Text(f"Erro: {str(ex)}"), bgcolor=ft.colors.RED_700))

    def tratar_click_admin(e):
        if router.modo_admin:
            router.modo_admin = False
            atualizar_visual_botao_admin()
            router.refresh_current_view()
        else:
            _abrir_dialog("toggle_admin", "Digite a credencial master para ativar o Modo Admin do sistema.")

    def atualizar_visual_botao_admin():
        if router.modo_admin:
            btn_modo_admin.content.controls[0].value = "MODO ADMIN: ATIVO"
            btn_modo_admin.content.controls[0].color = ft.colors.AMBER
            btn_modo_admin.content.controls[1].name = ft.icons.LOCK_OPEN_ROUNDED
            btn_modo_admin.content.controls[1].color = ft.colors.AMBER

            btn_admin_container.content.controls[0].visible = True
            btn_admin_container.content.controls[1].visible = True
        else:
            btn_modo_admin.content.controls[0].value = "MODO ADMIN"
            btn_modo_admin.content.controls[0].color = ft.colors.WHITE70
            btn_modo_admin.content.controls[1].name = ft.icons.LOCK_ROUNDED
            btn_modo_admin.content.controls[1].color = ft.colors.WHITE70

            btn_admin_container.content.controls[0].visible = False
            btn_admin_container.content.controls[1].visible = False

        btn_modo_admin.update()
        btn_admin_container.update()

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

    btn_modo_admin = ft.TextButton(
        content=ft.Row([
            ft.Text("MODO ADMIN", color=ft.colors.WHITE70, size=11, weight="bold"),
            ft.Icon(ft.icons.LOCK_ROUNDED, size=14, color=ft.colors.WHITE70),
        ], tight=True),
        on_click=tratar_click_admin,
    )

    btn_admin_container = ft.Container(
        content=ft.Row([
            ft.TextButton(
                content=ft.Row([
                    ft.Text("GERAR TABELA", color=ft.colors.WHITE70, size=11, weight="bold"),
                    ft.Icon(ft.icons.AUTO_AWESOME, size=14, color=ft.colors.WHITE70),
                ], tight=True),
                on_click=lambda _: _abrir_dialog("gerar", "Digite a senha para gerar a tabela de jogos do torneio."),
                visible=False
            ),
            ft.Text("|", color=ft.colors.WHITE24, visible=False),
            btn_modo_admin,
        ], tight=True),
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
                expand=2, alignment=ft.alignment.center
            ),
            ft.Container(content=btn_admin_container, expand=2, alignment=ft.alignment.center_right)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=25, vertical=15),
        bgcolor=ft.colors.BLACK54,
        border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.WHITE10))
    )

    page.add(
        header,
        ft.Container(content=main_content, expand=True, padding=20)
    )

    atualizar_visual_botao_admin()
    router.navigate("selecao_torneio")


if __name__ == "__main__":
    ft.app(target=main)