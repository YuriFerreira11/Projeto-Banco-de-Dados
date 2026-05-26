import random


class PartidasLogic:

    @staticmethod
    def gerar_tabela_simples_e_segura(times_reais: list[str]) -> list[dict]:
        n = len(times_reais)
        if n % 2 != 0:
            raise ValueError("O número de times deve ser par.")

        times = list(times_reais)
        random.shuffle(times)

        turno = []
        rodadas_turno = n - 1

        # TURNO
        for r in range(rodadas_turno):
            for i in range(n // 2):
                if i == 0:
                    casa, fora = (r, n - 1) if r % 2 == 0 else (n - 1, r)
                else:
                    t1, t2 = (r + i) % (n - 1), (n - 1 - i + r) % (n - 1)
                    casa, fora = (t1, t2) if i % 2 == 1 else (t2, t1)

                turno.append({
                    "rodada": r + 1,
                    "casa": times[casa],
                    "fora": times[fora]
                })

        # RETURNO
        returno = []
        for jogo in turno:
            returno.append({
                "rodada": jogo["rodada"] + rodadas_turno,
                "casa": jogo["fora"],
                "fora": jogo["casa"]
            })

        return turno + returno

    @staticmethod
    def imprimir_tabela(tabela: list[dict]):
        rodada_atual = None
        for jogo in tabela:
            if jogo["rodada"] != rodada_atual:
                rodada_atual = jogo["rodada"]
                print(f"\n--- Rodada {rodada_atual} ---")
            print(f"{jogo['casa']} x {jogo['fora']}")