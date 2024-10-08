# REST API и Telegram бот для управления личными контактами

### Функционал

1. **Записная книга**: cохранение информации о контактах (имя, телефон, день рождения и т.д.)
2. **Заметки**: ведение заметок после встречи с человеком (записать что было на встрече, записать что актуального в
   жизни человека, чем он увлекается и т.д.)
3. **Статистика**: поиск людей, с которыми давно не виделся, а стоило бы, и прочая статистика

### Технологии

- **Backend**: `Python`, `FastAPI`, `SQLAlchemy`, `Pydantic`
- **Telegram Bot**: `Aiogram`, `Requests`
- **База данных**: `PostgreSQL`, `Docker`
- **Общее**: `Pytest`, `Alembic`

### Архитектура

Проект разделен на два независимых компонента:

**Backend**: Написан на `FastAPI` и представляет собой API для хранения и обработки данных контактов. Его можно
использовать не только для бота, но и для других интерфейсов, например для веб-приложения.

![](/docs/swagger.png)

**Telegram Bot**: Реализован через `Aiogram`. Он взаимодействует с backend через HTTP-запросы. Бот может быть
заменен другим клиентом (например, web-интерфейсом), не затрагивая работу backend.

![](/docs/bot.png)

### Что реализовано

- Backend: [REST API](src/api)
    - UNIT-тестирование API через [Pytest](src/api/tests)
    - Автосгенерированный Swagger: [в будущем будет ссылка]().
    - Взаимодействие с базой данных через SQLAlchemy.
- Клиент: [Telegram bot](src/bot)
    - Асинхронный расширяемый код.
    - Обработка ошибок при которой (по идее) бот никогда не упадет (в худшем случае выйдет в главное меню).
- База данных
    - Поднятие PostgreSQL через [docker compose](docker-compose.yaml).
    - Миграции базы данных через [Alembic](src/migrations).
    - Бекапы базы данных:
        - Автоматические бекапы через [docker compose](docker-compose.yaml).
        - Ручные бекапы через [.sh скрипты](backup_scripts).
    - Подключение к БД через переменные окружения и [pydantic-settings](src/settings.py).

## Использование

### Для использования

Открыть бота в телеграм: [в будущем будет ссылка на бота]()

### Для разработчиков

Подготовка

```bash
# склонировать репозиторий
git clone https://github.com/kudrmax/crm
cd crm

# установить виртуальное окружение и зависимости
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

Настроить переменные окружения (в файл .env). Следующие переменные должны быть обязательно установлены:

```dotenv
# Значения приведены для примера. У вас могут быть другие.

SERVER_HOST=0.0.0.0
SERVER_PORT=8000

BOT_TOKEN=... # создайте своего бота в Telegram и получите токен

# для основной базы данных
POSTGRES_HOST=0.0.0.0
POSTGRES_HOST_PORT=5500
POSTGRES_OUTER_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=...
POSTGRES_DATABASE=crm

# для базы данных для тестов
POSTGRES_TEST_HOST=0.0.0.0
POSTGRES_TEST_HOST_PORT=5501
POSTGRES_TEST_OUTER_PORT=5432
POSTGRES_TEST_USER=postgres_test
POSTGRES_TEST_PASSWORD=...
POSTGRES_TEST_DATABASE=crm_test
```

Поднять базу данных:

```shell
# поднять PostgreSQL
make db_up  # установите make если не установлен

# применить миграции
alembic upgrade head  # установите alembic если не установлен
```

Запустить сервер для beckend:

```shell
make backend_up
```

Запустить сервер для Telegram бота:

```shell
make bot_up
```

Как остановить сервер:

```bash
# остановить базу данных
make db_down

# остановить сервер для backend
CTRL+C

# остановить сервер для бота
CTRL+C
```

## Планируемые функции

- [x] **Backend**: REST API на FastAPI.
- [x] **Клиент**: Telegram бот, который использует backend.
- [ ] Добавить авторизацию и пользователей.
- [ ] Захостить бота на сервер.

## Автор

**Макс Кудряшов**: [Telegram](https://t.me/kudrmax)
