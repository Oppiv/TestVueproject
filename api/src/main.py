# uvicorn – сервер, который запустит наше приложение
import uvicorn
# FastAPI – фреймворк для создания веб-приложений
from fastapi import FastAPI

# Импортируем роутер из нашего пакета src.router (файл router.py) и называем labubu_router
from src.router import router as labubu_router

# Создаём экземпляр FastAPI – это и есть наше приложение
# openapi_url – адрес, по которому будет доступна автоматическая документация OpenAPI
# docs_url – адрес интерфейса Swagger
app = FastAPI(
    openapi_url=f"/openapi.json",
    docs_url=f"/docs",
)

# Подключаем маршруты роутера к приложению
app.include_router(labubu_router)

# Если файл запущен напрямую (python main.py), то стартуем сервер
if __name__ == "__main__":
    uvicorn.run(
        'src.main:app',          # путь к приложению: "папка.файл:переменная"
        host='localhost',        # слушаем только локальные подключения
        port=8000,               # порт
        reload=True,             # авто-перезагрузка при изменениях
    )