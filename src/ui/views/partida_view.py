import flet as ft
from src.repository.partidas_repository import PartidaRepository as partidas_repo


class RodadasView:
    def __init__(self, router, page: ft.Page, id_torneio: int = None, rodada: int = 1, modo_admin: bool = False,
                 **kwargs):
        self.router = router
        self.page = page
        self.id_torneio = id_torneio
        self.rodada = rodada
        self.modo_admin = modo_admin

    def abrir_editar_placar(self, e, partida):
        gm = partida.get("gols_m")
        gv = partida.get("gols_v")

        campo_casa = ft.TextField(
            label=partida["casa"], value="" if gm is None else str(gm),
            width=80, text_align=ft.TextAlign.CENTER, border_color=ft.colors.AMBER,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        campo_fora = ft.TextField(
            label=partida["fora"], value="" if gv is None else str(gv),
            width=80, text_align=ft.TextAlign.CENTER, border_color=ft.colors.AMBER,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        erro_txt = ft.Text("", color=ft.colors.RED_400, size=12)

        def salvar_placar(evt):
            try:
                gc = int(campo_casa.value)
                gf = int(campo_fora.value)
            except ValueError:
                erro_txt.value = "⚠️ Digite números válidos."
                erro_txt.update()
                return

            if partidas_repo.registrar_resultado(partida["id_partida"], gc, gf):
                edit_dialog.open = False
                self.page.update()
                self.router.refresh_current_view()
            else:
                erro_txt.value = "Erro ao salvar resultado no banco."
                erro_txt.update()

        edit_dialog = ft.AlertDialog(
            title=ft.Text("Lançar Resultado", weight="bold", size=16),
            content=ft.Container(
                width=240, # Força a largura do modal para não espremer o conteúdo
                content=ft.Column([
                    ft.Row(
                        [
                            campo_casa,
                            ft.Container(
                                content=ft.Text("×", size=24, weight="bold"),
                                margin=ft.margin.only(top=14)
                            ),
                            campo_fora
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    erro_txt
                ], tight=True, spacing=15)
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: (setattr(edit_dialog, 'open', False), self.page.update())),
                ft.ElevatedButton("Confirmar", bgcolor=ft.colors.AMBER, color=ft.colors.BLACK, on_click=salvar_placar)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        self.page.overlay.append(edit_dialog)
        edit_dialog.open = True
        self.page.update()

    def build(self) -> ft.Control:
        rodadas = partidas_repo.listar_rodadas(self.id_torneio)
        total = len(rodadas)
        partidas = partidas_repo.partidas_da_rodada(self.id_torneio, self.rodada)

        def ir(r):
            self.router.navigate_rodadas(self.id_torneio, r)

        cards = ft.Column(spacing=10)
        for p in partidas:
            finalizada = bool(p.get("finalizada"))
            gm = p.get("gols_m")
            gv = p.get("gols_v")

            if finalizada and gm is not None and gv is not None:
                placar = f"{gm}   ×   {gv}"
                cor_placar = ft.colors.AMBER
            else:
                placar = "vs"
                cor_placar = ft.colors.WHITE38

            linha_partida = ft.Row([
                ft.Row([
                    ft.Text(p["casa"], weight="bold"),
                    ft.Image(src=p.get("escudo_casa"), width=22, height=22, fit=ft.ImageFit.CONTAIN) if p.get(
                        "escudo_casa")
                    else ft.Icon(ft.icons.SHIELD, size=22, color=ft.colors.WHITE24),
                ], alignment=ft.MainAxisAlignment.END, expand=2, tight=True),

                ft.Text(placar, size=18, weight="bold", color=cor_placar, text_align=ft.TextAlign.CENTER, expand=1),

                ft.Row([
                    ft.Image(src=p.get("escudo_fora"), width=22, height=22, fit=ft.ImageFit.CONTAIN) if p.get(
                        "escudo_fora")
                    else ft.Icon(ft.icons.SHIELD, size=22, color=ft.colors.WHITE24),
                    ft.Text(p["fora"], weight="bold"),
                ], alignment=ft.MainAxisAlignment.START, expand=2, tight=True),
            ], alignment=ft.MainAxisAlignment.CENTER)

            if self.modo_admin:
                linha_partida.controls.insert(0, ft.Container(width=40))
                linha_partida.controls.append(
                    ft.IconButton(
                        icon=ft.icons.EDIT_ROUNDED, icon_color=ft.colors.AMBER_400,
                        icon_size=16, tooltip="Alterar Placar",
                        on_click=lambda e, part=p: self.abrir_editar_placar(e, part)
                    )
                )

            cards.controls.append(ft.Container(
                content=linha_partida,
                padding=ft.padding.symmetric(horizontal=16, vertical=14),
                bgcolor=ft.colors.WHITE10,
                border_radius=10,
            ))

        nav = ft.Row([
            ft.IconButton(icon=ft.icons.ARROW_BACK_IOS, on_click=lambda _: ir(self.rodada - 1),
                          disabled=self.rodada <= 1, icon_color=ft.colors.AMBER),
            ft.Text(f"Rodada {self.rodada} / {total}", size=16, weight="bold"),
            ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, on_click=lambda _: ir(self.rodada + 1),
                          disabled=self.rodada >= total, icon_color=ft.colors.AMBER),
        ], alignment=ft.MainAxisAlignment.CENTER)

        titulo = ft.Row(
            [ft.Text("PARTIDAS", size=28, weight="w900")],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        return ft.Column([
            titulo,
            ft.Divider(color=ft.colors.WHITE10),
            nav,
            cards,
        ], spacing=12, expand=True, scroll=ft.ScrollMode.ADAPTIVE)