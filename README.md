# Travely API

Django API для локацій, JWT авторизації, постів і головних фото міст.

## Локальний запуск

Скопіюйте `.env.sample` у `.env`, задайте власний `DJANGO_SECRET_KEY`, потім:

```bash
make up
```

API буде на `http://localhost:8000/api/`, документація — на `http://localhost:8000/swagger/`. Docker запускає PostgreSQL, виконує міграції та зберігає завантажені фото у volume `media_data`. `make shell` відкриває Django shell.

## Нові маршрути

- `POST /api/register/` — реєстрація.
- `POST /api/token/`, `POST /api/token/refresh/`, `POST /api/token/blacklist/` — JWT.
- `GET /api/city-posts/?city=Львів` — пости міста. `POST` додає пост, `PATCH /api/city-posts/<id>/` змінює власний пост.
- `GET /api/city-covers/?city=Львів` — головне фото міста. `POST` додає фото, `PATCH /api/city-covers/<id>/` змінює фото його автора.

Для запису передайте `Authorization: Bearer <access>`. Фото завантажуйте як `multipart/form-data`; максимальний розмір — 8 МБ. Читання постів і фото відкрите без входу. Старий `/api/login/` залишено для існуючих клієнтів.

Для продакшну потрібне постійне сховище медіафайлів: локальний Docker volume працює на одному сервері, а тимчасова файлова система serverless середовища не збереже фото між запусками.
