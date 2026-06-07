"""
Lógica de geração de tabela (round-robin com turno e returno).
Integrada com o banco via partidas_repo.
"""
import random
from src.repository import partidas_repository as partidas_repo
from src.database.db_queries import DBQueries


class PartidasLogic:

    @staticmethod
    def gerar_tabela(times_reais: list) -> list:
        """Gera tabela round-robin (turno + returno)."""
        n = len(times_reais)
        if n < 2:
            raise ValueError("Mínimo de 2 times.")
        if n % 2 != 0:
            raise ValueError("Número de times deve ser par.")

        times = list(times_reais)
        random.shuffle(times)

        turno = []
        rodadas_turno = n - 1

        for r in range(rodadas_turno):
            for i in range(n // 2):
                if i == 0:
                    casa, fora = (r, n - 1) if r % 2 == 0 else (n - 1, r)
                else:
                    t1 = (r + i) % (n - 1)
                    t2 = (n - 1 - i + r) % (n - 1)
                    casa, fora = (t1, t2) if i % 2 == 1 else (t2, t1)
                turno.append({
                    "rodada": r + 1,
                    "casa": times[casa],
                    "fora": times[fora]
                })

        returno = [{
            "rodada": j["rodada"] + rodadas_turno,
            "casa": j["fora"],
            "fora": j["casa"]
        } for j in turno]

        return turno + returno

    @staticmethod
    def gerar_e_salvar(id_torneio: int) -> int:
        """Gera a tabela e persiste no banco. Retorna total de jogos."""
        times = DBQueries.get_times_por_torneio_direto(id_torneio)
        if len(times) < 2:
            raise ValueError("Adicione pelo menos 2 times.")
        if len(times) % 2 != 0:
            raise ValueError("Adicione um número par de times.")

        nomes = [t.nome for t in times]
        map_nome_id = {t.nome: t.id_time for t in times}

        tabela = PartidasLogic.gerar_tabela(nomes)
        partidas_repo.salvar_tabela(tabela, id_torneio, map_nome_id)
        return len(tabela)
