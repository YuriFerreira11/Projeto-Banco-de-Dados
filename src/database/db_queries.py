from src.database.connection_factory import ConnectionFactory
from types import SimpleNamespace

class DBQueries:
    @staticmethod
    def get_times():
        conn = ConnectionFactory.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT ID_Time, Nome, Escudo FROM Time")
                rows = cursor.fetchall()
                # Retorna lista de objetos com atributos id_time, nome, escudo
                return [SimpleNamespace(id_time=r[0], nome=r[1], escudo=r[2]) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_jogadores():
        conn = ConnectionFactory.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT ID_Jogador, CPF, Nome, Funcao, ID_Time FROM Jogador")
                rows = cursor.fetchall()
                return [SimpleNamespace(id_jogador=r[0], cpf=r[1], nome=r[2], funcao=r[3], id_time=r[4]) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_jogadores_por_time(id_time):
        conn = ConnectionFactory.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT ID_Jogador, CPF, Nome, Funcao FROM Jogador WHERE ID_Time = %s", (id_time,))
                rows = cursor.fetchall()
                return [SimpleNamespace(id_jogador=r[0], cpf=r[1], nome=r[2], funcao=r[3]) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_detalhes_temporada(nome_time):
        conn = ConnectionFactory.get_connection()
        try:
            with conn.cursor() as cursor:
                # Adicionei 'posicao' no início da SELECT
                query = """
                        SELECT posicao, \
                               pontos, \
                               vitorias, \
                               empates, \
                               derrotas, \
                               gf, \
                               gs, \
                               saldo_gols
                        FROM View_classificacao_geral \
                        WHERE nome_time = %s \
                        """
                cursor.execute(query, (nome_time,))
                row = cursor.fetchone()
                if row:
                    return SimpleNamespace(
                        posicao=row[0], pontos=row[1], vitorias=row[2], empates=row[3],
                        derrotas=row[4], gf=row[5], gs=row[6], saldo_gols=row[7]
                    )
                return SimpleNamespace(posicao="-", pontos=0, vitorias=0, empates=0, derrotas=0, gf=0, gs=0,
                                       saldo_gols=0)
        finally:
            conn.close()

    @staticmethod
    def get_classificacao_completa():
        conn = ConnectionFactory.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM View_classificacao_geral ORDER BY pontos DESC, saldo_gols DESC")
                colunas = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                # Cria objetos dinâmicos baseados nos nomes das colunas da VIEW
                return [SimpleNamespace(**dict(zip(colunas, row))) for row in rows]
        finally:
            conn.close()