import asyncio
import os
import sys
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from dotenv import load_dotenv

# allow alembic to import your app package (adjust if your layout differs)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

# Alembic config
config = context.config
# read DB URL from env or from your Settings module
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # optional: import your Settings class instead of env var
    from app.core.pydantic_settings_config import Settings
    DATABASE_URL = str(Settings.database_url)

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not configured")
# If you want the CLI to show the same URL:
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your Declarative Base and model modules so metadata is populated
from app.models.base import Base
import app.models.user
import app.models.refresh_token

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # helpful to detect column type changes
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is not configured")
    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()