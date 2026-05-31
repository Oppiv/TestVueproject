# Импортируем типы данных для колонок: String – строка, Integer – целое число
from sqlalchemy import String, Integer
# Mapped – подсказка типа для колонок, mapped_column – для определения колонок
from sqlalchemy.orm import Mapped, mapped_column
# Base – наш базовый класс из session.py (через него модель будет знать о движке)
from src.session import Base


# Класс Labubu, который наследуется от Base – это одна таблица в базе данных
class Labubu(Base):
    # __tablename__ задаёт имя таблицы в базе
    __tablename__ = 'labubu'

    # Колонка id: целое число, первичный ключ, автоинкремент (значение автоматически увеличивается)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Колонка name: строка, не может быть NULL (nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    # Колонка description: строка, тоже не может быть NULL
    description: Mapped[str] = mapped_column(String, nullable=False)
