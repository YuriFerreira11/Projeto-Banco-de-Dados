import flet as ft


# =========================================================================
# 1. TELA DE LISTAGEM DE TIMES (Mantida idêntica para compatibilidade)
# =========================================================================
def tela_listagem_times(lista_de_times, ao_clicar_no_time, ao_trocar_torneio=None, ao_gerar_tabela=None,
                        ao_lançar_resultados=None):
    def tratar_hover(e):
        if e.data == "true":
            e.control.bgcolor = "#2C2D35"
            e.control.border = ft.border.all(1, ft.colors.AMBER_400)
        else:
            e.control.bgcolor = "#1A1A1A"
            e.control.border = ft.border.all(1, ft.colors.WHITE10)
        e.control.update()

    grid_times = ft.GridView(
        runs_count=5,
        child_aspect_ratio=1.0,
        spacing=18,
        run_spacing=18,
        expand=True
    )

    for time in lista_de_times:
        url_escudo = getattr(time, 'escudo', None)
        nome_time = getattr(time, 'nome', "Time Desconhecido")

        card_time = ft.Container(
            bgcolor="#1A1A1A",
            padding=20,
            border_radius=16,
            border=ft.border.all(1, ft.colors.WHITE10),
            alignment=ft.alignment.center,
            on_click=lambda _, t=time: ao_clicar_no_time(t),
            on_hover=tratar_hover,
            content=ft.Column([
                ft.Container(
                    content=ft.Image(
                        src=url_escudo,
                        width=70,
                        height=70,
                        fit=ft.ImageFit.CONTAIN
                    ) if url_escudo else ft.Icon(ft.icons.SHIELD_ROUNDED, size=70, color=ft.colors.WHITE24),
                    alignment=ft.alignment.center,
                    expand=True
                ),
                ft.Container(height=5),
                ft.Text(
                    nome_time,
                    size=15,
                    weight="bold",
                    color=ft.colors.WHITE,
                    text_align=ft.TextAlign.CENTER,
                    max_lines=1,
                    overflow=ft.TextOverflow.ELLIPSIS
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
        )
        grid_times.controls.append(card_time)

    return ft.Container(
        content=grid_times,
        padding=ft.padding.all(15),
        expand=True
    )


# =========================================================================
# 2. TELA DE DETALHES DO TIME (Versão Harmonizada e Fluida)
# =========================================================================
def tela_detalhes_time(time_obj, dados_classificacao, jogadores, ao_voltar):
    if not dados_classificacao:
        class Struct:
            posicao = "-"
            pontos = 0
            vitorias = 0
            empates = 0
            derrotas = 0
            gf = 0
            gs = 0
            saldo_gols = 0

        dados_classificacao = Struct()

    # --- 1. BARRA DE CLASSIFICAÇÃO COM DISTRIBUIÇÃO HARMONIOSA ---
    # Usando SPACE_EVENLY para preencher proporcionalmente toda a largura disponível
    linha_classificacao = ft.Container(
        content=ft.Row([
            ft.Text(f"POSIÇÃO: {dados_classificacao.posicao}º", weight="w900", color=ft.colors.AMBER_400, size=13),
            ft.Text("•", color=ft.colors.WHITE10, size=14),
            ft.Text(f"PONTOS: {dados_classificacao.pontos}", weight="bold", color=ft.colors.WHITE, size=13),
            ft.Text("•", color=ft.colors.WHITE10, size=14),
            ft.Text(f"VITÓRIAS: {dados_classificacao.vitorias}", color=ft.colors.GREEN_400, size=13, weight="medium"),
            ft.Text("•", color=ft.colors.WHITE10, size=14),
            ft.Text(f"EMPATES: {dados_classificacao.empates}", color=ft.colors.GREY_400, size=13, weight="medium"),
            ft.Text("•", color=ft.colors.WHITE10, size=14),
            ft.Text(f"DERROTAS: {dados_classificacao.derrotas}", color=ft.colors.RED_400, size=13, weight="medium"),
            ft.Text("•", color=ft.colors.WHITE10, size=14),
            ft.Text(f"SALDO DE GOLS: {dados_classificacao.saldo_gols}", color=ft.colors.PURPLE_400, size=13,
                    weight="medium"),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="#1A1A1A",
        padding=16,
        border_radius=12,
        border=ft.border.all(1, ft.colors.WHITE10),
    )

    # --- 2. TABELA DE ELENCO PERSONALIZADA (LARGURA TOTAL FLUIDA) ---
    # Criamos um cabeçalho customizado elegante que se expande por igual
    tabela_conteudo = ft.Column(spacing=0)

    # Linha do Cabeçalho da Tabela
    tabela_conteudo.controls.append(
        ft.Container(
            content=ft.Row([
                ft.Text("JOGADOR", color=ft.colors.AMBER_400, weight="bold", size=12, expand=3),
                ft.Text("POSIÇÃO", color=ft.colors.AMBER_400, weight="bold", size=12, expand=2),
            ], alignment=ft.MainAxisAlignment.START),
            padding=ft.padding.symmetric(horizontal=20, vertical=12),
            bgcolor="#1C1D24",
            border_radius=ft.border_radius.only(top_left=12, top_right=12)
        )
    )

    # Adicionando as linhas dos jogadores com efeito zebrado sutil
    if not jogadores:
        tabela_conteudo.controls.append(
            ft.Container(
                content=ft.Text("Nenhum jogador cadastrado neste elenco.", color=ft.colors.WHITE38, size=14),
                padding=20,
                alignment=ft.alignment.center
            )
        )
    else:
        for idx, j in enumerate(jogadores):
            nome_jogador = getattr(j, 'nome', 'Sem nome')
            posicao_jogador = getattr(j, 'posicao', getattr(j, 'funcao', 'Não informada'))

            # Cor de fundo alternada para leitura agradável
            bg_row = "#05FFFFFF" if idx % 2 == 0 else ft.colors.TRANSPARENT

            tabela_conteudo.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(nome_jogador, color=ft.colors.WHITE, weight="medium", size=14, expand=3),
                        ft.Text(posicao_jogador, color=ft.colors.WHITE70, size=14, expand=2),
                    ], alignment=ft.MainAxisAlignment.START),
                    padding=ft.padding.symmetric(horizontal=20, vertical=14),
                    bgcolor=bg_row,
                    border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.WHITE10 if idx < len(
                        jogadores) - 1 else ft.colors.TRANSPARENT))
                )
            )

    # Painel estruturado do Elenco Completo
    bloco_elenco = ft.Column([
        ft.Row([
            ft.Icon(ft.icons.GROUPS_ROUNDED, size=20, color=ft.colors.WHITE54),
            ft.Text("Elenco Atual", size=18, weight="bold", color=ft.colors.WHITE),
        ], alignment=ft.MainAxisAlignment.START, spacing=8),

        ft.Container(height=6),

        ft.Container(
            content=tabela_conteudo,
            bgcolor="#141414",
            border_radius=12,
            border=ft.border.all(1, ft.colors.WHITE10),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS  # Garante que o efeito zebrado respeite as bordas arredondadas
        )
    ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    # --- 3. ESTRUTURAÇÃO FINAL DA VIEW ---
    url_escudo = getattr(time_obj, 'escudo', None)
    nome_time = getattr(time_obj, 'nome', "TIME")

    return ft.Container(
        content=ft.Column([
            # Cabeçalho do Time
            ft.Row([
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK_ROUNDED,
                    icon_color=ft.colors.WHITE70,
                    on_click=lambda _: ao_voltar()
                ),
                ft.Container(
                    content=ft.Image(
                        src=url_escudo,
                        width=45,
                        height=45,
                        fit=ft.ImageFit.CONTAIN,
                    ) if url_escudo else ft.Icon(ft.icons.SHIELD, size=45, color=ft.colors.WHITE24),
                    margin=ft.margin.only(left=5, right=5)
                ),
                ft.Text(f"{nome_time.upper()}", size=26, weight="w900", color=ft.colors.WHITE)
            ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),

            ft.Divider(height=20, color=ft.colors.WHITE10),

            # Estatísticas do Painel
            linha_classificacao,

            ft.Container(height=15),

            # Elenco Harmonizado ocupando toda a área inferior de forma limpa
            bloco_elenco

        ], scroll=ft.ScrollMode.ADAPTIVE, expand=True),
        padding=15,
        expand=True
    )