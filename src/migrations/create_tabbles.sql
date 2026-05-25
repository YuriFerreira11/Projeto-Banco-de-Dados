-- LIMPEZA TOTAL (Apaga o banco antigo para não dar conflito)
DROP TABLE IF EXISTS Torneio_Admin CASCADE;
DROP TABLE IF EXISTS Admin CASCADE;
DROP TABLE IF EXISTS Estatistica_Partida CASCADE; -- Tabela que morreu no novo diagrama
DROP TABLE IF EXISTS Partidas CASCADE;
DROP TABLE IF EXISTS Jogador CASCADE;
DROP TABLE IF EXISTS Time CASCADE;
DROP TABLE IF EXISTS Torneio CASCADE;

--- 1. Tabela: TORNEIO
CREATE TABLE Torneio (
    ID_Torneio SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Data_Inicio DATE NOT NULL,
    Data_Fim DATE NOT NULL
);

--- 2. Tabela: ADMIN (Nova - para o login do sistema)
CREATE TABLE Admin (
    ID_Admin SERIAL PRIMARY KEY,
    Senha VARCHAR(255) NOT NULL -- Aqui ficará a senha criptografada pela sua SECRET_KEY
);

--- 3. Tabela: TORNEIO_ADMIN (Relacionamento N:N)
CREATE TABLE Torneio_Admin (
    ID_Torneio INT NOT NULL,
    ID_Admin INT NOT NULL,
    PRIMARY KEY (ID_Torneio, ID_Admin),
    CONSTRAINT FK_TorneioAdmin_Torneio FOREIGN KEY (ID_Torneio)
        REFERENCES Torneio(ID_Torneio) ON DELETE CASCADE,
    CONSTRAINT FK_TorneioAdmin_Admin FOREIGN KEY (ID_Admin)
        REFERENCES Admin(ID_Admin) ON DELETE CASCADE
);

--- 4. Tabela: TIME
CREATE TABLE Time (
    ID_Time SERIAL PRIMARY KEY,
    Nome VARCHAR(255) NOT NULL,
    Logo VARCHAR(255)
);

--- 5. Tabela: JOGADOR
CREATE TABLE Jogador (
    ID_Jogador SERIAL PRIMARY KEY,
    CPF VARCHAR(11) NOT NULL UNIQUE,
    Nome VARCHAR(255) NOT NULL,
    Funcao VARCHAR(50),
    ID_Time INT,
    CONSTRAINT FK_Jogador_Time FOREIGN KEY (ID_Time)
        REFERENCES Time(ID_Time) ON DELETE SET NULL
);

--- 6. Tabela: PARTIDAS (Com placar integrado conforme o novo diagrama)
CREATE TABLE Partidas (
    ID_Partida SERIAL PRIMARY KEY,
    Data_Hora TIMESTAMP NOT NULL,
    Local VARCHAR(255),
    ID_Torneio INT NOT NULL,
    ID_Time_Mandante INT NOT NULL,
    Gols_M INT DEFAULT 0,
    ID_Time_Visitante INT NOT NULL,
    Gols_V INT DEFAULT 0,
    CONSTRAINT FK_Partidas_Torneio FOREIGN KEY (ID_Torneio)
        REFERENCES Torneio(ID_Torneio) ON DELETE CASCADE,
    CONSTRAINT FK_Partidas_Mandante FOREIGN KEY (ID_Time_Mandante)
        REFERENCES Time(ID_Time),
    CONSTRAINT FK_Partidas_Visitante FOREIGN KEY (ID_Time_Visitante)
        REFERENCES Time(ID_Time),
    CONSTRAINT CK_Times_Diferentes CHECK (ID_Time_Mandante <> ID_Time_Visitante)
);