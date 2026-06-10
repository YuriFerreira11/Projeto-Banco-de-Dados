from types import SimpleNamespace
from database.connection_factory import ConnectionFactory


class JogadorRepository:

    @staticmethod
    def get_jogadores_por_time(id_time):
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT ID_Jogador, CPF, Nome, Funcao FROM Jogador WHERE ID_Time = %s",
                    (id_time,)
                )
                return [SimpleNamespace(id_jogador=r[0], cpf=r[1], nome=r[2], funcao=r[3])
                        for r in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def criar_jogador(cpf, nome, funcao, id_time):
        conn = ConnectionFactory.get_connection()
        if not conn: return
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO Jogador (CPF, Nome, Funcao, ID_Time) VALUES (%s, %s, %s, %s)",
                    (cpf, nome, funcao, id_time)
                )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def gerar_jogadores_para_time(id_time, nome_time):
        """Gera 11 jogadores automaticamente para um time."""
        posicoes = ["Goleiro", "Zagueiro", "Zagueiro", "Zagueiro",
                    "Lateral", "Lateral", "Volante", "Meia",
                    "Meia", "Atacante", "Atacante"]
        nomes_base = ["Carlos", "Bruno", "Diego", "Felipe", "Gabriel",
                      "Henrique", "Igor", "João", "Lucas", "Mateus", "Rafael"]
        conn = ConnectionFactory.get_connection()
        if not conn: return
        try:
            with conn.cursor() as cur:
                for i, (pos, nome) in enumerate(zip(posicoes, nomes_base)):
                    cpf = str(id_time * 1000 + i + 1).zfill(11)
                    cur.execute(
                        "INSERT INTO Jogador (CPF, Nome, Funcao, ID_Time) VALUES (%s, %s, %s, %s)",
                        (cpf, f"{nome} ({nome_time[:8]})", pos, id_time)
                    )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
