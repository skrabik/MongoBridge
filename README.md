# REST FastAPI MongoDB Service

Простой REST-сервис на FastAPI для приёма данных от стороннего сервиса и сохранения их в MongoDB. Сервис предоставляет CRUD-роуты над сущностью "record" с произвольным полем `payload` (словарь).

В проекте предусмотрены два варианта запуска: локально (без Docker) и в Docker. Подключение к MongoDB настраивается через переменные окружения.

Важно: базовый образ Docker использует Python 3.13.7. Для локального запуска рекомендуем Python 3.13.7 (или совместимый 3.13.x).

## Структура проекта

```
RESTfastApiMongoDBservice/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ settings.py
│  ├─ db.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  └─ record.py
│  ├─ repositories/
│  │  ├─ __init__.py
│  │  └─ records.py
│  └─ routers/
│     ├─ __init__.py
│     └─ records.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ .dockerignore
```

## Переменные окружения

Создайте файл `.env` в корне проекта со значениями, например:

```
MONGODB_URI=mongodb://difyroot:6HOyGG3ulHK8pfZEJq9VNTybiU4Mjlbg@91.84.112.250:27776/?authMechanism=SCRAM-SHA-256&tls=true&tlsCAFile=mongodb-cert.key&tlsCertificateKeyFile=mongodb.pem&tlsInsecure=true
MONGODB_DB=app
MONGODB_COLLECTION=records
APP_HOST=0.0.0.0
APP_PORT=8000
LOG_LEVEL=info
```

Примечания по TLS:
- Для Docker положите файлы сертификатов `mongodb-cert.key` и `mongodb.pem` в папку `./certs`. Compose примонтирует их в контейнер по путям `/app/mongodb-cert.key` и `/app/mongodb.pem`.
- Для локального запуска положите эти файлы в корень проекта (рядом с `app/`) или измените пути в `MONGODB_URI` на абсолютные Windows-пути (например, `C:\\path\\to\\mongodb-cert.key`). При `tlsInsecure=true` указание файлов может быть не обязательно (менее безопасно).

Если создание `.env.example` в вашей среде ограничено, используйте пример выше для ручного создания `.env`.

## Локальный запуск (без Docker)

Требуется Python 3.13.x. Пример для PowerShell (Windows 11):

```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt

$env:APP_HOST="127.0.0.1"  # опционально
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Проверка:

```
curl http://localhost:8000/api/v1/records
```

## Запуск в Docker

1) Создайте `.env` в корне (см. раздел выше)
2) Поместите сертификаты MongoDB в папку `./certs` (если требуются по URI)
3) Запуск:

```
docker compose up --build -d
```

Откройте `http://localhost:8000/docs` для Swagger UI.

## API

- POST `/api/v1/records` — создать запись. Тело:
  ```json
  { "payload": { "any": "data" } }
  ```
- GET `/api/v1/records/{id}` — получить запись
- GET `/api/v1/records?skip=0&limit=50` — список
- PATCH `/api/v1/records/{id}` — обновить запись (partial), тело как у create
- DELETE `/api/v1/records/{id}` — удалить запись

Ответы содержат поля: `id`, `payload`, `created_at`, `updated_at`.

