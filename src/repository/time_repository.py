from types import SimpleNamespace
from database.connection_factory import ConnectionFactory


class TimeRepository:

    @staticmethod
    def get_todos_times():
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT ID_Time, Nome, Escudo FROM Time ORDER BY Nome")
                return [SimpleNamespace(id_time=r[0], nome=r[1], escudo=r[2]) for r in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_times_por_torneio(id_torneio):
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT t.ID_Time, t.Nome, t.Escudo
                    FROM Time t
                    JOIN Torneio_Time tt ON tt.ID_Time = t.ID_Time
                    WHERE tt.ID_Torneio = %s
                    ORDER BY t.Nome
                """, (id_torneio,))
                return [SimpleNamespace(id_time=r[0], nome=r[1], escudo=r[2]) for r in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_detalhes_temporada(nome_time):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return SimpleNamespace(posicao="-", pontos=0, vitorias=0, empates=0,
                                   derrotas=0, gf=0, gs=0, saldo_gols=0)
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT posicao, pontos, vitorias, empates, derrotas, gf, gs, saldo_gols
                    FROM View_classificacao_geral WHERE nome_time = %s
                    LIMIT 1
                """, (nome_time,))
                row = cur.fetchone()
                if row:
                    return SimpleNamespace(posicao=row[0], pontos=row[1], vitorias=row[2],
                                           empates=row[3], derrotas=row[4], gf=row[5],
                                           gs=row[6], saldo_gols=row[7])
                return SimpleNamespace(posicao="-", pontos=0, vitorias=0, empates=0,
                                       derrotas=0, gf=0, gs=0, saldo_gols=0)
        finally:
            conn.close()

    @staticmethod
    def criar_time(nome, escudo):
        conn = ConnectionFactory.get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO Time (Nome, Escudo) VALUES (%s, %s) RETURNING ID_Time",
                    (nome, escudo or None)
                )
                id_time = cur.fetchone()[0]
            conn.commit()
            return id_time
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
