FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry
# перебрасываю зваисимости в рабочую папку
COPY poetry.lock pyproject.toml /app/
# отключаю создание виртуального окружения
RUN poetry config virtualenvs.create false
# скип всез соглашалок 
RUN poetry install --no-root --no-interaction

COPY . /app/

EXPOSE 8888
# запускаю poetry скрипт на поднятие бд, само приложение 
CMD ["poetry","run","sh", "-c", "python scripts/init_db.py && uvicorn src.main:app --host 0.0.0.0 --port 8888"]

#Старая версия 
# CMD [ "poetry","run","uvicorn","src.main:app","--host","0.0.0.0","--port","8888" ]