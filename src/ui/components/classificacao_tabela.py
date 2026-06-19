import flet as ft


def criar_tabela_classificacao(lista_objetos):
    if not lista_objetos:
        return ft.Container(
            content=ft.Text("Nenhum registro encontrado.", size=16),
            padding=20,
            alignment=ft.alignment.center
        )

    # Extrai os nomes das colunas baseados nos atributos da classe
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
        # 'border' com 'b' minúsculo é o segredo aqui
        border=ft.border.all(1, ft.colors.OUTLINE_VARIANT),
        border_radius=10,
        column_spacing=40
    )
