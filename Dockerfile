Выбери базовый образ Python (например, FROM python:3.9-slim).

Установи рабочую директорию (WORKDIR /app).

Скопируй requirements.txt и установи зависимости (RUN pip install ...).

Скопируй весь твой код (COPY . .).

Определи команду для запуска по умолчанию (CMD [ "python", "main.py" ]).