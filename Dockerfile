FROM python:3.13-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false

RUN poetry install --no-root --no-interaction

COPY . /app/

EXPOSE 8888

CMD [ "poetry","run","uvicorn","compliment_app.src.main:app","--host","0.0.0.0","--port","8888" ]