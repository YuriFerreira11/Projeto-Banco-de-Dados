import psycopg2
from src.config.settings import DATABASE_CONFIG


class ConnectionFactory:
    @staticmethod
    def get_connection():
        try:
            return psycopg2.connect(
                host=DATABASE_CONFIG["host"],
                database=DATABASE_CONFIG["dbname"],
                user=DATABASE_CONFIG["user"],
                password=str(DATABASE_CONFIG["password"]),
                port=DATABASE_CONFIG["port"]
            )
        except Exception as e:
            print(f"Erro de conexão com o Banco de Dados: {e}")
            return None
