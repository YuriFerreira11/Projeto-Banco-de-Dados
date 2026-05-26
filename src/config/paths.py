from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

CONFIG_PATH = BASE_DIR / "config.yaml"

SRC_PATH = BASE_DIR / "src"

MIGRATIONS_PATH = SRC_PATH / "migrations"

CREATE_TABLES_PATH = (
    MIGRATIONS_PATH / "create_tabbles.sql"
)

CREATE_VIEWS_PATH = (
    MIGRATIONS_PATH / "create_views.sql"
)