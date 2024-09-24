FROM python:3.12-alpine

WORKDIR /yandex_disk

COPY ./src/backup_to_yandex_disk/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/backup_to_yandex_disk/ ./backup_to_yandex_disk/