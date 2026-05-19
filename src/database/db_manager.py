import os
import sys
import psycopg2
import yaml

# Descobre o caminho absoluto para a pasta 'src' de forma dinâmica
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminhos absolutos calibrados com a árvore real do projeto
PATH_CONFIG = os.path.join(BASE_DIR, "config.yaml")
PATH_TABELAS = os.path.join(BASE_DIR, "database", "create_tabbles.sql")
PATH_VIEWS = os.path.join(BASE_DIR, "database", "create_views.sql")


def carregar_credenciais():
    """Lê o arquivo yaml e retorna os dados de conexão."""
    if not os.path.exists(PATH_CONFIG):
        raise FileNotFoundError(f"Arquivo '{PATH_CONFIG}' não encontrado.")
    with open(PATH_CONFIG, "r") as arquivo:
        config = yaml.safe_load(arquivo)
    return config["database"]


def executar_arquivo_sql(cursor, caminho_arquivo, descricao):
    """Lê um arquivo .sql e executa todos os comandos dele no banco."""
    print(f" Executando: {descricao}...")
    if not os.path.exists(caminho_arquivo):
        print(f" [❌] Erro: Arquivo não encontrado em {caminho_arquivo}")
        return False

    with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo_sql = arquivo.read()

    try:
        cursor.execute(conteudo_sql)
        print(f" [✔] {descricao} concluído com sucesso!")
        return True
    except Exception as e:
        print(f" [❌] Erro ao executar {descricao}: {e}")
        return False


def apagar_estrutura_banco():
    """Remove todas as views e tabelas físicas do schema public."""
    print("\n" + "-" * 50)
    print("OPERANDO: Apagando toda a estrutura do banco...")
    print("-" * 50)

    comando_limpeza = """
        DROP VIEW IF EXISTS VIEW_HISTORICO_INDIVIDUAL_TIME CASCADE;
        DROP VIEW IF EXISTS VIEW_RESULTADOS_E_AGENDAMENTOS CASCADE;
        DROP VIEW IF EXISTS VIEW_CLASSIFICACAO_GERAL CASCADE;
        DROP VIEW IF EXISTS VIEW_ARTILHARIA_E_GARCOM CASCADE;

        DROP TABLE IF EXISTS ESTATISTICA_PARTIDA CASCADE;
        DROP TABLE IF EXISTS PARTIDAS CASCADE;
        DROP TABLE IF EXISTS JOGADOR CASCADE;
        DROP TABLE IF EXISTS TIME CASCADE;
        DROP TABLE IF EXISTS TORNEIO CASCADE;
    """
    try:
        dados_banco = carregar_credenciais()
        with psycopg2.connect(**dados_banco) as conexao:
            conexao.autocommit = True
            with conexao.cursor() as cursor:
                cursor.execute(comando_limpeza)
        print(" [✔] Banco de dados limpo com sucesso (0 tabelas restantes).")
        return True
    except Exception as e:
        print(f" [❌] Erro ao limpar o banco de dados: {e}")
        return False


def criar_estrutura_banco():
    """Executa os scripts SQL para criar as tabelas e as views."""
    print("\n" + "-" * 50)
    print("OPERANDO: Criando tabelas e views estruturais...")
    print("-" * 50)

    try:
        dados_banco = carregar_credenciais()
        with psycopg2.connect(**dados_banco) as conexao:
            conexao.autocommit = True
            with conexao.cursor() as cursor:
                if executar_arquivo_sql(cursor, PATH_TABELAS, "Criação de Tabelas Físicas"):
                    if executar_arquivo_sql(cursor, PATH_VIEWS, "Criação da Camada de Visões (Views)"):
                        print(" [✔] Toda a infraestrutura foi mapeada com sucesso.")
                        return True
        return False
    except Exception as e:
        print(f" [❌] Erro durante a criação das estruturas: {e}")
        return False


def restart_banco():
    """Combina as funções de apagar e criar para um reset completo."""
    print("\n" + "=" * 60)
    print("CONTROLADOR: INICIANDO PROCESSAMENTO DE RESTART TOTAL")
    print("=" * 60)

    if apagar_estrutura_banco():
        if criar_estrutura_banco():
            print("\n[SUCESSO] O Banco foi reiniciado e está pronto para uso!")
            print("=" * 60 + "\n")
            return True

    print("\n[FALHA] Não foi possível completar o restart do banco.")
    print("=" * 60 + "\n")
    return False


def inspecionar_banco():
    """Testa a conexão e lista o estado atual das tabelas e views."""
    print("\nLendo o arquivo de configuração...")
    try:
        dados_banco = carregar_credenciais()
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")
        return

    print(f"Tentando conectar ao host: {dados_banco['host']}...")
    try:
        with psycopg2.connect(**dados_banco) as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT NOW();")
                horario_banco = cursor.fetchone()

                print("\n[CONEXÃO BEM-SUCEDIDA!]")
                print(f"-> Banco: {dados_banco['dbname']} | Usuário: {dados_banco['user']}")
                print(f"-> Horário do servidor: {horario_banco[0]}\n")

                # Inspeção de Tabelas
                print("-" * 50)
                print("INSPEÇÃO DE TABELAS FÍSICAS (BASE TABLES):")
                print("-" * 50)
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE' ORDER BY table_name;
                """)
                tabelas = cursor.fetchall()
                for t in tabelas: print(f" [✔] Tabela: {t[0]}")
                if not tabelas: print(" [⚠] Nenhuma tabela física encontrada.")

                # Inspeção de Views
                print("\n" + "-" * 50)
                print("INSPEÇÃO DE TABELAS VIRTUAIS (VIEWS):")
                print("-" * 50)
                cursor.execute("""
                    SELECT table_name FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_type = 'VIEW' ORDER BY table_name;
                """)
                views = cursor.fetchall()
                for v in views: print(f" [★] View: {v[0]}")
                if not views: print(" [⚠] Nenhuma View encontrada.")
                print("-" * 50 + "\n")

    except Exception as erro:
        print(f"\n[FALHA NA CONEXÃO]: {erro}")


def exibir_menu():
    print("\n" + "=" * 45)
    print("       GERENCIADOR DO BANCO DE DADOS - TORNEIO")
    print("=" * 45)
    print(" [1] Verificar Conexão e Inspecionar Estruturas")
    print(" [2] Criar Tabelas e Views (Apenas se estiver vazio)")
    print(" [3] Limpar Banco (Apagar Tabelas e Views)")
    print(" [4] Restart Total (Apagar tudo e Recriar do zero)")
    print(" [0] Sair do Programa")
    print("=" * 45)


def menu_principal():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                inspecionar_banco()
            case "2":
                criar_estrutura_banco()
            case "3":
                confirmar = input("Tem certeza que deseja APAGAR tudo? (s/n): ").lower()
                if confirmar == 's':
                    apagar_estrutura_banco()
                else:
                    print("Operação cancelada.")
            case "4":
                confirmar = input("Isso vai ZERAR o banco de dados. Continuar? (s/n): ").lower()
                if confirmar == 's':
                    restart_banco()
                else:
                    print("Operação cancelada.")
            case "0":
                print("\nEncerrando o gerenciador de infraestrutura. Até mais!")
                sys.exit(0)
            case _:
                print("\n[❌] Opção inválida! Digite um número de 0 a 4.")

        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    # Quando rodar o db_manager.py diretamente, ele abre o menu!
    menu_principal()