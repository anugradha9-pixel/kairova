from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from app.config.settings import settings
from app.db.base import Base

# =========================================================
# IMPORT ALL SQLALCHEMY MODELS
# REQUIRED FOR ALEMBIC AUTOGENERATE
# =========================================================

import app.auth.models
import app.auth.session_models
import app.modules.creator.models

import app.modules.product.models
import app.modules.product_cost.models

# =========================================================
# ALEMBIC CONFIG
# =========================================================

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# =========================================================
# DATABASE URL
# =========================================================

def get_url() -> str:
    return settings.DATABASE_URL


# =========================================================
# OFFLINE MIGRATIONS
# =========================================================

def run_migrations_offline() -> None:

    context.configure(
        url=get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# =========================================================
# ONLINE MIGRATIONS
# =========================================================

def run_migrations_online() -> None:

    configuration = config.get_section(
        config.config_ini_section,
    )

    if configuration is None:
        raise RuntimeError(
            "Alembic configuration not found."
        )

    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
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


# =========================================================
# ENTRYPOINT
# =========================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()