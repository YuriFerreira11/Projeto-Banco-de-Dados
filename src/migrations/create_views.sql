CREATE OR REPLACE VIEW View_classificacao_geral AS
SELECT
    p.id_torneio,      -- COLUNA FALTANTE ADICIONADA
    t.nome AS nome_time,
    t.escudo,
    -- Ranking fictício apenas para exemplo, ajuste conforme seu cálculo real:
    ROW_NUMBER() OVER(PARTITION BY p.id_torneio ORDER BY SUM(
        CASE
            WHEN (t.id_time = p.id_time_mandante AND p.gols_m > p.gols_v) OR
                 (t.id_time = p.id_time_visitante AND p.gols_v > p.gols_m) THEN 3
            WHEN p.gols_m = p.gols_v THEN 1
            ELSE 0
        END
    ) DESC) as posicao,
    SUM(
        CASE
            WHEN (t.id_time = p.id_time_mandante AND p.gols_m > p.gols_v) OR
                 (t.id_time = p.id_time_visitante AND p.gols_v > p.gols_m) THEN 3
            WHEN p.gols_m = p.gols_v THEN 1
            ELSE 0
        END
    ) AS pontos,
    COUNT(*) AS partidas_jogadas,
    SUM(CASE WHEN (t.id_time = p.id_time_mandante AND p.gols_m > p.gols_v) OR (t.id_time = p.id_time_visitante AND p.gols_v > p.gols_m) THEN 1 ELSE 0 END) AS vitorias,
    SUM(CASE WHEN p.gols_m = p.gols_v THEN 1 ELSE 0 END) AS empates,
    SUM(CASE WHEN (t.id_time = p.id_time_mandante AND p.gols_m < p.gols_v) OR (t.id_time = p.id_time_visitante AND p.gols_v < p.gols_m) THEN 1 ELSE 0 END) AS derrotas,
    SUM(CASE WHEN t.id_time = p.id_time_mandante THEN p.gols_m ELSE p.gols_v END) AS gf,
    SUM(CASE WHEN t.id_time = p.id_time_mandante THEN p.gols_v ELSE p.gols_m END) AS gs,
    SUM(CASE WHEN t.id_time = p.id_time_mandante THEN p.gols_m - p.gols_v ELSE p.gols_v - p.gols_m END) AS saldo_gols
FROM Time t
JOIN Partidas p ON (t.id_time = p.id_time_mandante OR t.id_time = p.id_time_visitante)
GROUP BY p.id_torneio, t.id_time, t.nome, t.escudo;


-- 2. Resultados e Agendamentos
CREATE OR REPLACE VIEW VIEW_RESULTADOS_E_AGENDAMENTOS AS
SELECT
    p.Data_Hora,
    p.Local,
    tm.Nome AS Time_Mandante,
    p.Gols_M AS Placar_Mandante,
    p.Gols_V AS Placar_Visitante,
    tv.Nome AS Time_Visitante,
    CASE
        WHEN p.Data_Hora < CURRENT_TIMESTAMP THEN 'Finalizada'
        ELSE 'Agendada'
    END AS Status
FROM Partidas p
INNER JOIN Time tm ON p.ID_Time_Mandante = tm.ID_Time
INNER JOIN Time tv ON p.ID_Time_Visitante = tv.ID_Time;


-- 3. Histórico Individual
CREATE OR REPLACE VIEW VIEW_HISTORICO_INDIVIDUAL_TIME AS
SELECT
    t.Nome AS Time_Pesquisado,
    v.Data_Hora,
    CASE
        WHEN t.Nome = v.Time_Mandante THEN v.Time_Visitante
        ELSE v.Time_Mandante
    END AS Adversario,
    CASE
        WHEN t.Nome = v.Time_Mandante THEN v.Placar_Mandante
        ELSE v.Placar_Visitante
    END AS Placar_Time,
    CASE
        WHEN t.Nome = v.Time_Mandante THEN v.Placar_Visitante
        ELSE v.Placar_Mandante
    END AS Placar_Adversario,
    CASE
        WHEN t.Nome = v.Time_Mandante THEN 'Mandante'
        ELSE 'Visitante'
    END AS Condicao,
    v.Status
FROM Time t
CROSS JOIN VIEW_RESULTADOS_E_AGENDAMENTOS v
WHERE t.Nome = v.Time_Mandante OR t.Nome = v.Time_Visitante;