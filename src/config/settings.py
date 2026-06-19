import yaml
from src.config.paths import CONFIG_PATH

with CONFIG_PATH.open("r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

DATABASE_CONFIG = config["database"]
