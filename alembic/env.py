from logging.config import fileConfig
from sqlalchemy import pool
from alembic import context
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config

import os
from dotenv import load_dotenv
load_dotenv()

# Эта строка нужна, если у тебя есть metadata в models.py
from app.models import Base

config = context.config

# Загружаем URL из .env или переменных среды
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:admin@db:5432/fastapi_finance")
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Логгинг
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Async run
def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
