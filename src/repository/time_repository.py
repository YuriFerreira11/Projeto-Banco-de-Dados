from database.connection_factory import ConnectionFactory
from model.Time import Time
class TimeRepository:

    @classmethod
    def insert_time(cls, time: Time):
        conn = ConnectionFactory.get_connection()
        try:
            cursor = conn.cursor()
            sql = """
                INSERT INTO time(nome, logo)
                VALUES(%s, %s)
            """
            valores = (time.nome,time.logo)
            cursor.execute(sql, valores)
            conn.commit()
            return True, "Time salvo com sucesso"
        except Exception as e:
            return False, f"Erro ao salvar time: {e}"
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def return_name_time(cls) -> list[tuple]:
        conn = ConnectionFactory.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT t.nome FROM time t')
            return [row[0] for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
    def remover_time(time: Time):
        conn = ConnectionFactory.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM time WHERE nome = %s', (time.nome,))
            conn.commit()
            return True, "Time removido com sucesso"
        except Exception as e:
            return False, f"Erro ao remover time: {e}"
        finally:
            cursor.close()
            conn.close()