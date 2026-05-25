from src.database.ConnectionFactory import ConnectionFactory
from src.model.Time import Time


class DBQueries:
    """
    Esta classe centraliza todas as consultas de busca (SELECT) do banco de dados.
    Os dados reais da interface virão daqui ao invés do MockFactory.
    """

    @staticmethod
    def get_times():
        conn = ConnectionFactory.get_connection()
        if not conn:
            print("Erro: Não foi possível conectar ao banco para buscar times.")
            return []

        try:
            with conn.cursor() as cursor:
                # Busca os dados reais na tabela física 'TIME'
                cursor.execute("SELECT id_time, nome, escudo FROM TIME ORDER BY nome")
                rows = cursor.fetchall()

                # Mapeia as linhas do banco para objetos da classe Time
                return [Time(id_time=r[0], nome=r[1], escudo=r[2]) for r in rows]
        except Exception as e:
            print(f"Erro na query get_times: {e}")
            return []
        finally:
            conn.close()