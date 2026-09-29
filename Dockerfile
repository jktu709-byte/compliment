# Образ - выступающий в качества фундамента
FROM python:3.12
# Создаем рабочую папку внутри изолированного процесса
WORKDIR /app
# Устанавливаю poetry
RUN pip install --no-cache-dir poetry==1.8.2
# перебрасываю зваисимости в рабочую папку
COPY poetry.lock pyproject.toml /app/
# отключаю создание виртуального окружения
RUN poetry config virtualenvs.create false
# скип всех согласований 
RUN poetry install --no-root --no-interaction -vvv
# Копирование контекста
COPY . /app/
# Информация на каком порту крутится приложение
EXPOSE 8000
# запускаю poetry скрипт на поднятие бд, само приложение
CMD ["poetry", "run", "uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

#Старая версия 
# CMD [ "poetry","run","uvicorn","src.main:app","--host","0.0.0.0","--port","8888" ]