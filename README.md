# QRkot - Фонд помощи котам

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Стек технологий
- Python 3.9
- FastAPI
- SQLAlchemy

### Установка
- Скачать проект:
```
git clone git@github.com:Saida3232/cat_charity_fund.git
```
- Перейти в директорию с проектом:
```
cd cat_charity_fund/
```
- Создать и активировать виртуальное окружение:
```
python3 -m venv venv
venv/source/activate
```

- Установить зависимости:
```
pip install -r requirements.txt
```
- Заполните файл `.env` с настройками:
```
APP_TITLE='Благотворительный фонд поддержки котиков QRKot'

APP_DESCRIPTION = 'мяууу'

DATABASE_URL=sqlite+aiosqlite:///./fastapi.db

SECRET = 'code'
```
- Создать и применить миграции для создания БД:
```
alembic revision --avtogenerate
alembic upgrade head
```
- Запустить приложение:
```
uvicorn app.main:app
```
Документация API будет доступна по адресу:
```
http://127.0.0.1:8000/docs
```