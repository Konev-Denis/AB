# hw

ДЗ Академия Бэкенда 22/23. Python

Используються: Python, fast-api, Dockerfile, Postgresql, alembic

Если вдруг что, то для swagger нужно запустить тест `make run` и перейти по ссылке http://localhost:8000/docs

## Docker

### Первый способ

Настроить docker-compose.yaml и запустить приложение командой: `docker-compose up`

### Второй способ

Собрать Image командой `docker build --build-arg APP_PORT=8050 -t APP .` APP_PORT - это порт контейнера.

И запустить контейнер командой `docker run -dp 8000:8050 --env-file ./.env APP`
