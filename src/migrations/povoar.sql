-- ============================================================
-- SCRIPT DE POVOAMENTO
-- As partidas são geradas pelo admin via interface.
-- ============================================================

-- 1. LIMPEZA
TRUNCATE TABLE Partidas, Jogador, Torneio_Time, Torneio_Admin, Time, Torneio, Admin RESTART IDENTITY CASCADE;

-- 2. ADMIN
INSERT INTO Admin (Senha) VALUES ('senha123');

-- 3. TORNEIOS
INSERT INTO Torneio (Nome, Data_Inicio, Data_Fim) VALUES
    ('Série A 2026', '2026-01-01', '2026-12-31'),
    ('Série B 2026', '2026-02-01', '2026-11-30');

-- 4. TIMES SÉRIE A (IDs 1–20)
INSERT INTO Time (Nome, Escudo) VALUES
('Palmeiras',     'https://upload.wikimedia.org/wikipedia/pt/1/10/Palmeiras_logo.png'),
('Flamengo',      'https://upload.wikimedia.org/wikipedia/pt/d/de/Flamengo-2018.png'),
('Fluminense',    'https://upload.wikimedia.org/wikipedia/pt/a/a3/FFC_logo.png'),
('Athletico-PR',  'https://upload.wikimedia.org/wikipedia/pt/c/c7/Athletico_Paranaense.png'),
('Bragantino',    'https://upload.wikimedia.org/wikipedia/pt/9/9e/RedBullBragantino.png'),
('São Paulo',     'https://upload.wikimedia.org/wikipedia/pt/4/4b/S%C3%A3o_Paulo_Futebol_Clube.png'),
('Bahia',         'https://upload.wikimedia.org/wikipedia/pt/6/61/ECBahia.png'),
('Coritiba',      'https://upload.wikimedia.org/wikipedia/pt/3/38/Coritiba_FBC.png'),
('Cruzeiro',      'https://upload.wikimedia.org/wikipedia/pt/b/bc/Cruzeiro_Esporte_Clube.png'),
('Botafogo',      'https://upload.wikimedia.org/wikipedia/pt/d/d2/Botafogo_de_Futebol_e_Regatas_logo.png'),
('Vitória',       'https://upload.wikimedia.org/wikipedia/pt/7/70/Esporte_Clube_Vitória_logo.png'),
('Atlético-MG',   'https://upload.wikimedia.org/wikipedia/pt/5/5f/Atletico_mineiro_galo.png'),
('Internacional', 'https://upload.wikimedia.org/wikipedia/commons/f/f1/Escudo_do_Sport_Club_Internacional.svg'),
('Grêmio',        'https://upload.wikimedia.org/wikipedia/pt/d/d3/Gremio_logo.png'),
('Corinthians',   'https://upload.wikimedia.org/wikipedia/pt/5/5a/Club_Athletico_Paulistano_logo.png'),
('Vasco',         'https://upload.wikimedia.org/wikipedia/pt/e/e9/VascodaGama.png'),
('Santos',        'https://upload.wikimedia.org/wikipedia/commons/3/35/Santos_logo.svg'),
('Mirassol',      'https://upload.wikimedia.org/wikipedia/pt/0/01/Mirassol_Futebol_Clube.png'),
('Remo',          'https://upload.wikimedia.org/wikipedia/pt/4/4a/Clube_do_Remo.png'),
('Chapecoense',   'https://upload.wikimedia.org/wikipedia/pt/8/8d/Chapecoense_logo.png');

-- 5. TIMES SÉRIE B (IDs 21–26)
INSERT INTO Time (Nome, Escudo) VALUES
('Sport Recife', 'https://upload.wikimedia.org/wikipedia/pt/1/17/Sport_Club_do_Recife.png'),
('Ceará',        'https://upload.wikimedia.org/wikipedia/pt/4/4c/Ceara_SC_Logo.png'),
('Goiás',        'https://upload.wikimedia.org/wikipedia/pt/b/be/Goiás_Esporte_Clube_logo.png'),
('Avaí',         'https://upload.wikimedia.org/wikipedia/pt/f/f3/Avai_FC_2005.png'),
('Ponte Preta',  'https://upload.wikimedia.org/wikipedia/pt/9/90/Ponte_Preta_logo.png'),
('Guarani',      'https://upload.wikimedia.org/wikipedia/pt/4/41/Guarani_Futebol_Clube_logo.png');

-- 6. VÍNCULO TORNEIO_TIME (Série A — times 1 a 20 no torneio 1)
INSERT INTO Torneio_Time (ID_Torneio, ID_Time)
SELECT 1, generate_series(1, 20);

-- Série B — times 21 a 26 no torneio 2
INSERT INTO Torneio_Time (ID_Torneio, ID_Time)
SELECT 2, generate_series(21, 26);

-- 7. JOGADORES (2 por time para os 20 times da Série A)
DO $$
DECLARE t_id INT;
BEGIN
    FOR t_id IN 1..20 LOOP
        INSERT INTO Jogador (Nome, Funcao, ID_Time) VALUES
        ('Capitão ' || t_id, 'Zagueiro', t_id),
        ('Craque '  || t_id, 'Atacante', t_id);
    END LOOP;
END $$;

-- Jogadores Série B
INSERT INTO Jogador (Nome, Funcao, ID_Time) VALUES
('Diego Souza', 'Atacante', 21),
('Vina',        'Meia',     22),
('Tadeu',       'Goleiro',  23),
('Vagner Love', 'Atacante', 24);
