# Импортируем всё необходимое для асинхронного SQLAlchemy:
# AsyncEngine – движок для асинхронной работы с БД
# AsyncSession – асинхронная сессия (аналог соединения с транзакцией)
# async_sessionmaker – фабрика для создания сессий
# create_async_engine – функция для создания асинхронного движка
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
# DeclarativeBase – базовый класс для декларативных моделей таблиц
from sqlalchemy.orm import DeclarativeBase

# Импортируем объект с настройками settings
from src.config import settings

# Проверяем, что асинхронный URL для подключения к БД задан
if settings.DB.SQLALCHEMY_DATABASE_URI_ASYNC is None:
    raise Exception('Failed to get SQLALCHEMY_DATABASE_URI_ASYNC')

# Создаём асинхронный движок (engine) – отвечает за низкоуровневое общение с БД
engine: AsyncEngine = create_async_engine(url=settings.DB.SQLALCHEMY_DATABASE_URI_ASYNC)

# Создаём фабрику сессий – она будет выдавать сессии, когда они понадобятся
# expire_on_commit=False – после коммита не делать объекты "устаревшими" (удобно при использовании вне контекста)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, expire_on_commit=False)


# Базовый класс для всех моделей таблиц (их мы определим в tables.py)
class Base(DeclarativeBase):
    pass  # pass означает "ничего не делаем", просто наследуем функциональность


# Функция-генератор, которая будет использоваться как зависимость (Depends)
# FastAPI будет автоматически создавать сессию и передавать в эндпоинты
async def get_session() -> AsyncSession:
    # async with создаёт асинхронный контекстный менеджер сессии
    # сессия автоматически закроется после выхода из блока with
    async with async_session_maker() as session:
        yield session  # yield возвращает сессию и приостанавливает функцию до её использования