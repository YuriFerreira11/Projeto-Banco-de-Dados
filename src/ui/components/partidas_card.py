import flet as ft


def criar_card_partidas(partidas):
    def formatar_placar(gols):
        # Se os gols forem None (banco de dados), retorna vazio para o placar
        return str(gols) if gols is not None else ""

    def criar_card_confronto(p):
        # Lógica para verificar se o jogo já aconteceu
        jogo_realizado = p.gols_m is not None and p.gols_v is not None

        return ft.Container(
            content=ft.Column([
                # 1. Cabeçalho do Card (Local e Data)
                ft.Row([
                    ft.Icon(ft.icons.LOCATION_ON, size=12, color=ft.colors.WHITE54),
                    ft.Text(f"{p.local}  •  {p.data_hora}", size=11, color=ft.colors.WHITE54),
                ], alignment=ft.MainAxisAlignment.CENTER),

                ft.Divider(height=1, color=ft.colors.WHITE10),

                # 2. O Confronto (Time A x Time B)
                ft.Row([
                    # Time Mandante
                    ft.Row([
                        ft.Text(p.nome_mandante, weight="bold", size=16),
                        ft.Image(src=p.escudo_mandante, width=30, height=30) if p.escudo_mandante
                        else ft.Icon(ft.icons.SHIELD, size=30),
                    ], alignment=ft.MainAxisAlignment.END, expand=True),

                    # Placar Central
                    ft.Container(
                        content=ft.Row([
                            ft.Text(formatar_placar(p.gols_m), size=22, weight="w900", color=ft.colors.AMBER),
                            ft.Text("X" if not jogo_realizado else "-", size=14, weight="bold",
                                    color=ft.colors.WHITE38),
                            ft.Text(formatar_placar(p.gols_v), size=22, weight="w900", color=ft.colors.AMBER),
                        ], alignment=ft.MainAxisAlignment.CENTER, tight=True),
                        bgcolor=ft.colors.BLACK12,
                        padding=ft.padding.symmetric(horizontal=15, vertical=5),
                        border_radius=8,
                    ),

                    # Time Visitante
                    ft.Row([
                        ft.Image(src=p.escudo_visitante, width=30, height=30) if p.escudo_visitante
                        else ft.Icon(ft.icons.SHIELD, size=30),
                        ft.Text(p.nome_visitante, weight="bold", size=16),
                    ], alignment=ft.MainAxisAlignment.START, expand=True),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ], spacing=15),

            bgcolor="#1E1E1E",
            padding=20,
            border_radius=12,
            border=ft.border.all(1, ft.colors.WHITE10),
            margin=ft.margin.only(bottom=10),
            width=800,  # Largura fixa para manter o padrão na tela centralizada
        )

    # Retorna uma coluna centralizada com todos os cards
    return ft.Column(
        controls=[criar_card_confronto(p) for p in partidas],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.ADAPTIVE
    )