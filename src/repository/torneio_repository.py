from src.database.connection_factory import ConnectionFactory
from src.model import Torneio as Torneio
class TorneioRepository:


    @classmethod
    def criar_torneio(cls, torneio: Torneio):
        conn = ConnectionFactory.get_connection()
        try:
            cursor = conn.cursor()
            # O SQL deve retornar o ID criado
            sql = "INSERT INTO torneio (nome, data_inicio, data_fim) VALUES (%s, %s, %s) RETURNING id_torneio"
            valores = (torneio.nome, torneio.data_inicio, torneio.data_fim)
            cursor.execute(sql, valores)

            id_gerado = cursor.fetchone()[0]  # Captura o valor do RETURNING
            conn.commit()
            return True, id_gerado  # Retorna o ID aqui
        except Exception as e:
            conn.rollback()
            return False, str(e)
        finally:
            cursor.close()
            conn.close()
