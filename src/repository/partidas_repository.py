from database.connection_factory import ConnectionFactory


class PartidasRepository:
    @staticmethod
    def salvar_rodadas(lista_jogos: list[dict], id_torneio: int):
        conn = ConnectionFactory.get_connection()
        try:
            cursor = conn.cursor()
            # Mapeamento de nomes para IDs para uso nas queries
            cursor.execute("SELECT id_time, nome FROM time")
            times_db = {nome: id_t for id_t, nome in cursor.fetchall()}

            sql = """
                  INSERT INTO Partidas (Data_Hora, ID_Torneio, ID_Time_Mandante, ID_Time_Visitante)
                  VALUES (%s, %s, %s, %s) \
                  """

            for jogo in lista_jogos:
                # Ajustar a data conforme necessidade do seu sistema
                data_padrao = "2026-06-01 15:00:00"

                cursor.execute(sql, (
                    data_padrao,
                    id_torneio,
                    times_db[jogo['casa']],
                    times_db[jogo['fora']]
                ))

            conn.commit()
            return True, "Rodadas inseridas com sucesso."
        except Exception as e:
            conn.rollback()
            return False, f"Erro ao inserir rodadas: {e}"
        finally:
            cursor.close()
            conn.close()