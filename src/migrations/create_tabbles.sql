-- 1. Tabela: TORNEIO
-- É independente, armazena os dados macros do campeonato.
CREATE TABLE TORNEIO (
    ID_Torneio SERIAL,
    Nome VARCHAR(255) NOT NULL,
    Data_Inicio DATE NOT NULL,
    Data_Fim DATE NOT NULL,
    CONSTRAINT PK_TORNEIO PRIMARY KEY (ID_Torneio)
);

-- 2. Tabela: TIME
-- Guarda as informações dos clubes participantes.
CREATE TABLE TIME (
    ID_Time SERIAL,
    Nome VARCHAR(255) NOT NULL,
    Logo VARCHAR(255),
    CONSTRAINT PK_TIME PRIMARY KEY (ID_Time)
);

-- 3. Tabela: JOGADOR
-- Depende da tabela TIME para associar o atleta ao clube.
CREATE TABLE JOGADOR (
    ID_Jogador SERIAL,
    CPF VARCHAR(14) NOT NULL UNIQUE,
    Nome VARCHAR(255) NOT NULL,
    Funcao VARCHAR(50),
    ID_Time INT NOT NULL,
    CONSTRAINT PK_JOGADOR PRIMARY KEY (ID_Jogador),
    CONSTRAINT FK_JOGADOR_TIME FOREIGN KEY (ID_Time)
        REFERENCES TIME (ID_Time)
        ON DELETE CASCADE
);

-- 4. Tabela: PARTIDAS
-- Relaciona o Torneio aos dois clubes envolvidos (Mandante e Visitante).
CREATE TABLE PARTIDAS (
    ID_Partida SERIAL,
    Data_Hora TIMESTAMP NOT NULL,
    Local VARCHAR(255),
    ID_Torneio INT NOT NULL,
    ID_Time_Mandante INT NOT NULL,
    ID_Time_Visitante INT NOT NULL,
    CONSTRAINT PK_PARTIDAS PRIMARY KEY (ID_Partida),
    CONSTRAINT FK_PARTIDAS_TORNEIO FOREIGN KEY (ID_Torneio)
        REFERENCES TORNEIO (ID_Torneio)
        ON DELETE CASCADE,
    CONSTRAINT FK_PARTIDAS_MANDANTE FOREIGN KEY (ID_Time_Mandante)
        REFERENCES TIME (ID_Time),
    CONSTRAINT FK_PARTIDAS_VISITANTE FOREIGN KEY (ID_Time_Visitante)
        REFERENCES TIME (ID_Time),
    -- Garante que um time não jogue contra ele mesmo na mesma partida
    CONSTRAINT CK_CONFRONTO_VALIDO CHECK (ID_Time_Mandante <> ID_Time_Visitante)
);

-- 5. Tabela: ESTATISTICA_PARTIDA
-- Tabela atômica que liga o jogador aos eventos de uma partida específica.
CREATE TABLE ESTATISTICA_PARTIDA (
    ID_Estatistica SERIAL,
    Gols INT DEFAULT 0,
    Assistencias INT DEFAULT 0,
    C_Amarelo INT DEFAULT 0,
    C_Vermelho INT DEFAULT 0,
    Penalidades INT DEFAULT 0,
    ID_Partida INT NOT NULL,
    ID_Jogador INT NOT NULL,
    CONSTRAINT PK_ESTATISTICA_PARTIDA PRIMARY KEY (ID_Estatistica),
    CONSTRAINT FK_ESTATISTICA_PARTIDA_PARTIDA FOREIGN KEY (ID_Partida)
        REFERENCES PARTIDAS (ID_Partida)
        ON DELETE CASCADE,
    CONSTRAINT FK_ESTATISTICA_PARTIDA_JOGADOR FOREIGN KEY (ID_Jogador)
        REFERENCES JOGADOR (ID_Jogador)
        ON DELETE CASCADE
);