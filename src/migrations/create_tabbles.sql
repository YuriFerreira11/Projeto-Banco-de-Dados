-- PARTE 1: LIMPEZA TOTAL (Drops)
DROP TABLE IF EXISTS Partidas CASCADE;
DROP TABLE IF EXISTS Torneio_Time CASCADE;
DROP TABLE IF EXISTS Jogador CASCADE;
DROP TABLE IF EXISTS Time CASCADE;
DROP TABLE IF EXISTS Torneio CASCADE;
DROP TABLE IF EXISTS Admin CASCADE;


-- PARTE 2: CRIAÇÃO RESTRITA DAS TABELAS (Apenas Estrutura e Chaves Primárias)
CREATE TABLE Torneio (
    ID_Torneio SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Data_Inicio DATE NOT NULL,
    Data_Fim DATE NOT NULL
);

CREATE TABLE Admin (
    ID_Admin SERIAL PRIMARY KEY,
    Senha VARCHAR(255) NOT NULL
);

CREATE TABLE Time (
    ID_Time SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Escudo VARCHAR(255)
);

CREATE TABLE Torneio_Time (
    ID_Torneio INT NOT NULL,
    ID_Time    INT NOT NULL,
    PRIMARY KEY (ID_Torneio, ID_Time)
);

CREATE TABLE Jogador (
    ID_Jogador SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Funcao VARCHAR(50),
    ID_Time INT
);

CREATE TABLE Partidas (
    ID_Partida SERIAL PRIMARY KEY,
    ID_Torneio INT NOT NULL,
    Rodada INT NOT NULL,
    ID_Time_Mandante INT NOT NULL,
    ID_Time_Visitante INT NOT NULL,
    Gols_M INT DEFAULT 0,
    Gols_V INT DEFAULT 0,
    Data_Hora TIMESTAMP,
    Local VARCHAR(255),
    CONSTRAINT CK_Times_Diferentes CHECK (ID_Time_Mandante <> ID_Time_Visitante)
);


-- PARTE 3: ADIÇÃO DAS REFERÊNCIAS (Chaves Estrangeiras - Foreign Keys)
-- Relacionamentos da tabela Torneio_Time
ALTER TABLE Torneio_Time
    ADD CONSTRAINT FK_TorneioTime_Torneio FOREIGN KEY (ID_Torneio)
    REFERENCES Torneio(ID_Torneio) ON DELETE CASCADE;

ALTER TABLE Torneio_Time
    ADD CONSTRAINT FK_TorneioTime_Time FOREIGN KEY (ID_Time)
    REFERENCES Time(ID_Time) ON DELETE CASCADE;

-- Relacionamentos da tabela Jogador
ALTER TABLE Jogador
    ADD CONSTRAINT FK_Jogador_Time FOREIGN KEY (ID_Time)
    REFERENCES Time(ID_Time) ON DELETE SET NULL;

-- Relacionamentos da tabela Partidas
ALTER TABLE Partidas
    ADD CONSTRAINT FK_Partidas_Torneio FOREIGN KEY (ID_Torneio)
    REFERENCES Torneio(ID_Torneio) ON DELETE CASCADE;

ALTER TABLE Partidas
    ADD CONSTRAINT FK_Partidas_Mandante FOREIGN KEY (ID_Time_Mandante)
    REFERENCES Time(ID_Time);

ALTER TABLE Partidas
    ADD CONSTRAINT FK_Partidas_Visitante FOREIGN KEY (ID_Time_Visitante)
    REFERENCES Time(ID_Time);