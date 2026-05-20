import yaml

from src.Config.paths import CONFIG_PATH


with CONFIG_PATH.open("r",encoding="utf-8") as ymlfile:
    config = yaml.safe_load(ymlfile)


DATABASE_CONFIG = config["database"]
SECRET_KEY = (
    config["chave_Fernet"]["SECRET_KEY"]
)