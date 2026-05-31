# Импортируем тип Any – означает «что угодно», пригодится в возврате функций
from typing import Any

# Из Pydantic берём валидатор полей и класс для построения строки подключения к PostgreSQL
from pydantic import field_validator, PostgresDsn
# ValidationInfo даёт доступ к данным, которые пользователь передал в модель
from pydantic_core.core_schema import ValidationInfo
# Из pydantic-settings импортируем базовый класс для настроек и конфигурацию модели
from pydantic_settings import SettingsConfigDict, BaseSettings


# Класс для хранения настроек подключения к БД
class DbSettings(BaseSettings):
    # Конфигурация модели: extra='ignore' – не ругаться на лишние поля в .env,
    # env_file='.env' – читать переменные из файла .env
    model_config = SettingsConfigDict(
        extra='ignore',
        env_file='.env'
    )
    # Параметры PostgreSQL с значениями по умолчанию, если они не указаны в .env
    POSTGRES_SERVER: str = 'localhost'   # адрес сервера БД
    POSTGRES_PORT: int = 5435            # порт
    POSTGRES_USER: str = "postgres"             # пользователь (обязательно указать в .env)
    POSTGRES_PASSWORD: str = "master"            # пароль (обязательно указать в .env)
    POSTGRES_DB: str = "postgres"        # имя базы данных
    POSTGRES_DB_ECHO: bool = True        # выводить SQL-запросы в консоль?

    # Строки подключения – None по умолчанию, они будут собраны автоматически
    SQLALCHEMY_DATABASE_URI: str | None = None          # синхронный URL
    SQLALCHEMY_DATABASE_URI_ASYNC: str | None = None    # асинхронный URL

    # Флаг для профилирования запросов (пока не используется)
    PROFILE_QUERY_MODE: bool = False

    # Валидатор для поля SQLALCHEMY_DATABASE_URI (синхронного)
    # mode='before' – выполняется до стандартной валидации типа
    @field_validator('SQLALCHEMY_DATABASE_URI', mode='before')
    @classmethod  # метод класса (первый аргумент cls, а не self)
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        # Если строка уже задана явно (например, в .env), просто вернём её
        if isinstance(v, str):
            return v

        # Иначе строим URL сами из частей, используя спец. класс PostgresDsn
        return str(PostgresDsn.build(
            scheme='postgresql+psycopg',                # драйвер
            username=info.data.get('POSTGRES_USER'),    # берём пользователя из данных модели
            password=info.data.get('POSTGRES_PASSWORD'),
            host=info.data.get('POSTGRES_SERVER'),
            port=info.data.get('POSTGRES_PORT'),
            path=info.data.get('POSTGRES_DB') or '',    # имя БД, если не указано — пустая строка
        ))

    # Аналогичный валидатор для асинхронного URL
    @field_validator('SQLALCHEMY_DATABASE_URI_ASYNC', mode='before')
    @classmethod
    def assemble_async_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        # Если уже задана строка – возвращаем как есть
        if isinstance(v, str):
            return v

        # В асинхронном варианте просто берём то, что получилось для синхронного URL
        # (в реальном проекте обычно меняют драйвер на asyncpg, но здесь так)
        return info.data.get('SQLALCHEMY_DATABASE_URI')


# Основной класс всех настроек
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        env_file='.env'
    )
    # Базовый путь API (можно использовать в маршрутах, сейчас просто хранится)
    BASE_ROUTE_PATH: str = '/api/v1'
    # Вложенный объект настроек БД
    DB: DbSettings = DbSettings()


# Создаём экземпляр настроек, который будем импортировать в других модулях
settings = Settings()