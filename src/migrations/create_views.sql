-- 1. Classificação
CREATE OR REPLACE VIEW VIEW_CLASSIFICACAO_GERAL AS
WITH Pontuacao_Consolidada AS (
    -- Dados como Mandante
    SELECT
        ID_Time_Mandante AS ID_Time,
        CASE
            WHEN Gols_M > Gols_V THEN 3
            WHEN Gols_M = Gols_V THEN 1
            ELSE 0
        END AS Pontos,
        CASE WHEN Gols_M > Gols_V THEN 1 ELSE 0 END AS Vitoria,
        CASE WHEN Gols_M = Gols_V THEN 1 ELSE 0 END AS Empate,
        CASE WHEN Gols_M < Gols_V THEN 1 ELSE 0 END AS Derrota,
        Gols_M AS Gols_Feitos,
        Gols_V AS Gols_Sofridos
    FROM Partidas

    UNION ALL

    -- Dados como Visitante
    SELECT
        ID_Time_Visitante AS ID_Time,
        CASE
            WHEN Gols_V > Gols_M THEN 3
            WHEN Gols_V = Gols_M THEN 1
            ELSE 0
        END AS Pontos,
        CASE WHEN Gols_V > Gols_M THEN 1 ELSE 0 END AS Vitoria,
        CASE WHEN Gols_V = Gols_M THEN 1 ELSE 0 END AS Empate,
        CASE WHEN Gols_V < Gols_M THEN 1 ELSE 0 END AS Derrota,
        Gols_V AS Gols_Feitos,
        Gols_M AS Gols_Sofridos
    FROM Partidas
)
SELECT
    t.Nome AS Nome_Time,
    COALESCE(SUM(p.Pontos), 0) AS Pontos,
    COALESCE(SUM(p.Vitoria), 0) AS Vitorias,
    COALESCE(SUM(p.Empate), 0) AS Empates,
    COALESCE(SUM(p.Derrota), 0) AS Derrotas,
    COALESCE(SUM(p.Gols_Feitos), 0) AS GF,
    COALESCE(SUM(p.Gols_Sofridos), 0) AS GS,
    COALESCE(SUM(p.Gols_Feitos), 0) - COALESCE(SUM(p.Gols_Sofridos), 0) AS Saldo_Gols
FROM Time t
LEFT JOIN Pontuacao_Consolidada p ON t.ID_Time = p.ID_Time
GROUP BY t.ID_Time, t.Nome
ORDER BY Pontos DESC, Vitorias DESC, Saldo_Gols DESC;


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