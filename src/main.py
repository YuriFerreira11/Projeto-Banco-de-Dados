import os
import psycopg2
import yaml


def testar_conexao_torneio():
    print("Lendo o arquivo de configuração 'config.yaml'...")

    # 1. Verifica se o arquivo yaml existe antes de tentar abrir
    if not os.path.exists("config.yaml"):
        print(
            "Erro: Arquivo 'config.yaml' não foi encontrado na raiz do projeto."
        )
        return

    # 2. Carrega as credenciais
    with open("config.yaml", "r") as arquivo:
        config = yaml.safe_load(arquivo)
        dados_banco = config["database"]

    print(f"Tentando conectar ao host: {dados_banco['host']}...")

    try:
        # 3. Abre a conexão com o banco do seu PC (via IP do Tailscale)
        conexao = psycopg2.connect(**dados_banco)
        cursor = conexao.cursor()

        # 4. Executa um comando simples (Verifica a hora atual do servidor do banco)
        cursor.execute("SELECT NOW();")
        horario_banco = cursor.fetchone()

        print("\n[CONEXÃO BEM-SUCEDIDA!]")
        print(f"-> Conectado ao banco: {dados_banco['dbname']}")
        print(f"-> Usuário ativo: {dados_banco['user']}")
        print(f"-> Horário do servidor do banco: {horario_banco[0]}")
        print("\nTeste bem sucedido!\n")

        # 5. Fecha os cursores e conexões de forma limpa
        cursor.close()
        conexao.close()
        print("Conexão encerrada com segurança.")

    except Exception as erro:
        print("\nFALHA NA CONEXÃO COM O BANCO DE DADOS:")
        print(erro)
        print(
            "\nDicas de checagem:\n"
            "1. O PostgreSQL está rodando no seu Ubuntu?\n"
            "2. O Tailscale está ativo nas duas máquinas?\n"
            "3. A senha no yaml está correta?"
        )


if __name__ == "__main__":
    testar_conexao_torneio()