from fastapi import FastAPI
from app.controllers import router

# Создаём приложение
app = FastAPI(title="REST API Lab", description="CRUD с мягким удалением и пагинацией", version="1.0.0")

# Подключаем роутер с эндпоинтами /items
app.include_router(router)

# Простой health-check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Для запуска через python -m app.main (опционально)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)