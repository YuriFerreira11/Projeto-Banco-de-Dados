"""
View pública: exibe rodadas e placares (somente leitura).
View admin: lança resultados das partidas.
"""
import flet as ft
from repository import partidas_repository as partidas_repo


class RodadasView:
    """Visualização pública — sem edição."""

    def __init__(self, router, page: ft.Page,
                 id_torneio: int = None, rodada: int = 1, **kwargs):
        self.router     = router
        self.page       = page
        self.id_torneio = id_torneio
        self.rodada     = rodada

    def build(self) -> ft.Control:
        rodadas  = partidas_repo.listar_rodadas(self.id_torneio)
        total    = len(rodadas)
        partidas = partidas_repo.partidas_da_rodada(self.id_torneio, self.rodada)

        def ir(r):
            self.router.navigate_rodadas(self.id_torneio, r)

        cards = ft.Column(spacing=10)
        for p in partidas:
            finalizada = bool(p.get("finalizada"))
            gm = p.get("gols_m")
            gv = p.get("gols_v")

            if finalizada and gm is not None and gv is not None:
                placar    = f"{gm}  ×  {gv}"
                cor_placar = ft.colors.AMBER
            else:
                placar    = "vs"
                cor_placar = ft.colors.WHITE38

            cards.controls.append(ft.Container(
                content=ft.Row([
                    ft.Text(p["casa"], expand=2, weight="bold",
                            text_align=ft.TextAlign.RIGHT),
                    ft.Text(placar, size=18, weight="bold",
                            color=cor_placar,
                            text_align=ft.TextAlign.CENTER, expand=1),
                    ft.Text(p["fora"], expand=2, weight="bold"),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.symmetric(horizontal=16, vertical=14),
                bgcolor=ft.colors.WHITE10,
                border_radius=10,
            ))

        nav = ft.Row([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK_IOS,
                on_click=lambda _: ir(self.rodada - 1),
                disabled=self.rodada <= 1,
                icon_color=ft.colors.AMBER,
            ),
            ft.Text(f"Rodada {self.rodada} / {total}", size=16, weight="bold"),
            ft.IconButton(
                icon=ft.icons.ARROW_FORWARD_IOS,
                on_click=lambda _: ir(self.rodada + 1),
                disabled=self.rodada >= total,
                icon_color=ft.colors.AMBER,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)

        return ft.Column([
            ft.Row([
                ft.Text("Rodadas", size=22, weight="bold", color=ft.colors.AMBER),
                ft.ElevatedButton(
                    "Classificação", icon=ft.icons.LEADERBOARD,
                    bgcolor=ft.colors.WHITE12, color=ft.colors.WHITE,
                    on_click=lambda _: self.router.navigate("classificacao"),
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(color=ft.colors.WHITE10),
            nav,
            cards,
        ], spacing=12, expand=True, scroll=ft.ScrollMode.ADAPTIVE)


class AdminRodadasView:
    """Interface do admin para lançar resultados."""

    def __init__(self, router, page: ft.Page,
                 id_torneio: int = None, rodada: int = 1, **kwargs):
        self.router     = router
        self.page       = page
        self.id_torneio = id_torneio
        self.rodada     = rodada

    def build(self) -> ft.Control:
        rodadas  = partidas_repo.listar_rodadas(self.id_torneio)
        total    = len(rodadas)
        partidas = partidas_repo.partidas_da_rodada(self.id_torneio, self.rodada)

        status = ft.Text("", size=12)
        cards  = ft.Column(spacing=10)

        def ir(r):
            self.router.navigate_admin_rodadas(self.id_torneio, r)

        def build_card(p):
            finalizada = bool(p.get("finalizada"))
            gm = p.get("gols_m")
            gv = p.get("gols_v")

            gc_field = ft.TextField(
                value="" if gm is None else str(gm),
                width=60, text_align=ft.TextAlign.CENTER,
                border_color=ft.colors.AMBER,
                disabled=finalizada,
                input_filter=ft.NumbersOnlyInputFilter(),
            )
            gf_field = ft.TextField(
                value="" if gv is None else str(gv),
                width=60, text_align=ft.TextAlign.CENTER,
                border_color=ft.colors.AMBER,
                disabled=finalizada,
                input_filter=ft.NumbersOnlyInputFilter(),
            )

            def salvar(e, pid=p["id_partida"]):
                try:
                    gc = int(gc_field.value)
                    gf = int(gf_field.value)
                except ValueError:
                    status.value = "⚠️ Digite números válidos."
                    status.color = ft.colors.RED_300
                    status.update(); return

                ok = partidas_repo.registrar_resultado(pid, gc, gf)
                if ok:
                    status.value = "✅ Resultado salvo!"
                    status.color = ft.colors.GREEN_300
                    gc_field.disabled = True
                    gf_field.disabled = True
                    gc_field.update(); gf_field.update()
                else:
                    status.value = "Partida já finalizada."
                    status.color = ft.colors.WHITE54
                status.update()

            return ft.Container(
                content=ft.Row([
                    ft.Text(p["casa"], expand=2, weight="bold",
                            text_align=ft.TextAlign.RIGHT),
                    gc_field,
                    ft.Text("×", size=16, weight="bold",
                            text_align=ft.TextAlign.CENTER),
                    gf_field,
                    ft.Text(p["fora"], expand=2, weight="bold"),
                    ft.IconButton(
                        icon=ft.icons.SAVE_ALT,
                        icon_color=ft.colors.AMBER,
                        tooltip="Salvar resultado",
                        on_click=salvar,
                        disabled=finalizada,
                    ),
                    ft.Container(
                        content=ft.Text("✔", size=12, color=ft.colors.GREEN_300),
                        visible=finalizada,
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                bgcolor=ft.colors.WHITE10,
                border_radius=10,
            )

        for p in partidas:
            cards.controls.append(build_card(p))

        nav = ft.Row([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK_IOS,
                on_click=lambda _: ir(self.rodada - 1),
                disabled=self.rodada <= 1,
                icon_color=ft.colors.AMBER,
            ),
            ft.Text(f"Rodada {self.rodada} / {total}", size=16, weight="bold"),
            ft.IconButton(
                icon=ft.icons.ARROW_FORWARD_IOS,
                on_click=lambda _: ir(self.rodada + 1),
                disabled=self.rodada >= total,
                icon_color=ft.colors.AMBER,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)

        return ft.Column([
            ft.Row([
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_color=ft.colors.WHITE70,
                    tooltip="Voltar",
                    on_click=lambda _: self.router.navigate("partidas"),
                ),
                ft.Text("Admin — Lançar Resultados",
                        size=20, weight="bold", color=ft.colors.AMBER),
            ]),
            ft.Divider(color=ft.colors.WHITE10),
            nav,
            cards,
            status,
        ], spacing=12, expand=True, scroll=ft.ScrollMode.ADAPTIVE)
