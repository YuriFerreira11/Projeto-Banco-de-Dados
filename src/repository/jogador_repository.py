from types import SimpleNamespace
from src.database.connection_factory import ConnectionFactory


class JogadorRepository:

    @staticmethod
    def get_jogadores_por_time(id_time):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return []
        try:
            with conn.cursor() as cur:
                # Puxa 3 colunas: índice 0, 1 e 2
                cur.execute(
                    "SELECT ID_Jogador, Nome, Funcao FROM Jogador WHERE ID_Time = %s",
                    (id_time,)
                )
                # CORRIGIDO: Mapeamento direto sem a coluna CPF para evitar IndexError
                return [
                    SimpleNamespace(id_jogador=r[0], nome=r[1], funcao=r[2])
                    for r in cur.fetchall()
                ]
        finally:
            conn.close()

    @staticmethod
    def criar_jogador(nome, funcao, id_time):
        # CORRIGIDO: Removido o parâmetro 'cpf' da assinatura da função
        conn = ConnectionFactory.get_connection()
        if not conn:
            return
        try:
            with conn.cursor() as cur:
                # CORRIGIDO: Alinhado para 3 colunas e 3 placeholders (%s)
                cur.execute(
                    "INSERT INTO Jogador (Nome, Funcao, ID_Time) VALUES (%s, %s, %s)",
                    (nome, funcao, id_time)
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
        if not conn:
            return
        try:
            with conn.cursor() as cur:
                for pos, nome in zip(posicoes, nomes_base):
                    # CORRIGIDO: Removida a geração e inserção do CPF falso
                    cur.execute(
                        "INSERT INTO Jogador (Nome, Funcao, ID_Time) VALUES (%s, %s, %s)",
                        (f"{nome} ({nome_time[:8]})", pos, id_time)
                    )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()