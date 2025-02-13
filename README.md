```
backend
├─ .env
├─ .venv
│  ├─ bin
│  ├─ lib
├─ api
│  ├─ __init__.py
│  ├─ database.py
│  ├─ models.py
│  ├─ schemas.py
│  ├─ urls.py
│  └─ views.py
├─ main.py
└─ requirement.txt

```

cli for generation random key
openssl rand -hex 32

cli for migration - baka makalimutan ko
alembic revision --autogenerate -m {message for migration}
alembic upgrade head
alembic check

TODO (later): Add websocket and make code cleaner
