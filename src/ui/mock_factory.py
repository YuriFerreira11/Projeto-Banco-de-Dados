from datetime import datetime
from src.model.Time import Time
from src.model.Jogador import Jogador
from src.model.Partidas import Partidas
from src.model.Torneio import Torneio

class MockFactory:
    @staticmethod
    def get_times():
        return [
            Time(1, "Flamengo", "🔴⚫"),
            Time(2, "Palmeiras", "🟢⚪"),
            Time(3, "São Paulo", "🔴⚪⚫"),
            Time(4, "Cruzeiro", "🔵⚪"),
            Time(5, "Atlético-MG", "⚫⚪"),
        ]

    @staticmethod
    def get_jogadores():
        times = MockFactory.get_times()
        jogadores = []
        # Criando 5 jogadores para cada time
        for t in times:
            for i in range(1, 6):
                jogadores.append(Jogador(
                    id_jogador=len(jogadores)+1, 
                    cpf=f"123.456.78{len(jogadores)}", 
                    nome=f"Jogador {i} do {t.nome}", 
                    funcao="Atacante" if i == 1 else "Defesa", 
                    id_time=t.id_time
                ))
        return jogadores

    @staticmethod
    def get_partidas():
        return [
            Partidas(1, datetime.now(), "Maracanã", 1, 1, 2, 2, 0), # Fla 2 x 0 Pal
            Partidas(2, datetime.now(), "Mineirão", 1, 4, 5, 1, 1), # Cru 1 x 1 Galo
        ]