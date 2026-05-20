-- 1. VIEW_ARTILHARIA_E_GARCOM
-- Agrupa estatísticas por jogador para listar gols e assistências em ordem decrescente.
CREATE OR REPLACE VIEW VIEW_ARTILHARIA_E_GARCOM AS
SELECT
    j.Nome AS Nome_Jogador,
    t.Nome AS Nome_Time,
    COALESCE(SUM(ep.Gols), 0) AS Gols_Marcados,
    COALESCE(SUM(ep.Assistencias), 0) AS Assistencias
FROM JOGADOR j
INNER JOIN TIME t ON j.ID_Time = t.ID_Time
LEFT JOIN ESTATISTICA_PARTIDA ep ON j.ID_Jogador = ep.ID_Jogador
GROUP BY j.ID_Jogador, j.Nome, t.Nome
ORDER BY Gols_Marcados DESC, Assistencias DESC;


-- 2. VIEW_CLASSIFICACAO_GERAL
-- Calcula as métricas clássicas de uma tabela de campeonato somando mandantes e visitantes.
CREATE OR REPLACE VIEW VIEW_CLASSIFICACAO_GERAL AS
WITH Gols_Por_Time_Na_Partida AS (
    -- Descobre o total de gols que cada TIME fez em cada PARTIDA
    SELECT
        ep.ID_Partida,
        j.ID_Time,
        COALESCE(SUM(ep.Gols), 0) AS Total_Gols
    FROM ESTATISTICA_PARTIDA ep
    INNER JOIN JOGADOR j ON ep.ID_Jogador = j.ID_Jogador
    GROUP BY ep.ID_Partida, j.ID_Time
),
Dados_Partidas_Consolidados AS (
    -- Junta os dados da partida com os gols calculados de cada lado
    SELECT
        p.ID_Partida,
        p.ID_Time_Mandante,
        p.ID_Time_Visitante,
        COALESCE(gm.Total_Gols, 0) AS Gols_Mandante,
        COALESCE(gv.Total_Gols, 0) AS Gols_Visitante
    FROM PARTIDAS p
    LEFT JOIN Gols_Por_Time_Na_Partida gm ON p.ID_Partida = gm.ID_Partida AND p.ID_Time_Mandante = gm.ID_Time
    LEFT JOIN Gols_Por_Time_Na_Partida gv ON p.ID_Partida = gv.ID_Partida AND p.ID_Time_Visitante = gv.ID_Time
),
Pontuacao_Partidas AS (
    -- Calcula os pontos, vitórias, empates, derrotas e gols como MANDANTE
    SELECT
        ID_Time_Mandante AS ID_Time,
        CASE
            WHEN Gols_Mandante > Gols_Visitante THEN 3
            WHEN Gols_Mandante = Gols_Visitante THEN 1
            ELSE 0
        END AS Pontos,
        CASE WHEN Gols_Mandante > Gols_Visitante THEN 1 ELSE 0 END AS Vitoria,
        CASE WHEN Gols_Mandante = Gols_Visitante THEN 1 ELSE 0 END AS Empate,
        CASE WHEN Gols_Mandante < Gols_Visitante THEN 1 ELSE 0 END AS Derrota,
        Gols_Mandante AS Gols_Feitos,
        Gols_Visitante AS Gols_Sofridos
    FROM Dados_Partidas_Consolidados

    UNION ALL

    -- Calcula os pontos, vitórias, empates, derrotas e gols como VISITANTE
    SELECT
        ID_Time_Visitante AS ID_Time,
        CASE
            WHEN Gols_Visitante > Gols_Mandante THEN 3
            WHEN Gols_Visitante = Gols_Mandante THEN 1
            ELSE 0
        END AS Pontos,
        CASE WHEN Gols_Visitante > Gols_Mandante THEN 1 ELSE 0 END AS Vitoria,
        CASE WHEN Gols_Visitante = Gols_Mandante THEN 1 ELSE 0 END AS Empate,
        CASE WHEN Gols_Visitante < Gols_Mandante THEN 1 ELSE 0 END AS Derrota,
        Gols_Visitante AS Gols_Feitos,
        Gols_Mandante AS Gols_Sofridos
    FROM Dados_Partidas_Consolidados
)
SELECT
    t.Nome AS Nome_Time,
    COALESCE(SUM(p.Pontos), 0) AS Pontos,
    COALESCE(SUM(p.Vitoria), 0) AS Vitorias,
    COALESCE(SUM(p.Empate), 0) AS Empates,
    COALESCE(SUM(p.Derrota), 0) AS Derrotas,
    COALESCE(SUM(p.Gols_Feitos), 0) - COALESCE(SUM(p.Gols_Sofridos), 0) AS Saldo_Gols
FROM TIME t
LEFT JOIN Pontuacao_Partidas p ON t.ID_Time = p.ID_Time
GROUP BY t.ID_Time, t.Nome
ORDER BY Pontos DESC, Vitorias DESC, Saldo_Gols DESC;


-- 3. VIEW_RESULTADOS_E_AGENDAMENTOS
-- Retorna os dados macro de partidas agendadas ou finalizadas de forma legível.
CREATE OR REPLACE VIEW VIEW_RESULTADOS_E_AGENDAMENTOS AS
SELECT
    p.Data_Hora,
    p.Local,
    tm.Nome AS Time_Mandante,
    COALESCE((SELECT SUM(gols) FROM ESTATISTICA_PARTIDA ep INNER JOIN JOGADOR j ON ep.id_jogador = j.id_jogador WHERE ep.id_partida = p.id_partida AND j.id_time = tm.id_time), 0) AS Placar_Mandante,
    COALESCE((SELECT SUM(gols) FROM ESTATISTICA_PARTIDA ep INNER JOIN JOGADOR j ON ep.id_jogador = j.id_jogador WHERE ep.id_partida = p.id_partida AND j.id_time = tv.id_time), 0) AS Placar_Visitante,
    tv.Nome AS Time_Visitante,
    CASE
        WHEN p.Data_Hora < CURRENT_TIMESTAMP THEN 'Finalizada'
        ELSE 'Agendada'
    END AS Status
FROM PARTIDAS p
INNER JOIN TIME tm ON p.ID_Time_Mandante = tm.ID_Time
INNER JOIN TIME tv ON p.ID_Time_Visitante = tv.ID_Time;


-- 4. VIEW_HISTORICO_INDIVIDUAL_TIME
-- Permite ao Python buscar o histórico individual puxando a condição (Mandante/Visitante) e Status.
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
FROM TIME t
CROSS JOIN VIEW_RESULTADOS_E_AGENDAMENTOS v
WHERE t.Nome = v.Time_Mandante OR t.Nome = v.Time_Visitante;