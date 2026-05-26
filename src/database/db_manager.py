import os
import sys

from connection_factory import ConnectionFactory
from config.paths import CREATE_TABLES_PATH, CREATE_VIEWS_PATH


def executar_arquivo_sql(cursor, caminho_arquivo, descricao):
    print(f" Executando: {descricao}...")

    if not caminho_arquivo.exists():
        print(f" [❌] Erro: Arquivo não encontrado em {caminho_arquivo}")
        return False

    with caminho_arquivo.open("r", encoding="utf-8") as arquivo:
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
    conn = ConnectionFactory.get_connection()
    if not conn:
        return False
    try:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(comando_limpeza)
        print(" [✔] Banco de dados limpo com sucesso (0 tabelas restantes).")
        return True
    except Exception as e:
        print(f" [❌] Erro ao limpar o banco de dados: {e}")
        return False
    finally:
        conn.close()

def criar_estrutura_banco():
    """Executa os scripts SQL para criar as tabelas e as views."""
    print("\n" + "-" * 50)
    print("OPERANDO: Criando tabelas e views estruturais...")
    print("-" * 50)

    conn = ConnectionFactory.get_connection()
    if not conn:
        return False
    try:
        conn.autocommit = True
        with conn.cursor() as cursor:
            if executar_arquivo_sql(cursor, CREATE_TABLES_PATH, "Criação de Tabelas Físicas"):
                if executar_arquivo_sql(cursor, CREATE_VIEWS_PATH, "Criação da Camada de Visões (Views)"):
                    print(" [✔] Toda a infraestrutura foi mapeada com sucesso.")
                    return True
        return False
    except Exception as e:
        print(f" [❌] Erro durante a criação das estruturas: {e}")
        return False
    finally:
        conn.close()

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
    """Lista as tabelas e views com atributos identificando PKs e FKs."""
    print("\nConectando ao banco de dados via Factory...")
    conn = ConnectionFactory.get_connection()
    if not conn: return

    try:
        with conn.cursor() as cursor:
            print("\n[CONEXÃO BEM-SUCEDIDA!]")

            def imprimir_objetos(tipo_objeto, rotulo, icone):
                print("-" * 80)
                print(f"{rotulo}")
                print("-" * 80)

                cursor.execute(f"""
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_type = '{tipo_objeto}'
                    ORDER BY table_name;
                """)
                objetos = cursor.fetchall()

                for obj in objetos:
                    nome_obj = obj[0]
                    # Query avançada para buscar colunas e seus tipos de restrição (PK/FK)
                    cursor.execute(f"""
                        SELECT 
                            cols.column_name,
                            CASE 
                                WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'PK'
                                WHEN tc.constraint_type = 'FOREIGN KEY' THEN 'FK'
                                ELSE ''
                            END as constraint_label
                        FROM information_schema.columns cols
                        LEFT JOIN information_schema.key_column_usage kcu 
                            ON cols.column_name = kcu.column_name 
                            AND cols.table_name = kcu.table_name
                        LEFT JOIN information_schema.table_constraints tc 
                            ON kcu.constraint_name = tc.constraint_name
                        WHERE cols.table_name = '{nome_obj}'
                        ORDER BY cols.ordinal_position;
                    """)

                    colunas_raw = cursor.fetchall()
                    formatadas = []
                    for col, label in colunas_raw:
                        # Adiciona (PK) ou (FK) ao lado do nome se existir
                        tag = f" ({label})" if label else ""
                        formatadas.append(f"{col}{tag}")

                    print(f" {icone} {nome_obj.capitalize()}({', '.join(formatadas)})")
                print("-" * 80)

            imprimir_objetos('BASE TABLE', 'ESQUEMA RELACIONAL (TABELAS FÍSICAS)', '[✔]')
            print()
            imprimir_objetos('VIEW', 'CAMADA DE VISÃO (VIEWS)', '[★]')

    except Exception as erro:
        print(f"\n[FALHA NA INSPEÇÃO]: {erro}")
    finally:
        conn.close()

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
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" * 2)
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