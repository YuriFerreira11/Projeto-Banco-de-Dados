import flet as ft


def criar_card_times(lista_times, ao_clicar_no_time):
    if not lista_times:
        return ft.Text("Nenhum time cadastrado.")

    grid = ft.GridView(
        expand=True,
        runs_count=5,  # Quantos cards por linha
        max_extent=200,  # Largura máxima de cada card
        child_aspect_ratio=1.0,
        spacing=20,
        run_spacing=20,
    )

    for time in lista_times:
        grid.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Image(src=time.escudo, width=80, height=80, fit="contain"),
                    ft.Text(time.nome, weight="bold", size=16, text_align="center"),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.colors.SURFACE_VARIANT,
                border_radius=15,
                padding=10,
                on_click=lambda e, t=time: ao_clicar_no_time(t),  # Passa o objeto time todo
                ink=True,  # Efeito visual de clique
            )
        )

    return grid