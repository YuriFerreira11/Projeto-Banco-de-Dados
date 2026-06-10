import flet as ft
from repository.torneio_repository import TorneioRepository
from repository.time_repository import TimeRepository
from repository.jogador_repository import JogadorRepository


def tela_criar_torneio(ao_concluir):
    campo_nome   = ft.TextField(label="Nome do Torneio", width=400, border_color=ft.colors.AMBER)
    campo_inicio = ft.TextField(label="Data Início (AAAA-MM-DD)", width=190, border_color=ft.colors.AMBER)
    campo_fim    = ft.TextField(label="Data Fim   (AAAA-MM-DD)", width=190, border_color=ft.colors.AMBER)

    times_col = ft.Column(spacing=8, scroll=ft.ScrollMode.ADAPTIVE)
    status    = ft.Text("", size=13)

    def novo_campo_time():
        nome_t   = ft.TextField(label="Nome do Time",  width=220, border_color=ft.colors.WHITE38)
        escudo_t = ft.TextField(label="URL do Escudo", width=300, border_color=ft.colors.WHITE38)
        btn_rem  = ft.IconButton(
            icon=ft.icons.REMOVE_CIRCLE_OUTLINE,
            icon_color=ft.colors.RED_400,
        )
        row = ft.Row([nome_t, escudo_t, btn_rem], spacing=8)
        btn_rem.on_click = lambda _: (times_col.controls.remove(row), times_col.update())
        return row

    for _ in range(4):
        times_col.controls.append(novo_campo_time())

    def criar(e):
        status.value = ""
        nome_torneio = campo_nome.value.strip()
        inicio       = campo_inicio.value.strip()
        fim          = campo_fim.value.strip()

        if not nome_torneio:
            status.value = "⚠️ Nome do torneio obrigatório."
            status.color = ft.colors.AMBER
            status.update(); return

        times_data = [
            (row.controls[0].value.strip(), row.controls[1].value.strip())
            for row in times_col.controls
            if row.controls[0].value.strip()
        ]

        if len(times_data) < 2:
            status.value = "⚠️ Adicione pelo menos 2 times."
            status.color = ft.colors.AMBER
            status.update(); return
        if len(times_data) % 2 != 0:
            status.value = "⚠️ O número de times deve ser par."
            status.color = ft.colors.AMBER
            status.update(); return

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

    return ft.Column([
        ft.Text("Criar Novo Torneio", size=24, weight="bold", color=ft.colors.AMBER),
        ft.Divider(color=ft.colors.WHITE10),
        ft.Text("Dados do Torneio", size=14, color=ft.colors.WHITE70),
        campo_nome,
        ft.Row([campo_inicio, campo_fim], spacing=12),
        ft.Container(height=10),
        ft.Row([
            ft.Text("Times", size=14, color=ft.colors.WHITE70),
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.icons.ADD, size=16, color=ft.colors.AMBER),
                    ft.Text("Adicionar Time", color=ft.colors.AMBER, size=12),
                ], tight=True),
                on_click=lambda _: (times_col.controls.append(novo_campo_time()), times_col.update()),
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Text("Os jogadores serão gerados automaticamente (11 por time).",
                size=11, color=ft.colors.WHITE38),
        times_col,
        ft.Container(height=8),
        ft.ElevatedButton(
            "Criar Torneio",
            icon=ft.icons.CHECK_CIRCLE,
            bgcolor=ft.colors.AMBER,
            color=ft.colors.BLACK,
            on_click=criar,
        ),
        status,
    ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE, expand=True)
