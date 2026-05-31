# Pydantic BaseModel – базовый класс для создания схем данных
# Field – позволяет добавить описание поля (будет видно в Swagger)
from pydantic import BaseModel, Field


# Схема Labubu – описывает, какие поля мы ожидаем от клиента (или возвращаем)
class Labubu(BaseModel):
    name: str = Field(description="Название")             # имя – строка
    description: str = Field(description="Описание")      # описание – строка

class LabubuUpdate(BaseModel):
    name: str | None
    description: str | None