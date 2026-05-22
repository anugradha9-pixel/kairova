from logging.config import fileConfig
import os

from sqlalchemy import engine_from_config, pool
from alembic import context

from backend.db.base import Base

# Import models so Alembic detects tables
from backend.auth import models as auth_models
from backend.creator import models as creator_models

config = context.config

# ======================================================
# DATABASE URL (SAFE FALLBACK)
# ======================================================
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:successproject@postgres:5432/kairova"
)

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ======================================================

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ======================================================
# ENTRYPOINT
# ======================================================
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

print("Running migrations with DB:", DATABASE_URL)