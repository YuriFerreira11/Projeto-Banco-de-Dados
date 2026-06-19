from types import SimpleNamespace
from src.database.connection_factory import ConnectionFactory


class TorneioRepository:

    @staticmethod
    def get_torneios():
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT ID_Torneio, Nome, Data_Inicio, Data_Fim FROM Torneio")
                colunas = [desc[0].lower() for desc in cur.description]
                return [SimpleNamespace(**dict(zip(colunas, row))) for row in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_classificacao_completa(id_torneio):
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM View_classificacao_geral
                    WHERE id_torneio = %s
                    ORDER BY pontos DESC, saldo_gols DESC
                """, (id_torneio,))
                colunas = [desc[0] for desc in cur.description]
                return [SimpleNamespace(**dict(zip(colunas, row))) for row in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def criar_torneio(nome, data_inicio, data_fim):
        conn = ConnectionFactory.get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO Torneio (Nome, Data_Inicio, Data_Fim) VALUES (%s, %s, %s) RETURNING ID_Torneio",
                    (nome, data_inicio or None, data_fim or None)
                )
                id_torneio = cur.fetchone()[0]
            conn.commit()
            return id_torneio
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def vincular_time(id_torneio, id_time):
        conn = ConnectionFactory.get_connection()
        if not conn: return
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO Torneio_Time (ID_Torneio, ID_Time) VALUES (%s, %s)",
                    (id_torneio, id_time)
                )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    @staticmethod
    def obter_senha_admin():
        conn = ConnectionFactory.get_connection()
        if not conn:
            return None

        try:
            with conn.cursor() as cur:
                # Busca a senha na tabela 'admin' onde o id_admin é igual a 1
                cur.execute(
                    "SELECT senha FROM admin WHERE id_admin = %s LIMIT 1",
                    (1,)
                )

                resultado = cur.fetchone()

                if resultado:
                    return resultado[0]  # Retorna "senha123"
                else:
                    return None  # Caso não exista nenhum admin com ID 1

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # Substituindo a sua variável antiga pelo dado dinâmico do banco:
    ADMIN_SENHA = obter_senha_admin()
