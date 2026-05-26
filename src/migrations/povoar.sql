-- 1. LIMPEZA (Garante que começamos do zero para evitar erro de FK)
TRUNCATE TABLE Partidas, Jogador, Time, Torneio_Admin, Torneio, Admin RESTART IDENTITY CASCADE;

-- 2. ADMIN (Criando um admin padrão)
INSERT INTO Admin (Senha) VALUES ('senha123');

-- 3. TORNEIO
INSERT INTO Torneio (Nome, Data_Inicio, Data_Fim)
VALUES ('Série A 2026', '2026-01-01', '2026-12-31');

-- 4. TIMES (Coluna "Escudo" com E maiúsculo conforme seu DDL)
INSERT INTO Time (Nome, Escudo) VALUES
('Palmeiras', 'https://upload.wikimedia.org/wikipedia/pt/1/10/Palmeiras_logo.png'),
('Flamengo', 'https://upload.wikimedia.org/wikipedia/pt/d/de/Flamengo-2018.png'),
('Fluminense', 'https://upload.wikimedia.org/wikipedia/pt/a/a3/FFC_logo.png'),
('Athletico-PR', 'https://upload.wikimedia.org/wikipedia/pt/c/c7/Athletico_Paranaense.png'),
('Bragantino', 'https://upload.wikimedia.org/wikipedia/pt/9/9e/RedBullBragantino.png'),
('São Paulo', 'https://upload.wikimedia.org/wikipedia/pt/4/4b/São_Paulo_Futebol_Clube.png'),
('Bahia', 'https://upload.wikimedia.org/wikipedia/pt/6/61/ECBahia.png'),
('Coritiba', 'https://upload.wikimedia.org/wikipedia/pt/3/38/Coritiba_FBC.png'),
('Cruzeiro', 'https://upload.wikimedia.org/wikipedia/pt/b/bc/Cruzeiro_Esporte_Clube.png'),
('Botafogo', 'https://upload.wikimedia.org/wikipedia/pt/d/d2/Botafogo_de_Futebol_e_Regatas_logo.png'),
('Vitória', 'https://upload.wikimedia.org/wikipedia/pt/7/70/Esporte_Clube_Vitória_logo.png'),
('Atlético-MG', 'https://upload.wikimedia.org/wikipedia/pt/5/5f/Atletico_mineiro_galo.png'),
('Internacional', 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Escudo_do_Sport_Club_Internacional.svg'),
('Grêmio', 'https://upload.wikimedia.org/wikipedia/pt/d/d3/Gremio_logo.png'),
('Corinthians', 'https://upload.wikimedia.org/wikipedia/pt/5/5a/Club_Athletico_Paulistano_logo.png'),
('Vasco', 'https://upload.wikimedia.org/wikipedia/pt/e/e9/VascodaGama.png'),
('Santos', 'https://upload.wikimedia.org/wikipedia/commons/3/35/Santos_logo.svg'),
('Mirassol', 'https://upload.wikimedia.org/wikipedia/pt/0/01/Mirassol_Futebol_Clube.png'),
('Remo', 'https://upload.wikimedia.org/wikipedia/pt/4/4a/Clube_do_Remo.png'),
('Chapecoense', 'https://upload.wikimedia.org/wikipedia/pt/8/8d/Chapecoense_logo.png');

-- 5. JOGADORES (CPF com 11 dígitos conforme seu VARCHAR(11))
DO $$
DECLARE t_id INT;
BEGIN
    FOR t_id IN 1..20 LOOP
        INSERT INTO Jogador (CPF, Nome, Funcao, ID_Time) VALUES
        (LPAD(CAST(t_id * 100 + 1 AS TEXT), 11, '0'), 'Capitão ' || t_id, 'Zagueiro', t_id),
        (LPAD(CAST(t_id * 100 + 2 AS TEXT), 11, '0'), 'Craque ' || t_id, 'Atacante', t_id);
    END LOOP;
END $$;

-- 6. PARTIDAS (Ajustado para Gols_M e Gols_V com iniciais maiúsculas)
INSERT INTO Partidas (Data_Hora, Local, ID_Torneio, ID_Time_Mandante, Gols_M, ID_Time_Visitante, Gols_V) VALUES
('2026-05-20 16:00:00', 'Allianz Parque', 1, 1, 2, 20, 0),
('2026-05-20 16:00:00', 'Maracanã', 1, 2, 3, 16, 1),
('2026-05-20 18:30:00', 'Mineirão', 1, 9, 4, 10, 0),
('2026-05-20 21:00:00', 'São Januário', 1, 16, 2, 19, 0),
('2026-05-21 19:00:00', 'Arena MRV', 1, 12, 1, 13, 1),
('2026-05-21 19:00:00', 'Neo Química Arena', 1, 15, 2, 6, 2),
('2026-05-22 16:00:00', 'Vila Belmiro', 1, 17, 0, 3, 2),
('2026-05-22 18:00:00', 'Arena da Baixada', 1, 4, 1, 5, 2),
('2026-05-22 21:00:00', 'Barradão', 1, 11, 0, 14, 1);



-- 1. NOVO TORNEIO
INSERT INTO Torneio (Nome, Data_Inicio, Data_Fim)
VALUES ('Série B 2026', '2026-02-01', '2026-11-30');

-- 2. NOVOS TIMES (Para a Série B)
INSERT INTO Time (Nome, Escudo) VALUES
('Sport Recife', 'https://upload.wikimedia.org/wikipedia/pt/1/17/Sport_Club_do_Recife.png'),
('Ceará', 'https://upload.wikimedia.org/wikipedia/pt/4/4c/Ceara_SC_Logo.png'),
('Goiás', 'https://upload.wikimedia.org/wikipedia/pt/b/be/Goiás_Esporte_Clube_logo.png'),
('Avaí', 'https://upload.wikimedia.org/wikipedia/pt/f/f3/Avai_FC_2005.png'),
('Ponte Preta', 'https://upload.wikimedia.org/wikipedia/pt/9/90/Ponte_Preta_logo.png'),
('Guarani', 'https://upload.wikimedia.org/wikipedia/pt/4/41/Guarani_Futebol_Clube_logo.png');

-- 3. JOGADORES PARA OS NOVOS TIMES
-- (IDs 21 a 26 baseados no insert acima)
INSERT INTO Jogador (CPF, Nome, Funcao, ID_Time) VALUES
('21000000001', 'Diego Souza', 'Atacante', 21),
('22000000001', 'Vina', 'Meia', 22),
('23000000001', 'Tadeu', 'Goleiro', 23),
('24000000001', 'Vagner Love', 'Atacante', 24);

-- 4. PARTIDAS DA SÉRIE B (ID_Torneio = 2)
-- Aqui testamos se o filtro por ID_Torneio está funcionando no seu Router/Queries
INSERT INTO Partidas (Data_Hora, Local, ID_Torneio, ID_Time_Mandante, Gols_M, ID_Time_Visitante, Gols_V) VALUES
('2026-05-24 16:00:00', 'Ilha do Retiro', 2, 21, 2, 22, 1), -- Sport 2 x 1 Ceará
('2026-05-24 18:00:00', 'Serrinha', 2, 23, 0, 24, 0),      -- Goiás 0 x 0 Avaí
('2026-05-25 20:00:00', 'Moisés Lucarelli', 2, 25, 1, 26, 1); -- Derby Campineiro