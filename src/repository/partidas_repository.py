from src.database.connection_factory import ConnectionFactory


def salvar_tabela(tabela: list, id_torneio: int, map_nome_id: dict):
    """Persiste a tabela gerada pelo PartidasLogic no banco."""
    conn = ConnectionFactory.get_connection()
    if not conn:
        raise RuntimeError("Sem conexão com o banco.")
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM Partidas WHERE ID_Torneio=%s", (id_torneio,))
            for jogo in tabela:
                id_mand = map_nome_id[jogo["casa"]]
                id_vis  = map_nome_id[jogo["fora"]]
                cur.execute(
                    "INSERT INTO Partidas (Rodada, ID_Torneio, ID_Time_Mandante, ID_Time_Visitante) VALUES (%s,%s,%s,%s)",
                    (jogo["rodada"], id_torneio, id_mand, id_vis)
                )
        conn.commit()
    finally:
        conn.close()


def listar_rodadas(id_torneio: int) -> list:
    conn = ConnectionFactory.get_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT Rodada FROM Partidas WHERE ID_Torneio=%s ORDER BY Rodada",
                (id_torneio,)
            )
            return [r[0] for r in cur.fetchall()]
    finally:
        conn.close()


def partidas_da_rodada(id_torneio: int, rodada: int) -> list:
    conn = ConnectionFactory.get_connection()
    if not conn:
        return []
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT p.ID_Partida   AS id_partida,
                       p.Rodada       AS rodada,
                       p.Finalizada   AS finalizada,
                       p.Gols_M       AS gols_m,
                       p.Gols_V       AS gols_v,
                       tc.Nome        AS casa,
                       tf.Nome        AS fora
                FROM Partidas p
                JOIN Time tc ON tc.ID_Time = p.ID_Time_Mandante
                JOIN Time tf ON tf.ID_Time = p.ID_Time_Visitante
                WHERE p.ID_Torneio=%s AND p.Rodada=%s
                ORDER BY p.ID_Partida
            """, (id_torneio, rodada))
            colunas = [desc[0] for desc in cur.description]
            return [dict(zip(colunas, row)) for row in cur.fetchall()]
    finally:
        conn.close()


def registrar_resultado(id_partida: int, gols_casa: int, gols_fora: int) -> bool:
    """
    Atualiza o placar de uma partida.
    A classificação é recalculada automaticamente pela View_classificacao_geral.
    """
    conn = ConnectionFactory.get_connection()
    if not conn:
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT Finalizada FROM Partidas WHERE ID_Partida=%s",
                (id_partida,)
            )
            row = cur.fetchone()
            if not row or row[0]:  # não encontrada ou já finalizada
                return False

            cur.execute(
                "UPDATE Partidas SET Gols_M=%s, Gols_V=%s, Finalizada=TRUE WHERE ID_Partida=%s",
                (gols_casa, gols_fora, id_partida)
            )
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao registrar resultado: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
