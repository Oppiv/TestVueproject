# APIRouter – группировка маршрутов
# Depends – инструмент для внедрения зависимостей (например, сессии БД)
# HTTPException – ошибка, которую можно вернуть клиенту
from fastapi import APIRouter, Depends, HTTPException
# AsyncSession – тип асинхронной сессии
from sqlalchemy.ext.asyncio import AsyncSession
# select и delete – конструкции SQL-запросов в SQLAlchemy
from sqlalchemy import select, delete, update

# Импортируем Pydantic-схему Labubu (называем её Schema, чтобы не путать с моделью таблицы)
from src.schema import Labubu as Schema
from src.schema import LabubuUpdate as UpdateSchema
# Импортируем модель таблицы Labubu (назовём Table)
from src.tables import Labubu as Table
# Импортируем движок engine (хотя не используется в этом файле, можно убрать)
# и функцию get_session, которая будет создавать сессии для каждого запроса
from src.session import engine, get_session

# Повторный импорт (на самом деле уже есть строчкой выше), можно оставить как есть
from src.session import get_session

# Создаём роутер с префиксом '/labubu' – все адреса будут начинаться с '/labubu'
router = APIRouter(prefix='/labubu')


# Получить список всех лабубу (GET /labubu/get_list)
@router.get('/get_list')
# async def – асинхронная функция обработчика
# db_session: AsyncSession – параметр, который FastAPI автоматически заполнит через Depends
async def get_list(db_session: AsyncSession = Depends(get_session)):
    # Строим SQL-запрос SELECT * FROM labubu
    query = select(Table)
    # Выполняем запрос асинхронно
    query_result = await db_session.execute(query)
    # scalars() извлекает строки как объекты Table, all() собирает все в список
    return query_result.scalars().all()
 

# Получить лабубу по имени (GET /labubu/get/имя)
@router.get('/get/{name}')
# name: str – параметр пути из URL
async def get(name: str, db_session: AsyncSession = Depends(get_session)):
    # Добавляем условие WHERE name = :name
    query = select(Table).where(Table.name == name)
    query_result = await db_session.execute(query)
    # first() возвращает первый результат или None, если не найдено
    return query_result.scalars().first()


# Создать нового лабубу (POST /labubu/create)
@router.post('/create')
# data: Schema – FastAPI преобразует JSON-тело запроса в объект схемы Labubu
async def create(data: Schema, db_session: AsyncSession = Depends(get_session)):
    # Создаём объект модели таблицы Table, распаковывая поля из схемы (name, description)
    new_user = Table(**data.model_dump())   # model_dump() -> {"name": ..., "description": ...}
    # Добавляем объект в сессию (пока не в БД)
    db_session.add(new_user)
    # Фиксируем транзакцию (реально выполняем INSERT)
    await db_session.commit()
    # Возвращаем созданного лабубу (клиент увидит его, включая id)
    return new_user

@router.put('/update/{id}')
async def _update(id: int,data: UpdateSchema, db_session: AsyncSession = Depends(get_session)):
    query = update(Table).where(Table.id == id).values(**data.model_dump(exclude_unset=True))
    await db_session.execute(query)
    await db_session.commit()
    return 'Успех ура ура ура'



# Удалить лабубу по ID (DELETE /labubu/delete/{id})
@router.delete('/delete/{id}')
# id: int – параметр из пути
async def delete_(id: int, db_session: AsyncSession = Depends(get_session)):
    # Строим запрос DELETE FROM labubu WHERE id = :id
    query = delete(Table).where(Table.id == id)
    try:
        # Выполняем запрос
        await db_session.execute(query)
        # Фиксируем удаление
        await db_session.commit()
        return 'Удалено'
    except Exception:
        # Если что-то пошло не так (например, нет строки с таким id), кидаем 404 ошибку
        raise HTTPException(404, 'Не смог удалить лабубу')
