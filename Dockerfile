FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    postgresql-client \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Установка директорий
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копирование проекта
COPY . /app/

# Создание директории для бэкапов
RUN mkdir -p /app/backups

# Копирование скрипта резервного копирования
COPY backup/backup.sh /app/backup.sh
RUN chmod +x /app/backup.sh

# Настройка cron для автоматического резервного копирования
RUN echo "0 2 * * * /app/backup.sh >> /app/backups/backup.log 2>&1" | crontab -

# Экспозиция порта
EXPOSE 8000

# Запуск сервера
CMD service cron start && python manage.py runserver 0.0.0.0:8000

