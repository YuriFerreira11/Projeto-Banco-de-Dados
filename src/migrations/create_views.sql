-- 1. Classificação Geral
-- Só conta partidas FINALIZADAS (Finalizada = TRUE)
-- Times sem partidas finalizadas não aparecem (LEFT JOIN via Torneio_Time)
CREATE OR REPLACE VIEW View_classificacao_geral AS
SELECT
    tt.id_torneio,
    t.nome        AS nome_time,
    t.escudo,
    ROW_NUMBER() OVER (
        PARTITION BY tt.id_torneio
        ORDER BY
            COALESCE(SUM(CASE
                WHEN (t.id_time = p.id_time_mandante AND p.gols_m > p.gols_v) OR
                     (t.id_time = p.id_time_visitante AND p.gols_v > p.gols_m) THEN 3
                WHEN p.gols_m = p.gols_v THEN 1
                ELSE 0
            END), 0) DESC,
            COALESCE(SUM(CASE
                WHEN t.id_time = p.id_time_mandante THEN p.gols_m - p.gols_v
                ELSE p.gols_v - p.gols_m
            END), 0) DESC
    ) AS posicao,
    COALESCE(SUM(CASE
        WHEN (t.id_time = p.id_time_mandante AND p.gols_m > p.gols_v) OR
             (t.id_time = p.id_time_visitante AND p.gols_v > p.gols_m) THEN 3
        WHEN p.gols_m = p.gols_v THEN 1
        ELSE 0
    END), 0) AS pontos,
    COUNT(p.id_partida)                                                           AS partidas_jogadas,
    COALESCE(SUM(CASE
        WHEN (t.id_time = p.id_time_mandante AND p.gols_m > p.gols_v) OR
             (t.id_time = p.id_time_visitante AND p.gols_v > p.gols_m) THEN 1
        ELSE 0
    END), 0) AS vitorias,
    COALESCE(SUM(CASE WHEN p.gols_m = p.gols_v THEN 1 ELSE 0 END), 0)           AS empates,
    COALESCE(SUM(CASE
        WHEN (t.id_time = p.id_time_mandante AND p.gols_m < p.gols_v) OR
             (t.id_time = p.id_time_visitante AND p.gols_v < p.gols_m) THEN 1
        ELSE 0
    END), 0) AS derrotas,
    COALESCE(SUM(CASE WHEN t.id_time = p.id_time_mandante THEN p.gols_m ELSE p.gols_v END), 0) AS gf,
    COALESCE(SUM(CASE WHEN t.id_time = p.id_time_mandante THEN p.gols_v ELSE p.gols_m END), 0) AS gs,
    COALESCE(SUM(CASE
        WHEN t.id_time = p.id_time_mandante THEN p.gols_m - p.gols_v
        ELSE p.gols_v - p.gols_m
    END), 0) AS saldo_gols
FROM Torneio_Time tt
JOIN Time t ON t.id_time = tt.id_time
LEFT JOIN Partidas p
    ON p.id_torneio = tt.id_torneio
    AND (t.id_time = p.id_time_mandante OR t.id_time = p.id_time_visitante)
    AND p.finalizada = TRUE
GROUP BY tt.id_torneio, t.id_time, t.nome, t.escudo;


-- 2. Resultados e Agendamentos
CREATE OR REPLACE VIEW VIEW_RESULTADOS_E_AGENDAMENTOS AS
SELECT
    p.Data_Hora,
    p.Local,
    tm.Nome            AS Time_Mandante,
    p.Gols_M           AS Placar_Mandante,
    p.Gols_V           AS Placar_Visitante,
    tv.Nome            AS Time_Visitante,
    CASE
        WHEN p.Finalizada THEN 'Finalizada'
        ELSE 'Agendada'
    END AS Status
FROM Partidas p
JOIN Time tm ON p.ID_Time_Mandante = tm.ID_Time
JOIN Time tv ON p.ID_Time_Visitante = tv.ID_Time;


-- 3. Histórico Individual
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
CROSS JOIN VIEW_RESULTADOS_E_AGENDAMENTOS v
WHERE t.Nome = v.Time_Mandante OR t.Nome = v.Time_Visitante;
