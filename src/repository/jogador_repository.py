from database.connection_factory import ConnectionFactory
from model.Jogador import Jogador

class JogadorRepository:
    @classmethod
    def criar_jogador(cls, jogador: Jogador):
        conn = ConnectionFactory.get_connection()
        try:
            cursor = conn.cursor()
            sql = """
            INSERT INTO jogador (cpf, nome, funcao, id_time) 
            VALUES (%s, %s, %s, %s)
            """
            valores = (jogador.cpf, jogador.nome, jogador.funcao, jogador.id_time)
            cursor.execute(sql, valores)
            conn.commit()
            return True, "Jogador criado com sucesso!"
        except Exception as e:
            return False, f"Erro ao salvar jogador: {e}"
        finally:
            cursor.close()
            conn.close()
