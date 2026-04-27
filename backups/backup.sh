#!/bin/sh

# Конфигурация
BACKUP_DIR="/app/backups"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
DB_NAME="corp_lis"
DB_USER="corp_lis_user"
DB_HOST="db"
DB_PORT="5432"
DB_PASSWORD="corp_lis_pass"

# Установка переменной окружения для пароля
export PGPASSWORD="$DB_PASSWORD"

# Создание директории для бэкапов
mkdir -p "$BACKUP_DIR"

# Создание временной директории
TEMP_DIR="/tmp/backup_$DATE"
mkdir -p "$TEMP_DIR"

echo "[$(date)] Начало резервного копирования..."

# 1. Резервное копирование базы данных PostgreSQL
echo "[$(date)] Создание дампа базы данных..."
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -F c -f "$TEMP_DIR/database_$DATE.dump"

if [ $? -eq 0 ]; then
    echo "[$(date)] Дамп базы данных успешно создан"
else
    echo "[$(date)] Ошибка при создании дампа базы данных"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 2. Резервное копирование медиа-файлов
echo "[$(date)] Копирование медиа-файлов..."
cp -r /app/media "$TEMP_DIR/media_$DATE"

if [ $? -eq 0 ]; then
    echo "[$(date)] Медиа-файлы успешно скопированы"
else
    echo "[$(date)] Ошибка при копировании медиа-файлов"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 3. Создание архива
echo "[$(date)] Создание архива..."
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" -C "$TEMP_DIR" .

if [ $? -eq 0 ]; then
    echo "[$(date)] Архив успешно создан: backup_$DATE.tar.gz"
else
    echo "[$(date)] Ошибка при создании архива"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 4. Очистка временных файлов
rm -rf "$TEMP_DIR"

# 5. Удаление старых бэкапов (старше 7 дней)
echo "[$(date)] Очистка старых бэкапов..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

if [ $? -eq 0 ]; then
    echo "[$(date)] Старые бэкапы удалены"
else
    echo "[$(date)] Ошибка при удалении старых бэкапов"
fi

echo "[$(date)] Резервное копирование завершено успешно!"