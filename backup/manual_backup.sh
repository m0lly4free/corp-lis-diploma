#!/bin/bash

netstat -ano | findstr :8000
taskkill /PID 6616 /F

# Ручной запуск резервного копирования
docker exec -e PGPASSWORD=corp_lis_pass corp_lis_web /app/backup/backup.sh


### БД ЧАСТЬ ###
# Копироваие БД для *.sql (убедись, что контейнер БД запущен "docker-compose up -d db") ```SQL ДАМП```
docker exec corp_lis_db pg_dump -U corp_lis_user -d corp_lis -F p > corp_lis_backup.sql 

# 1. Запусти только контейнер базы данных
docker-compose up -d db
# 2. Восстанови базу из SQL-файла
Get-Content .\corp_lis_backup.sql | docker exec -i corp_lis_db psql -U corp_lis_user -d corp_lis
# 3. Проверь, что таблицы создались
docker exec -it corp_lis_db psql -U corp_lis_user -d corp_lis -c "\dt"
### Если в выводе \dt ты видишь список таблиц (news, services, auth_user и т.д.), то данные успешно перенесены маладец...

# Запусти контейнеры и сделай миграции
docker-compose up -d
docker exec -it corp_lis_web python manage.py migrate

# Примени миграции (на всякий случай)
docker exec -it corp_lis_web python manage.py migrate

# Создай суперпользователя (если при заходе в админ панель админа нет)
docker exec -it corp_lis_web python manage.py createsuperuser


### ОСАЛЬНОЕ (АРХИВ) ###

# Распакоука архива
# Перейди в папку backups
cd backups
# Распакуй
tar -xzf backup_2026-05-18_13-13-44.tar.gz
 ### ДЛЯ ДАМПА БД ИСПОЛЬЗУЙ ВАРИАНТ ВЫШЕ
# Скопируй медиа из распакованной папки
Copy-Item .\media_2026-05-18_13-13-44\* corp_lis\media\ -Recurse -Force
# Либо же вручную в папку corp_lis/media если будет ошибк

