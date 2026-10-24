from logging.config import fileConfig  
from alembic import context
from sqlalchemy import engine_from_config, pool
from models.comp_models import User,BDBase  # noqa: F401
from core.db_config import db_settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)
    
dburl = db_settings.db_url.update_query_dict({"async_fallback":"true"})
# Дело в том, что базовый URL функция не принимает и поэтому приходится парсить url как строку. +"?async_fallback = True"
config.set_main_option("sqlalchemy.url",dburl.render_as_string(hide_password=False).replace("%","%%"))
target_metadata = BDBase.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url",dburl.render_as_string(hide_password=False).replace("%","%%"))
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
