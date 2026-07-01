-- =============================================================================
-- 1. CLASSIFICAÇÃO GERAL
-- =============================================================================
CREATE OR REPLACE VIEW View_Classificacao_Geral AS
SELECT
    tt.ID_Torneio,
    t.Nome AS Nome_Time,
    t.Escudo,
    ROW_NUMBER() OVER (
        PARTITION BY tt.ID_Torneio
        ORDER BY
            COALESCE(SUM(CASE
                WHEN (t.ID_Time = p.ID_Time_Mandante AND p.Gols_M > p.Gols_V) OR
                     (t.ID_Time = p.ID_Time_Visitante AND p.Gols_V > p.Gols_M) THEN 3
                WHEN p.Gols_M = p.Gols_V THEN 1
                ELSE 0
            END), 0) DESC,
            COALESCE(SUM(CASE
                WHEN t.ID_Time = p.ID_Time_Mandante THEN p.Gols_M - p.Gols_V
                ELSE p.Gols_V - p.Gols_M
            END), 0) DESC
    ) AS Posicao,
    COALESCE(SUM(CASE
        WHEN (t.ID_Time = p.ID_Time_Mandante AND p.Gols_M > p.Gols_V) OR
             (t.ID_Time = p.ID_Time_Visitante AND p.Gols_V > p.Gols_M) THEN 3
        WHEN p.Gols_M = p.Gols_V THEN 1
        ELSE 0
    END), 0) AS Pontos,
    COUNT(p.ID_Partida) AS Partidas_Jogadas,
    COALESCE(SUM(CASE
        WHEN (t.ID_Time = p.ID_Time_Mandante AND p.Gols_M > p.Gols_V) OR
             (t.ID_Time = p.ID_Time_Visitante AND p.Gols_V > p.Gols_M) THEN 1
        ELSE 0
    END), 0) AS Vitorias,
    COALESCE(SUM(CASE WHEN p.Gols_M = p.Gols_V THEN 1 ELSE 0 END), 0) AS Empates,
    COALESCE(SUM(CASE
        WHEN (t.ID_Time = p.ID_Time_Mandante AND p.Gols_M < p.Gols_V) OR
             (t.ID_Time = p.ID_Time_Visitante AND p.Gols_V < p.Gols_M) THEN 1
        ELSE 0
    END), 0) AS Derrotas,
    COALESCE(SUM(CASE WHEN t.ID_Time = p.ID_Time_Mandante THEN p.Gols_M ELSE p.Gols_V END), 0) AS GF,
    COALESCE(SUM(CASE WHEN t.ID_Time = p.ID_Time_Mandante THEN p.Gols_V ELSE p.Gols_M END), 0) AS GS,
    COALESCE(SUM(CASE
        WHEN t.ID_Time = p.ID_Time_Mandante THEN p.Gols_M - p.Gols_V
        ELSE p.Gols_V - p.Gols_M
    END), 0) AS Saldo_Gols
FROM Torneio_Time tt
JOIN Time t ON t.ID_Time = tt.ID_Time
LEFT JOIN Partidas p
    ON p.ID_Torneio = tt.ID_Torneio
    AND (t.ID_Time = p.ID_Time_Mandante OR t.ID_Time = p.ID_Time_Visitante)
    AND p.Finalizada = TRUE
GROUP BY tt.ID_Torneio, t.ID_Time, t.Nome, t.Escudo;

-- =============================================================================
-- 2. RESULTADOS E AGENDAMENTOS
-- =============================================================================
CREATE OR REPLACE VIEW VIEW_RESULTADOS_E_AGENDAMENTOS AS
SELECT
    p.Data_Hora,
    p.Local,
    tm.Nome AS Time_Mandante,
    p.Gols_M AS Placar_Mandante,
    p.Gols_V AS Placar_Visitante,
    tv.Nome AS Time_Visitante,
    CASE
        WHEN p.Finalizada THEN 'Finalizada'
        ELSE 'Agendada'
    END AS Status
FROM Partidas p
JOIN Time tm ON p.ID_Time_Mandante = tm.ID_Time
JOIN Time tv ON p.ID_Time_Visitante = tv.ID_Time;

-- =============================================================================
-- 3. HISTÓRICO INDIVIDUAL DO TIME
-- =============================================================================
CREATE OR REPLACE VIEW VIEW_HISTORICO_INDIVIDUAL_TIME AS
SELECT
    t.Nome AS Time_Pesquisado,
    v.Data_Hora,
    CASE WHEN t.Nome = v.Time_Mandante THEN v.Time_Visitante ELSE v.Time_Mandante END AS Adversario,
    CASE WHEN t.Nome = v.Time_Mandante THEN v.Placar_Mandante ELSE v.Placar_Visitante END AS Placar_Time,
    CASE WHEN t.Nome = v.Time_Mandante THEN v.Placar_Visitante ELSE v.Placar_Mandante END AS Placar_Adversario,
    CASE WHEN t.Nome = v.Time_Mandante THEN 'Mandante' ELSE 'Visitante' END AS Condicao,
    v.Status
FROM Time t
JOIN VIEW_RESULTADOS_E_AGENDAMENTOS v
    ON t.Nome = v.Time_Mandante OR t.Nome = v.Time_Visitante;