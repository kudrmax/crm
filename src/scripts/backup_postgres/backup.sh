#!/bin/bash

# Скрипт делает бекап в папке ../backups

# Определите переменные
CONTAINER_NAME="crm"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="../backups/crm_backup_$TIMESTAMP.dump"
BACKUP_DIR="/backups"

# Создайте директорию для бекапов в контейнере
docker exec -t $CONTAINER_NAME mkdir -p $BACKUP_DIR

# Выполните бекап базы данных
docker exec -t $CONTAINER_NAME pg_dump -U postgres -F c -b -v -f $BACKUP_DIR/crm_backup.dump crm

# Скопируйте бекап из контейнера на хост
docker cp $CONTAINER_NAME:$BACKUP_DIR/crm_backup.dump $BACKUP_FILE

# Удалите бекап из контейнера после копирования
docker exec -t $CONTAINER_NAME rm $BACKUP_DIR/crm_backup.dump

echo "Backup completed and saved to $BACKUP_FILE"
