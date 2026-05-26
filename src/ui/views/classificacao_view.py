import flet as ft


def tela_classificacao(dados_classificacao, ao_clicar_torneio):
    # Header ajustado para centralizar o texto e manter o botão
    header = ft.Column([
        ft.Text("TABELA DE CLASSIFICAÇÃO", size=28, weight="w900", text_align=ft.TextAlign.CENTER),
        ft.Text("Dados extraídos diretamente do banco", size=14, color=ft.colors.WHITE54, text_align=ft.TextAlign.CENTER),
        ft.Container(height=10),
        ft.ElevatedButton(
            "Ver Info do Torneio",
            icon=ft.icons.INFO_OUTLINE,
            on_click=lambda _: ao_clicar_torneio(),
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER) # Centraliza os textos e o botão

    def celula_texto(texto, is_bold=False, cor=ft.colors.WHITE):
        return ft.DataCell(ft.Text(str(texto), weight="bold" if is_bold else "normal", color=cor))

    rows = []
    for i, item in enumerate(dados_classificacao):
        url_escudo = getattr(item, 'escudo', None)
        nome_time = getattr(item, 'nome_time', "Time Desconhecido")

        rows.append(
            ft.DataRow(
                cells=[
                    celula_texto(f"{i + 1}º", is_bold=True, cor=ft.colors.AMBER if i < 3 else ft.colors.WHITE),
                    ft.DataCell(ft.Row([
                        ft.Image(src=url_escudo, width=20, height=20) if url_escudo
                        else ft.Icon(ft.icons.SHIELD, size=20, color=ft.colors.WHITE38),
                        ft.Text(nome_time, weight="bold")
                    ], tight=True)), # Tight garante que o conteúdo não espalhe
                    celula_texto(getattr(item, 'pontos', 0), is_bold=True),
                    celula_texto(getattr(item, 'vitorias', 0)),
                    celula_texto(getattr(item, 'saldo_gols', 0)),
                ]
            )
        )

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("POS")),
            ft.DataColumn(ft.Text("TIME")),
            ft.DataColumn(ft.Text("P")),
            ft.DataColumn(ft.Text("V")),
            ft.DataColumn(ft.Text("SG")),
        ],
        rows=rows,
        heading_row_color=ft.colors.BLACK12,
        divider_thickness=1,
    )

    return ft.Column([
        header, # Agora centralizado
        ft.Divider(height=30, color=ft.colors.WHITE10),
        # Container da tabela centralizado
        ft.Container(
            content=tabela,
            bgcolor="#1E1E1E",
            padding=20,
            border_radius=15,
            alignment=ft.alignment.center # Alinha a tabela no centro do container
        )
    ],
    scroll=ft.ScrollMode.ADAPTIVE,
    expand=True,
    horizontal_alignment=ft.CrossAxisAlignment.CENTER # FORÇA O ALINHAMENTO CENTRAL DE TUDO
    )