# Compliment App

Веб API для регистрации пользователей и выдачи комплиментов. Проект использует
FastAPI, асинхронный SQLAlchemy, PostgreSQL и Alembic. Зависимости управляются
Poetry; требуется Python 3.12.

## Запуск через Docker Compose

1. Создайте `.env` на основе `.env.example`. Укажите свои значения
   `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` и `SECRET_KEY`. Для запуска
   в Compose задайте `POSTGRES_HOST=db` и `POSTGRES_PORT=5432` — это адрес БД
   внутри сети контейнеров. Не добавляйте `.env` в Git.
2. Запустите приложение:

   ```bash
   docker compose up --build -d
   ```

Compose поднимает PostgreSQL, выполняет `alembic upgrade head` в сервисе
`migrate` и после успешной миграции запускает API. Документация Swagger доступна
по адресу <http://localhost:8000/docs>, а OpenAPI-схема — по
<http://localhost:8000/openapi.json>. Для остановки используйте
`docker compose down` (данные БД остаются в именованном томе `postgres_data`).

## Возможности API

Маршруты определены в `src/routers/`:

| Метод и путь | Назначение |
| --- | --- |
| `POST /users/register` | Регистрация пользователя |
| `POST /auth/login/jwt` | Вход и получение пары токенов |
| `GET /auth/tokens/refresh` | Обновление пары токенов; запрос принимает `refresh_token` в теле |
| `GET /compliments/data/all` | Список комплиментов |
| `GET /compliments/data/random/{user_id}` | Случайный комплимент для пользователя |
| `GET /compliments/history/{user_id}` | История пользователя |
| `PUT /compliments/data/{compliment_id}` | Обновление комплимента |
| `GET /compliments/test` | Проверка соединения с БД |

Тело запросов и ответы удобнее посмотреть в `/docs`. После первой миграции БД
может быть пустой: маршрут загрузки комплиментов из файла сейчас закомментирован.

## Разработка и тесты

Код разделён на маршруты (`src/routers/`), бизнес-логику (`src/auth/`,
`src/users/`, `src/compliments/`) и репозитории для работы с БД. Миграции
находятся в `src/migrations/`, интеграционные тесты — в
`src/tests/integration_tests/`.

Для локального запуска тестов нужны Docker Compose, Poetry и Python 3.12.
Установите зависимости командой `poetry install`, затем выполните:

```bash
make test
make test-down
```

`make test` запускает отдельную тестовую БД на порту 5434 и выполняет pytest;
фикстуры применяют миграции к тестовой БД. `make test-down` удаляет тестовый
контейнер. Параметры тестового подключения находятся в `tests.env`.

## CI/CD

Описание GitHub Actions, публикации образов в GHCR и настройки работы через
pull request: [CI/CD](docs/ci-cd.md).
