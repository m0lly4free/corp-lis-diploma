FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Установка директорий
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копирование проекта
COPY . /app/

# Экспозиция порта
EXPOSE 8000

# Запуск сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]