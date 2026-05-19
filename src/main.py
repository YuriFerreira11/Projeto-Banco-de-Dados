import os
import yaml

# Descobre o caminho absoluto para a pasta 'src' de forma dinâmica
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_CONFIG = os.path.join(BASE_DIR, "config.yaml")


def carregar_configuracao():
    """Lê o arquivo yaml de configuração na inicialização do sistema."""
    if not os.path.exists(PATH_CONFIG):
        raise FileNotFoundError(f"Arquivo '{PATH_CONFIG}' não encontrado.")

    with open(PATH_CONFIG, "r", encoding="utf-8") as arquivo:
        config = yaml.safe_load(arquivo)
    return config


if __name__ == "__main__":
    try:
        # Garante que o arquivo de configuração está legível antes de iniciar o app
        configuracao = carregar_configuracao()

        # Estado atual do desenvolvimento do app principal
        print("Em progresso..")

    except Exception as erro:
        print(f"Erro na inicialização do sistema: {erro}")