from src.database.connection_factory import ConnectionFactory
from types import SimpleNamespace


class DBQueries:

    @staticmethod
    def get_torneios():
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT ID_Torneio, Nome, Data_Inicio, Data_Fim FROM Torneio")
                colunas = [desc[0].lower() for desc in cursor.description]
                rows = cursor.fetchall()
                return [SimpleNamespace(**dict(zip(colunas, row))) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_todos_times():
        """Busca todos os times cadastrados, independente de torneio ou partidas."""
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT ID_Time, Nome, Escudo FROM Time ORDER BY Nome")
                rows = cursor.fetchall()
                return [SimpleNamespace(id_time=r[0], nome=r[1], escudo=r[2]) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_times_por_torneio(id_torneio):
        """Busca times inscritos no torneio via Torneio_Time."""
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT t.ID_Time, t.Nome, t.Escudo
                    FROM Time t
                    JOIN Torneio_Time tt ON tt.ID_Time = t.ID_Time
                    WHERE tt.ID_Torneio = %s
                    ORDER BY t.Nome
                """, (id_torneio,))
                rows = cursor.fetchall()
                return [SimpleNamespace(id_time=r[0], nome=r[1], escudo=r[2]) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_times_por_torneio_direto(id_torneio):
        """Alias de get_times_por_torneio, usado na geração da tabela."""
        return DBQueries.get_times_por_torneio(id_torneio)

    @staticmethod
    def get_classificacao_completa(id_torneio):
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT * FROM View_classificacao_geral
                    WHERE id_torneio = %s
                    ORDER BY pontos DESC, saldo_gols DESC
                """
                cursor.execute(query, (id_torneio,))
                colunas = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                return [SimpleNamespace(**dict(zip(colunas, row))) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_partidas(id_torneio):
        """Busca todas as partidas do torneio."""
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT p.ID_Partida,
                           p.Data_Hora as data_hora,
                           p.Local as local,
                           p.Gols_M as gols_m,
                           p.Gols_V as gols_v,
                           t1.Nome   as nome_mandante,
                           t1.Escudo as escudo_mandante,
                           t2.Nome   as nome_visitante,
                           t2.Escudo as escudo_visitante
                    FROM Partidas p
                    JOIN Time t1 ON p.ID_Time_Mandante = t1.ID_Time
                    JOIN Time t2 ON p.ID_Time_Visitante = t2.ID_Time
                    WHERE p.ID_Torneio = %s
                    ORDER BY p.Rodada, p.ID_Partida
                """
                cursor.execute(query, (id_torneio,))
                colunas = [desc[0].lower() for desc in cursor.description]
                rows = cursor.fetchall()
                return [SimpleNamespace(**dict(zip(colunas, row))) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_partidas_por_rodada(id_torneio, rodada):
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT p.ID_Partida,
                           p.Data_Hora as data_hora,
                           p.Local as local,
                           p.Gols_M as gols_m,
                           p.Gols_V as gols_v,
                           p.Finalizada,
                           t1.Nome   as nome_mandante,
                           t1.Escudo as escudo_mandante,
                           t2.Nome   as nome_visitante,
                           t2.Escudo as escudo_visitante
                    FROM Partidas p
                    JOIN Time t1 ON p.ID_Time_Mandante = t1.ID_Time
                    JOIN Time t2 ON p.ID_Time_Visitante = t2.ID_Time
                    WHERE p.ID_Torneio = %s AND p.Rodada = %s
                    ORDER BY p.ID_Partida
                """
                cursor.execute(query, (id_torneio, rodada))
                colunas = [desc[0].lower() for desc in cursor.description]
                rows = cursor.fetchall()
                return [SimpleNamespace(**dict(zip(colunas, row))) for row in rows]
        finally:
            conn.close()

    @staticmethod
    def get_times():
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT ID_Time, Nome, Escudo FROM Time ORDER BY Nome")
                rows = cursor.fetchall()
                return [SimpleNamespace(id_time=r[0], nome=r[1], escudo=r[2]) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_jogadores_por_time(id_time):
        conn = ConnectionFactory.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT ID_Jogador, CPF, Nome, Funcao FROM Jogador WHERE ID_Time = %s",
                    (id_time,)
                )
                rows = cursor.fetchall()
                return [SimpleNamespace(id_jogador=r[0], cpf=r[1], nome=r[2], funcao=r[3]) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_detalhes_temporada(nome_time):
        conn = ConnectionFactory.get_connection()
        if not conn:
            return SimpleNamespace(posicao="-", pontos=0, vitorias=0, empates=0,
                                   derrotas=0, gf=0, gs=0, saldo_gols=0)
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT posicao, pontos, vitorias, empates, derrotas, gf, gs, saldo_gols
                    FROM View_classificacao_geral WHERE nome_time = %s
                    LIMIT 1
                """
                cursor.execute(query, (nome_time,))
                row = cursor.fetchone()
                if row:
                    return SimpleNamespace(posicao=row[0], pontos=row[1],
                                           vitorias=row[2], empates=row[3],
                                           derrotas=row[4], gf=row[5],
                                           gs=row[6], saldo_gols=row[7])
                return SimpleNamespace(posicao="-", pontos=0, vitorias=0, empates=0,
                                       derrotas=0, gf=0, gs=0, saldo_gols=0)
        finally:
            conn.close()
