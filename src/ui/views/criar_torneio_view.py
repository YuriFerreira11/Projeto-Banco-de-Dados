import flet as ft
from repository.torneio_repository import TorneioRepository
from repository.time_repository import TimeRepository
from repository.jogador_repository import JogadorRepository


def tela_criar_torneio(ao_concluir, ao_voltar):
    # Definimos larguras exatas para que a soma feche perfeitamente dentro dos 750px do form
    LARGURA_FORM = 750

    # Dados do Torneio com tamanhos fixos e proporcionais
    campo_nome = ft.TextField(label="Nome do Torneio", width=LARGURA_FORM, border_color=ft.colors.AMBER)
    campo_inicio = ft.TextField(label="Data Início (AAAA-MM-DD)", width=365, border_color=ft.colors.WHITE24)
    campo_fim = ft.TextField(label="Data Fim (AAAA-MM-DD)", width=365, border_color=ft.colors.WHITE24)

    # Coluna dos times SEM scroll próprio para não brigar com o scroll do container principal
    times_col = ft.Column(spacing=8)
    status = ft.Text("", size=13)

    def novo_campo_time():
        # Usando larguras fixas em vez de expand para evitar o erro de TransformLayer
        nome_t = ft.TextField(label="Nome do Time", width=280, border_color=ft.colors.WHITE24)
        escudo_t = ft.TextField(label="URL do Escudo", width=390, border_color=ft.colors.WHITE24)
        btn_rem = ft.IconButton(
            icon=ft.icons.REMOVE_CIRCLE_OUTLINE,
            icon_color=ft.colors.RED_400,
        )
        row = ft.Row([nome_t, escudo_t, btn_rem], spacing=10, alignment=ft.MainAxisAlignment.START)
        btn_rem.on_click = lambda _: (times_col.controls.remove(row), times_col.update())
        return row

    # Inicia com 4 campos padrão
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
            (row.controls[0].value.strip(), row.controls[1].value.strip())
            for row in times_col.controls
            if row.controls[0].value.strip()
        ]

        if len(times_data) < 2:
            status.value = "⚠️ Adicione pelo menos 2 times."
            status.color = ft.colors.AMBER
            status.update()
            return

        if len(times_data) % 2 != 0:
            status.value = "⚠️ O número de times deve ser par."
            status.color = ft.colors.AMBER
            status.update()
            return

        try:
            id_torneio = TorneioRepository.criar_torneio(nome_torneio, inicio or None, fim or None)

            for nome_t, escudo_t in times_data:
                id_time = TimeRepository.criar_time(nome_t, escudo_t or None)
                TorneioRepository.vincular_time(id_torneio, id_time)
                JogadorRepository.gerar_jogadores_para_time(id_time, nome_t)

            status.value = f"✅ Torneio '{nome_torneio}' criado com {len(times_data)} times!"
            status.color = ft.colors.GREEN_300
            status.update()
            ao_concluir()

        except Exception as ex:
            status.value = f"❌ Erro: {ex}"
            status.color = ft.colors.RED_400
            status.update()

    # Estrutura interna do formulário centralizado
    form_body = ft.Column(
        width=LARGURA_FORM,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        spacing=15,
        controls=[
            # Cabeçalho com o botão VOLTAR no canto direito
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

            # Dados básicos do torneio
            ft.Text("Dados do Torneio", size=14, color=ft.colors.WHITE70, weight="bold"),
            campo_nome,
            ft.Row([campo_inicio, campo_fim], spacing=20, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Divider(color=ft.colors.WHITE10, height=1),

            # Seção de times com o botão "+ Adicionar Time" alinhado à direita
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.END,
                controls=[
                    ft.Column([
                        ft.Text("Times", size=16, color=ft.colors.WHITE70, weight="bold"),
                        ft.Text("Os jogadores serão gerados automaticamente (11 por time).", size=11,
                                color=ft.colors.WHITE38)
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

            # Botão de enviar
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

    # O truque final: Coluna externa com Scroll adaptável cuida da tela inteira sem quebrar os filhos!
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