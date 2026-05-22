from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

from backend.config.settings import settings
from backend.db.base import Base

# =====================================
# ALEMBIC CONFIG
# =====================================

config = context.config

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# =====================================
# IMPORT ALL MODELS HERE
# (IMPORTANT FOR AUTOGENERATE)
# =====================================

from backend.auth.models import User  # noqa: F401


# =====================================
# TARGET METADATA
# =====================================

target_metadata = Base.metadata


# =====================================
# MIGRATION: OFFLINE MODE
# =====================================

def run_migrations_offline() -> None:
    url = settings.DATABASE_URL

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# =====================================
# MIGRATION: ONLINE MODE
# =====================================

def run_migrations_online() -> None:

    configuration = config.get_section(
        config.config_ini_section,
        {},
    )

    # Force correct DB URL from settings (prevents SQLite drift)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

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


# =====================================
# RUN MODE SWITCH
# =====================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()