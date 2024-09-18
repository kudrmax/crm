#!/bin/bash

# Скрипт восстанавливает последний бекап из папки ../backups


# Определите переменные
CONTAINER_NAME="crm"
BACKUP_DIR="../backups"
BACKUP_FILE=$(ls -t $BACKUP_DIR/*.dump | head -n 1)
BACKUP_FILE_NAME=$(basename $BACKUP_FILE)
BACKUP_DIR_IN_CONTAINER="/backups"

# Проверьте, что бекап существует
if [ -z "$BACKUP_FILE" ]; then
    echo "No backup files found."
    exit 1
fi

# Остановите и удалите контейнер, если он запущен
docker stop $CONTAINER_NAME
docker rm $CONTAINER_NAME

# Запустите новый контейнер с базой данных
docker-compose up -d db

# Создайте директорию для бекапов в контейнере
docker exec -t $CONTAINER_NAME mkdir -p $BACKUP_DIR_IN_CONTAINER

# Скопируйте бекап в контейнер
docker cp $BACKUP_FILE $CONTAINER_NAME:$BACKUP_DIR_IN_CONTAINER/crm_backup.dump

# Восстановите базу данных из бекапа
docker exec -t $CONTAINER_NAME pg_restore -U postgres -d crm -v $BACKUP_DIR_IN_CONTAINER/crm_backup.dump

# Удалите бекап из контейнера после восстановления
docker exec -t $CONTAINER_NAME rm $BACKUP_DIR_IN_CONTAINER/crm_backup.dump

echo "Restore completed from $BACKUP_FILE_NAME"
