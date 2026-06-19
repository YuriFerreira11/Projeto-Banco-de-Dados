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
                    "SELECT ID_Jogador, Nome, Funcao FROM Jogador WHERE ID_Time = %s ORDER BY Funcao ASC, Nome ASC",
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
    def atualizar_jogador(id_jogador, nome, funcao):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE Jogador SET Nome=%s, Funcao=%s WHERE ID_Jogador=%s",
                    (nome, funcao, id_jogador)
                )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def deletar_jogador(id_jogador):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return False
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Jogador WHERE ID_Jogador=%s", (id_jogador,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()