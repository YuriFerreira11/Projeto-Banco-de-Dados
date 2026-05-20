import psycopg2
from psycopg2 import Error
from src.Config.settings import DATABASE_CONFIG
class ConnectionFactory:

    @classmethod
    def get_connection(cls):
        try:
            return psycopg2.connect(**DATABASE_CONFIG)
        except Error as e:
            print(f" [❌] Erro ao conectar ao PostgreSQL: {e}")
            return None
        except Exception as e:
            print(f" [❌] Erro de configuração: {e}")
            return None