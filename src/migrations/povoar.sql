-- =============================================================================
-- 1. LIMPEZA DO BANCO
-- =============================================================================
TRUNCATE TABLE Partidas, Jogador, Torneio_Time, Time, Torneio, Admin
RESTART IDENTITY CASCADE;

-- =============================================================================
-- 2. ADMINISTRADORES
-- =============================================================================
INSERT INTO Admin (Senha)
VALUES ('senha123');

-- =============================================================================
-- 3. TORNEIOS
-- =============================================================================
INSERT INTO Torneio (Nome, Data_Inicio, Data_Fim)
VALUES ('Série A 2026', '2026-01-01', '2026-12-31');

-- =============================================================================
-- 4. TIMES - SÉRIE A
-- =============================================================================
INSERT INTO Time (Nome, Escudo) VALUES
('Palmeiras',     'https://s.sde.globo.com/media/organizations/2014/04/14/palmeiras_60x60.png'),
('Flamengo',      'https://s.sde.globo.com/media/organizations/2014/04/14/flamengo_60x60.png'),
('Fluminense',    'https://s.sde.globo.com/media/organizations/2014/04/14/fluminense_60x60.png'),
('Athletico-PR',  'https://escudosfc.com.br/images/atlpr.png'),
('Bragantino',    'https://escudosfc.com.br/images/bragantino.png'),
('São Paulo',     'https://s.sde.globo.com/media/organizations/2014/04/14/sao_paulo_60x60.png'),
('Bahia',         'https://s.sde.globo.com/media/organizations/2014/04/14/bahia_60x60.png'),
('Coritiba',      'https://commons.wikimedia.org/wiki/Special:FilePath/Coritiba_Foot_Ball_Club_logo.svg'),
('Cruzeiro',      'https://commons.wikimedia.org/wiki/Special:FilePath/Cruzeiro_Esporte_Clube_(logo).svg'),
('Botafogo',      'https://s.sde.globo.com/media/organizations/2014/04/14/botafogo_60x60.png'),
('Vitória',       'https://s.sde.globo.com/media/organizations/2014/04/14/vitoria_60x60.png'),
('Atlético-MG',   'https://s.sde.globo.com/media/organizations/2014/04/14/atletico_mg_60x60.png'),
('Internacional', 'https://s.sde.globo.com/media/organizations/2014/04/14/internacional_60x60.png'),
('Grêmio',        'https://s.sde.globo.com/media/organizations/2014/04/14/gremio_60x60.png'),
('Corinthians',   'https://s.sde.globo.com/media/organizations/2014/04/14/corinthians_60x60.png'),
('Vasco',         'https://s.sde.globo.com/media/organizations/2014/04/14/vasco_60x60.png'),
('Santos',        'https://s.sde.globo.com/media/organizations/2014/04/14/santos_60x60.png'),
('Mirassol',      'https://commons.wikimedia.org/wiki/Special:FilePath/Mirassol_FC_logo.png'),
('Remo',          'https://escudosfc.com.br/images/remo.png'),
('Chapecoense',   'https://s.sde.globo.com/media/organizations/2014/04/14/chapecoense_60x60.png');

-- =============================================================================
-- 5. VÍNCULO TORNEIO E TIMES (SÉRIE A)
-- =============================================================================
INSERT INTO Torneio_Time (ID_Torneio, ID_Time)
SELECT tr.ID_Torneio, t.ID_Time
FROM Torneio tr
CROSS JOIN Time t
WHERE tr.Nome = 'Série A 2026'
  AND t.Nome IN (
    'Palmeiras', 'Flamengo', 'Fluminense', 'Athletico-PR', 'Bragantino',
    'São Paulo', 'Bahia', 'Coritiba', 'Cruzeiro', 'Botafogo', 'Vitória',
    'Atlético-MG', 'Internacional', 'Grêmio', 'Corinthians', 'Vasco',
    'Santos', 'Mirassol', 'Remo', 'Chapecoense'
  );

-- =============================================================================
-- 6. JOGADORES - SÉRIE A
-- =============================================================================

-- PALMEIRAS
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Weverton','Goleiro'),('Marcos Rocha','Lateral'),('Gustavo Gómez','Zagueiro'),
  ('Murilo','Zagueiro'),('Piquerez','Lateral'),('Aníbal Moreno','Meia'),
  ('Richard Ríos','Meia'),('Raphael Veiga','Meia'),('Felipe Anderson','Atacante'),
  ('Flaco López','Atacante'),('Dudu','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Palmeiras') t;

-- FLAMENGO
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Rossi','Goleiro'),('Wesley','Lateral'),('Léo Ortiz','Zagueiro'),
  ('Léo Pereira','Zagueiro'),('Ayrton Lucas','Lateral'),('Gerson','Meia'),
  ('Pulgar','Meia'),('De La Cruz','Meia'),('Arrascaeta','Meia'),
  ('Luiz Araújo','Atacante'),('Pedro','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Flamengo') t;

-- FLUMINENSE
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Fábio','Goleiro'),('Samuel Xavier','Lateral'),('Thiago Silva','Zagueiro'),
  ('Thiago Santos','Zagueiro'),('Diogo Barbosa','Lateral'),('Martinelli','Meia'),
  ('Facundo Bernal','Meia'),('Ganso','Meia'),('Jhon Arias','Atacante'),
  ('Kauã Elias','Atacante'),('Keno','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Fluminense') t;

-- ATHLETICO-PR
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Mycael','Goleiro'),('Madson','Lateral'),('Thiago Heleno','Zagueiro'),
  ('Kaique Rocha','Zagueiro'),('Sub-20','Lateral'),('Erick','Meia'),
  ('Fernandinho','Meia'),('Zapelli','Meia'),('Cuello','Atacante'),
  ('Nikão','Atacante'),('Pablo','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Athletico-PR') t;

-- BRAGANTINO
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Cleiton','Goleiro'),('Nathan Mendes','Lateral'),('Pedro Henrique','Zagueiro'),
  ('Luan Cândido','Zagueiro'),('Juninho Capixaba','Lateral'),('Jadsom','Meia'),
  ('Lucas Evangelista','Meia'),('Lincoln','Meia'),('Henry Mosquera','Atacante'),
  ('Eduardo Sasha','Atacante'),('Vitinho','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Bragantino') t;

-- SÃO PAULO
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Rafael','Goleiro'),('Igor Vinícius','Lateral'),('Arboleda','Zagueiro'),
  ('Alan Franco','Zagueiro'),('Welington','Lateral'),('Luiz Gustavo','Meia'),
  ('Alisson','Meia'),('Lucas Moura','Meia'),('Luciano','Meia'),
  ('Ferreira','Atacante'),('Calleri','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='São Paulo') t;

-- BAHIA
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Marcos Felipe','Goleiro'),('Santiago Arias','Lateral'),('Gabriel Xavier','Zagueiro'),
  ('Kanu','Zagueiro'),('Luciano Juba','Lateral'),('Caio Alexandre','Meia'),
  ('Jean Lucas','Meia'),('Éverton Ribeiro','Meia'),('Cauly','Meia'),
  ('Thaciano','Atacante'),('Everaldo','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Bahia') t;

-- CORITIBA
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Pedro Morisco','Goleiro'),('Natanael','Lateral'),('Mauricio Antônio','Zagueiro'),
  ('Benevenuto','Zagueiro'),('Bruno Melo','Lateral'),('Sebastian Gómez','Meia'),
  ('Vini Paulista','Meia'),('Matheus Frizzo','Meia'),('Robson','Atacante'),
  ('Lucas Ronier','Atacante'),('Júnior Brumado','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Coritiba') t;

-- CRUZEIRO
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Cássio','Goleiro'),('William','Lateral'),('Zé Ivaldo','Zagueiro'),
  ('João Marcelo','Zagueiro'),('Marlon','Lateral'),('Lucas Romero','Meia'),
  ('Walace','Meia'),('Matheus Pereira','Meia'),('Álvaro Barreal','Meia'),
  ('Gabriel Veron','Atacante'),('Kaio Jorge','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Cruzeiro') t;

-- BOTAFOGO
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('John','Goleiro'),('Vitinho','Lateral'),('Bastos','Zagueiro'),
  ('Alexander Barboza','Zagueiro'),('Cuiabano','Lateral'),('Gregore','Meia'),
  ('Marlon Freitas','Meia'),('Thiago Almada','Meia'),('Luiz Henrique','Atacante'),
  ('Igor Jesus','Atacante'),('Savarino','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Botafogo') t;

-- VITÓRIA
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Lucas Arcanjo','Goleiro'),('Raúl Cáceres','Lateral'),('Neris','Zagueiro'),
  ('Wagner Leonardo','Zagueiro'),('Lucas Esteves','Lateral'),('Luan','Meia'),
  ('Willian Oliveira','Meia'),('Matheuzinho','Meia'),('Osvaldo','Atacante'),
  ('Alerrandro','Atacante'),('Carlos Eduardo','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Vitória') t;

-- ATLÉTICO-MG
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Everson','Goleiro'),('Saravia','Lateral'),('Battaglia','Zagueiro'),
  ('Junior Alonso','Zagueiro'),('Guilherme Arana','Lateral'),('Otávio','Meia'),
  ('Alan Franco','Meia'),('Gustavo Scarpa','Meia'),('Bernard','Meia'),
  ('Paulinho','Atacante'),('Hulk','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Atlético-MG') t;

-- INTERNACIONAL
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Rochet','Goleiro'),('Nathan','Lateral'),('Vitão','Zagueiro'),
  ('Gabriel Mercado','Zagueiro'),('Bernabei','Lateral'),('Fernando','Meia'),
  ('Thiago Maia','Meia'),('Alan Patrick','Meia'),('Gabriel Carvalho','Meia'),
  ('Wesley','Atacante'),('Rafael Borré','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Internacional') t;

-- GRÊMIO
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Marchesín','Goleiro'),('João Pedro','Lateral'),('Rodrigo Ely','Zagueiro'),
  ('Jemerson','Zagueiro'),('Reinaldo','Lateral'),('Villasanti','Meia'),
  ('Dodi','Meia'),('Cristaldo','Meia'),('Miguel Monsalve','Meia'),
  ('Soteldo','Atacante'),('Martin Braithwaite','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Grêmio') t;

-- CORINTHIANS
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Hugo Souza','Goleiro'),('Fagner','Lateral'),('André Ramalho','Zagueiro'),
  ('Félix Torres','Zagueiro'),('Matheus Bidu','Lateral'),('José Martínez','Meia'),
  ('Charles','Meia'),('Rodrigo Garro','Meia'),('André Carrillo','Meia'),
  ('Memphis Depay','Atacante'),('Yuri Alberto','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Corinthians') t;

-- VASCO
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Léo Jardim','Goleiro'),('Paulo Henrique','Lateral'),('João Victor','Zagueiro'),
  ('Maicon','Zagueiro'),('Lucas Piton','Lateral'),('Hugo Moura','Meia'),
  ('Mateus Carvalho','Meia'),('Dimitri Payet','Meia'),('Rayan','Atacante'),
  ('David','Atacante'),('Pablo Vegetti','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Vasco') t;

-- SANTOS
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Gabriel Brazão','Goleiro'),('Hayner','Lateral'),('Gil','Zagueiro'),
  ('Jair Paula','Zagueiro'),('Gonzalo Escobar','Lateral'),('João Schmidt','Meia'),
  ('Diego Pituca','Meia'),('Giuliano','Meia'),('Rómulo Otero','Meia'),
  ('Guilherme','Atacante'),('Wendel Silva','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Santos') t;

-- MIRASSOL
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Alex Muralha','Goleiro'),('Lucas Ramon','Lateral'),('João Victor','Zagueiro'),
  ('Luiz Otávio','Zagueiro'),('Zeca','Lateral'),('Neto Moura','Meia'),
  ('Danielzinho','Meia'),('Gabriel','Meia'),('Negueba','Atacante'),
  ('Fernandinho','Atacante'),('Dellatorre','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Mirassol') t;

-- REMO
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Marcelo Rangel','Goleiro'),('Diogo Batista','Lateral'),('Rafael Castro','Zagueiro'),
  ('Bruno Bispo','Zagueiro'),('Sávio','Lateral'),('Jaderson','Meia'),
  ('Giovanni Pavani','Meia'),('Matheus Anjos','Meia'),('Pedro Vitor','Atacante'),
  ('Rodrigo Alves','Atacante'),('Ytalo','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Remo') t;

-- CHAPECOENSE
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Léo Vieira','Goleiro'),('Marcelinho','Lateral'),('Bruno Leonardo','Zagueiro'),
  ('João Paulo','Zagueiro'),('Mancha','Lateral'),('Foguinho','Meia'),
  ('Tarik','Meia'),('Thomás Bedinelli','Meia'),('Marcinho','Atacante'),
  ('Rafael Carvalheira','Atacante'),('Mário Sérgio','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Chapecoense') t;


-- =============================================================================
-- 7. TORNEIO EUROPA E SEUS TIMES/JOGADORES
-- =============================================================================
INSERT INTO Torneio (Nome, Data_Inicio, Data_Fim)
VALUES ('Torneio Teste Europa 2026', '2026-07-01', '2026-07-31');

INSERT INTO Time (Nome, Escudo) VALUES
('Liverpool',     'https://upload.wikimedia.org/wikipedia/en/0/0c/Liverpool_FC.svg'),
('Real Madrid',   'https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg'),
('Barcelona',     'https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg'),
('Bayern Munich', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/FC_Bayern_M%C3%BCnchen_logo_%282024%29.svg/1280px-FC_Bayern_M%C3%BCnchen_logo_%282024%29.svg.png');

-- VÍNCULO TORNEIO E TIMES (EUROPA)
INSERT INTO Torneio_Time (ID_Torneio, ID_Time)
SELECT tr.ID_Torneio, t.ID_Time
FROM Torneio tr
CROSS JOIN Time t
WHERE tr.Nome = 'Torneio Teste Europa 2026'
  AND t.Nome IN ('Liverpool', 'Real Madrid', 'Barcelona', 'Bayern Munich');

-- JOGADORES - LIVERPOOL
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Alisson Becker','Goleiro'),('Jeremie Frimpong','Lateral'),('Virgil van Dijk','Zagueiro'),
  ('Jérémy Jacquet','Zagueiro'),('Milos Kerkez','Lateral'),('Ryan Gravenberch','Meia'),
  ('Alexis Mac Allister','Meia'),('Florian Wirtz','Meia'),('Dominik Szoboszlai','Meia'),
  ('Hugo Ekitiké','Atacante'),('Alexander Isak','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Liverpool') t;

-- JOGADORES - REAL MADRID
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Thibaut Courtois','Goleiro'),('Dani Carvajal','Lateral'),('Antonio Rüdiger','Zagueiro'),
  ('Éder Militão','Zagueiro'),('Ferland Mendy','Lateral'),('Federico Valverde','Meia'),
  ('Aurélien Tchouaméni','Meia'),('Jude Bellingham','Meia'),('Rodrygo','Atacante'),
  ('Vinícius Júnior','Atacante'),('Kylian Mbappé','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Real Madrid') t;

-- JOGADORES - BARCELONA
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Marc-André ter Stegen','Goleiro'),('Jules Koundé','Lateral'),('Ronald Araújo','Zagueiro'),
  ('Pau Cubarsí','Zagueiro'),('Alejandro Balde','Lateral'),('Frenkie de Jong','Meia'),
  ('Pedri','Meia'),('Gavi','Meia'),('Lamine Yamal','Atacante'),
  ('Robert Lewandowski','Atacante'),('Raphinha','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Barcelona') t;

-- JOGADORES - BAYERN MUNICH
INSERT INTO Jogador (Nome, Funcao, ID_Time)
SELECT j.nome, j.funcao, t.ID_Time
FROM ( VALUES
  ('Manuel Neuer','Goleiro'),('Konrad Laimer','Lateral'),('Dayot Upamecano','Zagueiro'),
  ('Kim Min-jae','Zagueiro'),('Alphonso Davies','Lateral'),('Joshua Kimmich','Meia'),
  ('Leon Goretzka','Meia'),('Jamal Musiala','Meia'),('Michael Olise','Atacante'),
  ('Harry Kane','Atacante'),('Kingsley Coman','Atacante')
) AS j(nome, funcao)
CROSS JOIN (SELECT ID_Time FROM Time WHERE Nome='Bayern Munich') t;