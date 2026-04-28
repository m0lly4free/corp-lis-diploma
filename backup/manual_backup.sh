#!/bin/bash

# Ручной запуск резервного копирования
docker exec -e PGPASSWORD=corp_lis_pass corp_lis_web /app/backups/backup.sh