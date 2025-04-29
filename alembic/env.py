from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
from app.models import Category, Transaction, User

# читаем alembic.ini
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# читаем основной url из ini-файла
db_url = config.get_main_option("sqlalchemy.url")

# проверяем, был ли передан db_url через -x
x_args = context.get_x_argument(as_dictionary=True)
if "db_url" in x_args:
    db_url = x_args["db_url"]

# подставляем URL в конфиг
config.set_main_option("sqlalchemy.url", db_url)

# метаданные для автогенерации
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
