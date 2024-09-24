import os

import yadisk

from src.settings import settings

client = yadisk.Client(token=settings.yandex_disk.token)


def load_backup_file_to_disk(file_path: str):
    if not client.check_token():
        raise Exception("Yandex disk token is invalid")
    file_name = file_path.split("/")[-1]
    try:
        client.upload(file_path, f"Backups/CRM/{file_name}")
    except Exception as e:
        print(f'Error with {file_path}.')
        print(e)
    print(f'File {file_path} has been uploaded')


def find_all_backup_files(backups_dir):
    dump_files = []
    for filename in os.listdir(backups_dir):
        if filename.endswith('.dump'):
            dump_files.append(filename)
    return dump_files


def load_all_backup_files_to_disk(backups_dir: str):
    for backup_file_name in find_all_backup_files(backups_dir):
        load_backup_file_to_disk(backups_dir + '/' + backup_file_name)


if __name__ == "__main__":
    load_all_backup_files_to_disk('../../backups')
