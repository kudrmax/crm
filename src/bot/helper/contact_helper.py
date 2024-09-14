import json
from datetime import datetime

import requests
from typing import List, Dict, Any

from src.errors.errors import *
from src.settings import BASE_URL_REQUESTS


class ContactHelper:
    @classmethod
    async def create_contact(cls, name: str):
        response = requests.post(BASE_URL_REQUESTS + '/contacts/new', data=json.dumps({"name": name}))
        if response.status_code == 409:
            raise ContactAlreadyExistsError(name)
        if response.status_code == 200:
            return True
        await cls.raise_if_500(response)

    @classmethod
    async def find_contact_by_name(cls, name: str) -> List[str] | None:
        response = requests.get(f'{BASE_URL_REQUESTS}/contacts/{name}/search')
        await cls.raise_if_500(response)

        contacts = response.json()
        contact_names = [contact['name'] for contact in contacts]
        return contact_names

    @classmethod
    async def update_contact(cls, name: str, field_to_update: str, new_value: Any) -> Dict[str, str] | None:
        field_to_update = field_to_update.lower()

        response = requests.get(f'{BASE_URL_REQUESTS}/contacts/{name}')
        if response.status_code == 404:
            raise ContactNotFoundError
        await cls.raise_if_500(response)

        contact = response.json()
        response = requests.put(
            f'{BASE_URL_REQUESTS}/contacts/{name}',
            data=json.dumps({field_to_update: new_value})
        )
        if response.status_code == 404:
            raise ContactNotFoundError
        if response.status_code == 409:
            raise ContactAlreadyExistsError
        await cls.raise_if_500(response)

        return {
            'field': field_to_update.title(),
            'old_value': contact[field_to_update],
            'new_value': new_value
        }

    @classmethod
    async def print_contact_data(cls, contact: Dict[str, str]) -> str:
        answer = ""
        for key, value in contact.items():
            answer += f"{key}: {value}\n"
        return answer

    @classmethod
    async def get_all_logs(cls, name: str) -> str | None:
        response = requests.get(f'{BASE_URL_REQUESTS}/logs/{name}')
        if response.status_code == 404:
            raise ContactNotFoundError
        await cls.raise_if_500(response)

        logs = response.json()
        result_list = []
        date_set = set()
        for log in logs:
            log_str = log['log']
            log_datetime_str = log['datetime']
            log_datetime_obj = datetime.strptime(log_datetime_str, "%Y-%m-%dT%H:%M:%S.%f")
            log_date_str = f"{log_datetime_obj.date().strftime("%d-%m-%Y")}:"
            if log_date_str not in date_set:
                result_list.append(log_date_str)
                date_set.add(log_date_str)
            result_list.append('- ' + log_str)
        return '\n'.join(result_list)

    @classmethod
    async def add_log(cls, log_str: str, name: str):
        response = requests.post(f'{BASE_URL_REQUESTS}/logs/new', json={
            'name': name,
            'log': log_str
        })
        if response.status_code == 404:
            raise ContactNotFoundError

    @classmethod
    async def get_contact_data_by_name(cls, name: str) -> Dict[str, str] | None:
        response = requests.get(f'{BASE_URL_REQUESTS}/contacts/{name}')
        if response.status_code == 404:
            raise ContactNotFoundError
        contact = response.json()
        return contact

    @classmethod
    async def raise_if_500(cls, response):
        if response.status_code == 500:
            raise InternalServerError

    @classmethod
    async def delete(cls, name: str):
        response = requests.delete(f'{BASE_URL_REQUESTS}/contacts/{name}')
        if response.status_code == 404:
            raise ContactNotFoundError
