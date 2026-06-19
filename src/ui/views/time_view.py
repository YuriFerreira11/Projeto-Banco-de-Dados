import flet as ft


def time_view(page: ft.Page, ao_clicar_no_time, lista_times):
    """
    Renderiza a interface com os cards contendo todos os times cadastrados no banco.
    """

    grid_times = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=220,
        child_aspect_ratio=1.1,
        spacing=15,
        run_spacing=15,
    )

    # Varre a lista de objetos vinda do banco de dados
    for time in lista_times:
        grid_times.controls.append(
            ft.GestureDetector(
                content=ft.Container(
                    content=ft.Column(
                        [
                            # Substitua o ft.Icon por uma lógica que verifica a imagem:
                            ft.Image(src=getattr(time, "escudo", None), width=45, height=45,
                                     fit=ft.ImageFit.CONTAIN) if getattr(time, "escudo", None)
                            else ft.Icon(ft.icons.SHIELD_ROUNDED, size=45, color=ft.colors.PRIMARY),
                            ft.Text(
                                value=getattr(time, "nome", "Time Indefinido"),
                                weight=ft.FontWeight.BOLD,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS
                            ),
                            ft.Text(
                                value=f"Série {getattr(time, 'serie', 'A')}",
                                size=12,
                                color=ft.colors.OUTLINE
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor="#1E1E1E",
                    border_radius=12,
                    padding=10,
                    animate_scale=ft.animation.Animation(300, ft.AnimationCurve.EASE_OUT),
                ),
                # Linha 36 corrigida: Mapeamento explícito via argumento padrão do lambda (t=time)
                # No Flet 0.21.2 o GestureDetector usa on_tap, não on_click
                on_tap=lambda _, t=time: ao_clicar_no_time(t),
            )
        )

    return ft.Column(
        controls=[
            ft.Text("TIMES DO TORNEIO", size=28, weight="w900", text_align=ft.TextAlign.CENTER),
            ft.Divider(height=10),
            grid_times
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
