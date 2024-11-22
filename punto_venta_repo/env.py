from alembic import context
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# noinspection PyUnresolvedReferences
from punto_venta_repo.operations import *

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from punto_venta_app.orm import Base as orm_base, tables_shortnames

target_metadata = orm_base.metadata


def table_shortname(constraint, table):
    if len(table.name) > 10 and table.name in tables_shortnames:
        return tables_shortnames.get(table.name)

    return table.name


# naming conventions
target_metadata.naming_convention = {
    "table_shortname": table_shortname,
    "ix": "ix_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_shortname)s_%(column_0_name)s",
    "pk": "pk_%(table_name)s",
}


def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table":
        # object is not view
        return not object.info.get('is_view', False)
    else:
        return True


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_object=include_object,
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
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
