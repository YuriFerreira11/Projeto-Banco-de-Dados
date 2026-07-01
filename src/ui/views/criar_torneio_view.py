import flet as ft
from src.repository.torneio_repository import TorneioRepository
from src.repository.time_repository import TimeRepository
from src.repository.jogador_repository import JogadorRepository
from src.services.partidas_logic import PartidasLogic  # Importando a lógica de partidas


def tela_criar_torneio(ao_concluir, ao_voltar):
    LARGURA_FORM = 750

    campo_nome = ft.TextField(label="Nome do Torneio", width=LARGURA_FORM, border_color=ft.colors.AMBER)
    campo_inicio = ft.TextField(label="Data Início (AAAA-MM-DD)", width=315, border_color=ft.colors.WHITE24)
    campo_fim = ft.TextField(label="Data Fim (AAAA-MM-DD)", width=315, border_color=ft.colors.WHITE24)


    def mudar_data_inicio(e):
        if picker_inicio.value:
            # Formata o objeto date nativo em string AAAA-MM-DD
            campo_inicio.value = picker_inicio.value.strftime("%Y-%m-%d")
            campo_inicio.update()


    def mudar_data_fim(e):
        if picker_fim.value:
            campo_fim.value = picker_fim.value.strftime("%Y-%m-%d")
            campo_fim.update()


    picker_inicio = ft.DatePicker(
        on_change=mudar_data_inicio,
        help_text="Selecione a data de início do torneio"
    )
    picker_fim = ft.DatePicker(
        on_change=mudar_data_fim,
        help_text="Selecione a data de término do torneio"
    )

    chk_auto_gerar = ft.Checkbox(
        label="Gerar tabela de partidas (rodadas) automaticamente após a criação",
        value=False,
        label_style=ft.TextStyle(color=ft.colors.WHITE70, size=13)
    )

    times_col = ft.Column(spacing=8)
    status = ft.Text("", size=13)

    jogadores_col = ft.Column(spacing=8, scroll=ft.ScrollMode.ADAPTIVE)
    linha_alvo_atual = None

    def nova_linha_jogador(nome="", funcao=""):
        campo_nome_j = ft.TextField(label="Nome do Jogador", value=nome, width=240, border_color=ft.colors.WHITE24)
        campo_funcao_j = ft.Dropdown(
            label="Função",
            value=funcao if funcao else "Meia",
            width=160,
            border_color=ft.colors.WHITE24,
            options=[
                ft.dropdown.Option("Goleiro"),
                ft.dropdown.Option("Zagueiro"),
                ft.dropdown.Option("Lateral"),
                ft.dropdown.Option("Volante"),
                ft.dropdown.Option("Meia"),
                ft.dropdown.Option("Atacante"),
            ]
        )
        btn_rem_j = ft.IconButton(icon=ft.icons.REMOVE_CIRCLE_OUTLINE, icon_color=ft.colors.RED_400)
        row_j = ft.Row([campo_nome_j, campo_funcao_j, btn_rem_j], spacing=10, alignment=ft.MainAxisAlignment.START)
        btn_rem_j.on_click = lambda _: (jogadores_col.controls.remove(row_j), jogadores_col.update())
        return row_j

    def salvar_elenco_modal(e):
        nonlocal linha_alvo_atual
        if linha_alvo_atual:
            lista_jogadores = []
            for row in jogadores_col.controls:
                nome_j = row.controls[0].value.strip()
                funcao_j = row.controls[1].value
                if nome_j:
                    lista_jogadores.append({"nome": nome_j, "funcao": funcao_j})

            linha_alvo_atual.data = lista_jogadores
            btn_elenco = linha_alvo_atual.controls[2]
            if lista_jogadores:
                btn_elenco.icon_color = ft.colors.GREEN_400
                btn_elenco.tooltip = f"{len(lista_jogadores)} jogadores definidos"
            else:
                btn_elenco.icon_color = ft.colors.WHITE30
                btn_elenco.tooltip = "Adicionar Elenco"

            linha_alvo_atual.update()
        fechar_elenco_modal(e)

    def fechar_elenco_modal(e):
        elenco_modal.open = False
        e.page.update()

    elenco_modal = ft.AlertDialog(
        modal=True,
        title=ft.Row([
            ft.Text("Gerenciar Elenco", weight="bold", size=18),
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.icons.ADD, size=16, color=ft.colors.AMBER),
                    ft.Text("Jogador", color=ft.colors.AMBER, size=12, weight="bold"),
                ], tight=True),
                on_click=lambda _: (jogadores_col.controls.append(nova_linha_jogador()), jogadores_col.update())
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        content=ft.Container(content=jogadores_col, width=480, height=400, padding=ft.padding.only(right=10)),
        actions=[
            ft.TextButton("Cancelar", on_click=fechar_elenco_modal, style=ft.ButtonStyle(color=ft.colors.WHITE54)),
            ft.ElevatedButton("Confirmar", bgcolor=ft.colors.AMBER, color=ft.colors.BLACK, on_click=salvar_elenco_modal)
        ],
        actions_alignment=ft.MainAxisAlignment.END
    )

    def abrir_elenco_modal(e, row, nome_time_atual):
        nonlocal linha_alvo_atual
        linha_alvo_atual = row
        elenco_modal.title.controls[0].value = f"Elenco - {nome_time_atual if nome_time_atual else 'Time'}"

        jogadores_col.controls.clear()
        if row.data:
            for jog in row.data:
                jogadores_col.controls.append(nova_linha_jogador(jog["nome"], jog["funcao"]))
        else:
            jogadores_col.controls.append(nova_linha_jogador())
            jogadores_col.controls.append(nova_linha_jogador())

        if elenco_modal not in e.page.overlay:
            e.page.overlay.append(elenco_modal)

        elenco_modal.open = True
        e.page.update()

    def novo_campo_time():
        nome_t = ft.TextField(label="Nome do Time", width=250, border_color=ft.colors.WHITE24)
        escudo_t = ft.TextField(label="URL do Escudo", width=340, border_color=ft.colors.WHITE24)
        btn_elenco = ft.IconButton(icon=ft.icons.PEOPLE_OUTLINE, icon_color=ft.colors.WHITE30,
                                   tooltip="Adicionar Elenco Manual")
        btn_rem = ft.IconButton(icon=ft.icons.REMOVE_CIRCLE_OUTLINE, icon_color=ft.colors.RED_400)

        row = ft.Row([nome_t, escudo_t, btn_elenco, btn_rem], spacing=10, alignment=ft.MainAxisAlignment.START)
        row.data = []

        btn_elenco.on_click = lambda e: abrir_elenco_modal(e, row, nome_t.value.strip())
        btn_rem.on_click = lambda _: (times_col.controls.remove(row), times_col.update())
        return row

    for _ in range(4):
        times_col.controls.append(novo_campo_time())

    def criar(e):
        status.value = ""
        nome_torneio = campo_nome.value.strip()
        inicio = campo_inicio.value.strip()
        fim = campo_fim.value.strip()

        if not nome_torneio:
            status.value = "⚠️ Nome do torneio obrigatório."
            status.color = ft.colors.AMBER
            status.update()
            return

        times_data = [
            (row.controls[0].value.strip(), row.controls[1].value.strip(), row.data)
            for row in times_col.controls
            if row.controls[0].value.strip()
        ]

        if len(times_data) < 2:
            status.value = "⚠️ Adicione pelo menos 2 times."
            status.color = ft.colors.AMBER
            status.update()
            return

        if len(times_data) % 2 != 0:
            status.value = "⚠️ O número de times deve ser par para gerar os confrontos."
            status.color = ft.colors.AMBER
            status.update()
            return

        try:
            id_torneio = TorneioRepository.criar_torneio(nome_torneio, inicio or None, fim or None)

            for nome_t, escudo_t, elenco_customizado in times_data:
                id_time = TimeRepository.criar_time(nome_t, escudo_t or None)
                TorneioRepository.vincular_time(id_torneio, id_time)

                if elenco_customizado:
                    for jog in elenco_customizado:
                        JogadorRepository.criar_jogador(jog["nome"], jog["funcao"], id_time)

            msg_partidas = ""
            if chk_auto_gerar.value:
                total_jogos = PartidasLogic.gerar_e_salvar(id_torneio)
                msg_partidas = f" e {total_jogos} jogos gerados!"

            status.value = f"Torneio '{nome_torneio}' criado com {len(times_data)} times{msg_partidas}."
            status.color = ft.colors.GREEN_300
            status.update()
            ao_concluir()

        except Exception as ex:
            status.value = f"Erro ao criar torneio/partidas: {ex}"
            status.color = ft.colors.RED_400
            status.update()

    # Função auxiliar injetada no ciclo de renderização para acoplar os pickers na página
    def acoplar_pickers_e_abrir(e, picker):
        if picker not in e.page.overlay:
            e.page.overlay.append(picker)
            e.page.update()
        picker.pick_date()

    form_body = ft.Column(
        width=LARGURA_FORM,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        spacing=15,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("Criar Novo Torneio", size=24, weight="bold", color=ft.colors.AMBER),
                    ft.TextButton(
                        content=ft.Row([
                            ft.Icon(ft.icons.ARROW_BACK, size=16, color=ft.colors.WHITE70),
                            ft.Text("VOLTAR", color=ft.colors.WHITE70, size=12, weight="bold")
                        ], tight=True),
                        on_click=lambda _: ao_voltar()
                    )
                ]
            ),
            ft.Divider(color=ft.colors.WHITE10, height=1),

            ft.Text("Dados do Torneio", size=14, color=ft.colors.WHITE70, weight="bold"),
            campo_nome,

            ft.Row([
                ft.Row([
                    campo_inicio,
                    ft.IconButton(
                        icon=ft.icons.CALENDAR_MONTH_ROUNDED,
                        icon_color=ft.colors.AMBER,
                        tooltip="Escolher data de início",
                        on_click=lambda e: acoplar_pickers_e_abrir(e, picker_inicio)
                    )
                ], spacing=0, tight=True),
                ft.Row([
                    campo_fim,
                    ft.IconButton(
                        icon=ft.icons.CALENDAR_MONTH_ROUNDED,
                        icon_color=ft.colors.AMBER,
                        tooltip="Escolher data de término",
                        on_click=lambda e: acoplar_pickers_e_abrir(e, picker_fim)
                    )
                ], spacing=0, tight=True)
            ], spacing=10, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Container(content=chk_auto_gerar, padding=ft.padding.only(top=5, bottom=5)),

            ft.Divider(color=ft.colors.WHITE10, height=1),

            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.END,
                controls=[
                    ft.Column([
                        ft.Text("Times", size=16, color=ft.colors.WHITE70, weight="bold"),
                        ft.Text("Clique no ícone de grupo ao lado do time para preencher Nome e Posição do elenco.",
                                size=11, color=ft.colors.WHITE38)
                    ], spacing=2),
                    ft.TextButton(
                        content=ft.Row([
                            ft.Icon(ft.icons.ADD, size=16, color=ft.colors.AMBER),
                            ft.Text("Adicionar Time", color=ft.colors.AMBER, size=12, weight="bold"),
                        ], tight=True),
                        on_click=lambda _: (times_col.controls.append(novo_campo_time()), times_col.update()),
                    ),
                ]
            ),

            times_col,
            status,
            ft.Container(height=5),

            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.ElevatedButton(
                        "Criar Torneio",
                        icon=ft.icons.CHECK_CIRCLE,
                        bgcolor=ft.colors.AMBER,
                        color=ft.colors.BLACK,
                        on_click=criar,
                    )
                ]
            )
        ]
    )

    return ft.Column(
        controls=[
            ft.Container(
                content=form_body,
                alignment=ft.alignment.top_center,
                padding=ft.padding.only(top=10, bottom=40),
            )
        ],
        scroll=ft.ScrollMode.ADAPTIVE,
        expand=True
    )
