import psycopg2

class ConnectionFactory:
    @staticmethod
    def get_connection():
        try:
            return psycopg2.connect(
                host="100.125.6.3",     # Use o IP do YAML que é mais garantido
                database="torneio_bd1",
                user="admin",           # Se falhar com admin, tente "postgres"
                password="220400",      # CORRIGIDO: Era 22040 no seu código
                port="5432"
            )
        except Exception as e:
            print(f"Erro de conexão: {e}")
            return None