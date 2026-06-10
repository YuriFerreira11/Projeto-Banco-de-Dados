# Sistema de Gestão de Torneios 🏆

Este projeto consiste no desenvolvimento de um sistema desktop para gerenciamento de torneios de futebol. O foco principal é a estruturação de um banco de dados relacional robusto capaz de armazenar dados de equipes, atletas, partidas e eventos (gols e cartões), permitindo a geração automática de tabelas de classificação e estatísticas de desempenho.

O diferencial técnico reside na integração de um motor de processamento em Python com uma interface gráfica moderna e reativa, garantindo integridade referencial e eficiência nas consultas ao banco de dados.

## 🎯 Objetivos
* **Modelagem de Dados:** Criar um esquema relacional normalizado para gerenciar a complexidade de um torneio esportivo.
* **Automação de Cálculos:** Implementar lógica de negócio para processamento de rankings e critérios de desempate via código.
* **Gestão Administrativa:** Fornecer uma interface segura para que administradores realizem a manutenção dos dados (CRUD).

## 🚀 Tecnologias Utilizadas
* **Linguagem:** Python 3.x 
* **Interface Gráfica (GUI):** Flet (Framework baseado em Flutter com visual Material Design 3)
* **Mapeamento Objeto-Relacional (ORM):** SQLAlchemy 
* **Banco de Dados:** PostgreSQL

## ⚙️ Requisitos do Sistema (Funcionalidades)
* Cadastro e gerenciamento de times e jogadores.
* Registro de partidas com definição de mandantes e visitantes.
* Súmula digital para registro de eventos (gols, cartões e penalidades) em tempo real.
* Cálculo dinâmico da tabela de classificação (vitórias, empates, derrotas e saldo de gols).
* Sistema de autenticação para diferenciar administradores de visitantes.
## Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/YuriFerreira11/Projeto-Banco-de-Dados.git
cd Projeto-Banco-de-Dados
```

---

### 2. Crie e ative um ambiente virtual (Opcional, mas recomendado)

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configure o banco de dados

Certifique-se de possuir o PostgreSQL em execução na máquina.

Crie um arquivo `config.yaml` na raiz do projeto seguindo o modelo abaixo:

```yaml
database:
  host: "localhost"
  port: 5432
  dbname: "nome_do_banco"
  user: "seu_usuario"
  password: "sua_senha"
```

---

### 5. Execute a aplicação

```bash
python main
```
