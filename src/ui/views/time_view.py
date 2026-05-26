import flet as ft
from src.ui.components.classificacao_tabela import criar_tabela_classificacao


def tela_detalhes_time(time_obj, dados_classificacao, jogadores, ao_voltar):
    if not dados_classificacao:
        class Struct:
            posicao = "-";
            pontos = 0;
            vitorias = 0;
            empates = 0;
            derrotas = 0;
            gf = 0;
            gs = 0;
            saldo_gols = 0

        dados_classificacao = Struct()

    # Função dos quadrinhos (agora usa expand=True para se autoajustar no espaço da linha)
    def criar_card_mini(label, valor, cor_fundo, icone, cor_texto=ft.colors.WHITE70, cor_valor=ft.colors.WHITE):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icone, size=12, color=cor_texto),
                ft.Text(label, size=9, weight="bold", color=cor_texto),
                ft.Text(f"{valor}", size=16, weight="bold", color=cor_valor),
            ], horizontal_alignment="center", spacing=0),
            bgcolor=cor_fundo,
            padding=8,
            border_radius=8,
            expand=True  # Divide o espaço igualmente dentro do Row pai
        )

    # --- LADO ESQUERDO: ESTATÍSTICAS ---
    coluna_estatisticas = ft.Column([
        # Linha 1: Posição e Pontos
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("POSIÇÃO", size=12, weight="bold", color=ft.colors.BLACK54),
                    ft.Text(f"{dados_classificacao.posicao}º", size=32, weight="bold", color=ft.colors.BLACK),
                ], horizontal_alignment="center"),
                bgcolor=ft.colors.WHITE,
                padding=12,
                border_radius=12,
                expand=True
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("PONTOS", size=12, weight="bold", color=ft.colors.WHITE70),
                    ft.Text(f"{dados_classificacao.pontos}", size=32, weight="bold", color=ft.colors.WHITE),
                ], horizontal_alignment="center"),
                bgcolor="#1E1E1E",
                padding=12,
                border_radius=12,
                expand=True
            ),
        ], spacing=10),

        ft.Container(height=10),

        # Linha 2: V / E / D
        ft.Row([
            criar_card_mini("VITÓRIAS", dados_classificacao.vitorias, "#2C2C2C", ft.icons.CHECK_CIRCLE),
            criar_card_mini("EMPATES", dados_classificacao.empates, "#2C2C2C", ft.icons.REMOVE_CIRCLE),
            criar_card_mini("DERROTAS", dados_classificacao.derrotas, "#2C2C2C", ft.icons.CANCEL),
        ], spacing=10),

        ft.Container(height=10),

        # Linha 3: Gols
        ft.Row([
            criar_card_mini("GOLS PRÓ", dados_classificacao.gf, "#3D3D3D", ft.icons.ARROW_UPWARD),
            criar_card_mini("GOLS CONTRA", dados_classificacao.gs, "#3D3D3D", ft.icons.ARROW_DOWNWARD),
            criar_card_mini("SALDO GOLS", dados_classificacao.saldo_gols, "#3D3D3D", ft.icons.SWAP_VERT),
        ], spacing=10),
    ])

    # --- LADO DIREITO: ELENCO ---
    coluna_elenco = ft.Column([
        ft.Row([
            ft.Icon(ft.icons.GROUPS, size=24),
            ft.Text("Elenco Atual", size=22, weight="bold"),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),

        ft.Container(height=10),

        # A tabela de dados
        ft.Container(
            content=criar_tabela_classificacao(jogadores),
            alignment=ft.alignment.center
        )
    ], horizontal_alignment="center")

    # --- MONTAGEM DA TELA FINAL ---
    return ft.Column([
        # Cabeçalho (Intacto, ocupando toda a largura)
        ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: ao_voltar()),
            ft.Image(
                src=time_obj.escudo if time_obj.escudo else ft.icons.IMAGE_NOT_SUPPORTED,
                width=60,
                height=60,
                fit=ft.ImageFit.CONTAIN
            ),
            ft.Text(f"{time_obj.nome.upper()}", size=32, weight="bold")
        ], alignment=ft.MainAxisAlignment.START, spacing=20),

        ft.Divider(height=20),

        # Divisão da Tela: 50% Stats | 50% Elenco
        ft.ResponsiveRow([
            # No desktop (md), cada um ocupa 6 de 12 espaços (50%). No mobile (sm), ocupam 12 (100%).
            ft.Container(content=coluna_estatisticas, col={"sm": 12, "md": 6}, padding=ft.padding.only(right=10)),
            ft.Container(content=coluna_elenco, col={"sm": 12, "md": 6}, padding=ft.padding.only(left=10)),
        ], vertical_alignment=ft.CrossAxisAlignment.START)

    ], scroll=ft.ScrollMode.ADAPTIVE, expand=True)