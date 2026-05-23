# REST API Lab (FastAPI + PostgreSQL + Docker)

## Краткое описание проекта
Проект реализует REST API для управления сущностью `Item` с полным CRUD, мягким удалением (soft delete), пагинацией и валидацией данных. Используется FastAPI, PostgreSQL, SQLAlchemy, Alembic, Docker Compose.

## Инструкция по запуску через `docker-compose up --build`
1. Установите Docker Desktop.
2. Склонируйте или скачайте репозиторий.
3. Создайте файл `.env` на основе `.env.example` (пример ниже).
4. В терминале в папке проекта выполните:
   ```bash
   docker-compose up --build
API будет доступно по адресу: http://localhost:8000/docs

## Пример файла переменных окружения (.env.example)
## Пример файла переменных окружения (`.env.example`)

```ini
DB_USER=student
DB_PASSWORD=change_me
DB_NAME=wp_labs
DB_HOST=postgres
DB_PORT=5432
PORT=8000

#№ Описание API (список эндпоинтов и параметров пагинации)
Эндпоинты:

GET /items/ – список с пагинацией

POST /items/ – создание

GET /items/{id} – получение одного

PUT /items/{id} – полное обновление

PATCH /items/{id} – частичное обновление

DELETE /items/{id} – мягкое удаление

## Параметры пагинации для GET /items/:

page (≥1, по умолч. 1) – номер страницы

limit (1–100, по умолч. 10) – записей на странице

## Пример запроса: 

/items/?page=2&limit=5

## Пример ответа:

json
{
  "data": [ /* массив объектов Item */ ],
  "meta": { "total": 25, "page": 2, "limit": 5, "total_pages": 5 }
}
## Инструкция по запуску миграций
Миграции применяются автоматически при запуске контейнера (через entrypoint.sh). Для ручного управления используйте команды внутри контейнера:

bash
docker exec -it wp_labs_app alembic upgrade head   # применить все миграции
docker exec -it wp_labs_app alembic revision --autogenerate -m "описание"  # создать новую миграцию
Файлы миграций лежат в migrations/versions/ и включены в репозиторий.
