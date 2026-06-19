import flet as ft


def tela_classificacao(dados_classificacao, ao_clicar_torneio=None):
    # Header simplificado: apenas o título
    header = ft.Column([
        ft.Text("TABELA DE CLASSIFICAÇÃO", size=28, weight="w900", text_align=ft.TextAlign.CENTER),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    # Helper alterado para alinhar à ESQUERDA com um leve respiro (padding)
    def celula_texto(texto, is_bold=False, cor=ft.colors.WHITE):
        return ft.DataCell(
            ft.Container(
                content=ft.Text(str(texto), weight="bold" if is_bold else "normal", color=cor),
                alignment=ft.alignment.center_left,
                padding=ft.padding.only(left=15)  # Evita que o texto cole na linha vertical
            )
        )

    rows = []
    for i, item in enumerate(dados_classificacao):
        url_escudo = getattr(item, 'escudo', None)
        nome_time = getattr(item, 'nome_time', "Time Desconhecido")

        bg_linha = "#0AFFFFFF" if i % 2 == 0 else ft.colors.TRANSPARENT

        rows.append(
            ft.DataRow(
                color=bg_linha,
                cells=[
                    # POS - Alinhado à Esquerda
                    celula_texto(f"{i + 1}º", is_bold=True, cor=ft.colors.AMBER if i < 3 else ft.colors.WHITE),

                    # TIME - Escudo e Nome alinhados perfeitamente à esquerda
                    ft.DataCell(
                        ft.Container(
                            content=ft.Row([
                                ft.Image(src=url_escudo, width=22, height=22, fit=ft.ImageFit.CONTAIN) if url_escudo
                                else ft.Icon(ft.icons.SHIELD, size=22, color=ft.colors.WHITE24),
                                ft.Text(nome_time, weight="bold", size=14)
                            ], tight=True, spacing=12, alignment=ft.MainAxisAlignment.START),
                            alignment=ft.alignment.center_left,
                            padding=ft.padding.only(left=15)
                        )
                    ),

                    # P, V, GP, GC, SG - Todos alinhados à esquerda para consistência
                    celula_texto(getattr(item, 'pontos', 0), is_bold=True),
                    celula_texto(getattr(item, 'vitorias', 0)),
                    celula_texto(getattr(item, 'gf', getattr(item, 'gols_pro', 0))),
                    celula_texto(getattr(item, 'gs', getattr(item, 'gols_contra', 0))),
                    celula_texto(getattr(item, 'saldo_gols', 0)),
                ]
            )
        )

    tabela = ft.DataTable(
        width=850,
        heading_row_height=45,
        data_row_min_height=50,
        heading_row_color=ft.colors.BLACK26,
        column_spacing=20,

        border=ft.border.all(1, ft.colors.WHITE10),
        vertical_lines=ft.BorderSide(1, ft.colors.WHITE10),
        horizontal_lines=ft.BorderSide(1, ft.colors.WHITE10),

        columns=[
            # Todos os cabeçalhos alterados para ft.alignment.center_left com padding idêntico
            ft.DataColumn(ft.Container(ft.Text("POS", weight="bold", color=ft.colors.AMBER), alignment=ft.alignment.center_left, padding=ft.padding.only(left=15))),
            ft.DataColumn(ft.Container(ft.Text("TIME", weight="bold"), alignment=ft.alignment.center_left, padding=ft.padding.only(left=15))),
            ft.DataColumn(ft.Container(ft.Text("P", weight="bold"), alignment=ft.alignment.center_left, padding=ft.padding.only(left=15))),
            ft.DataColumn(ft.Container(ft.Text("V", weight="bold"), alignment=ft.alignment.center_left, padding=ft.padding.only(left=15))),
            ft.DataColumn(ft.Container(ft.Text("GP", weight="bold"), alignment=ft.alignment.center_left, padding=ft.padding.only(left=15))),
            ft.DataColumn(ft.Container(ft.Text("GC", weight="bold"), alignment=ft.alignment.center_left, padding=ft.padding.only(left=15))),
            ft.DataColumn(ft.Container(ft.Text("SG", weight="bold"), alignment=ft.alignment.center_left, padding=ft.padding.only(left=15))),
        ],
        rows=rows,
    )

    return ft.Column([
        header,
        ft.Divider(height=25, color=ft.colors.WHITE10),

        ft.Container(
            content=tabela,
            bgcolor="#141414",
            padding=10,
            border_radius=12,
        )
    ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )


def criar_tabela_classificacao(lista_objetos):
    if not lista_objetos:
        return ft.Container(
            content=ft.Text("Nenhum registro encontrado.", size=16),
            padding=20,
            alignment=ft.alignment.center
        )

    colunas = [
        ft.DataColumn(ft.Text(str(col).replace("_", " ").upper(), weight="bold"))
        for col in lista_objetos[0].__dict__.keys()
    ]

    linhas = []
    for obj in lista_objetos:
        linhas.append(
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(valor))) for valor in obj.__dict__.values()]
            )
        )

    return ft.DataTable(
        columns=colunas,
        rows=linhas,
        heading_row_color=ft.colors.SURFACE_VARIANT,
        border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
        border_radius=10,
        column_spacing=40
    )
