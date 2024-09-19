import datetime
import json
from datetime import datetime
from enum import Enum
from uuid import UUID

import requests
from typing import List, Dict, Any, Tuple

from src.errors import *
from src.settings import settings


class RequestType(Enum, str):
    get = 'GET'
    post = 'POST'
    put = 'PUT'
    patch = 'PATCH'
    delete = 'DELETE'


class ContactHelper:

    @classmethod
    async def create_request(self, url: str, request_type: RequestType, data: Dict[str, Any] | None = None):
        response = None
        if request_type == RequestType.get:
            response = requests.get(url)
        elif request_type == RequestType.post:
            response = requests.post(url, data=data)
        elif request_type == RequestType.put:
            response = requests.put(url, data=data)
        elif request_type == RequestType.patch:
            response = requests.patch(url, data=data)
        elif request_type == RequestType.delete:
            response = requests.delete(url, data=data)
        await self.process_errors(response)
        return response

    @classmethod
    async def raise_if_500(cls, response):
        if response.status_code == 500:
            raise InternalServerError(response)

    @classmethod
    async def process_errors(cls, response):
        if response.status_code == 500:
            raise InternalServerError
        if response.status_code == 404:
            raise ContactNotFoundError
        if response.status_code == 409:
            raise ContactAlreadyExistsError
        if response.status_code == 422:
            raise UnprocessableEntityError
        if response.status_code == 200:
            return True
        raise UnknownError

    @classmethod
    async def create_contact(cls, name: str):
        await cls.create_request(
            settings.server.api_url + '/contacts/new',
            RequestType.post,
            {'name': name}
        )

    @classmethod
    async def find_contact_by_name(cls, name: str) -> List[str] | None:
        response = await cls.create_request(
            f'{settings.server.api_url}/contacts/{name}/search',
            RequestType.get
        )

        contacts = response.json()
        contact_names = [contact['name'] for contact in contacts]
        return contact_names

    @classmethod
    async def update_contact(cls, name: str, field_to_update: str, new_value: Any) -> Dict[str, str] | None:
        field_to_update = field_to_update.lower()

        response = await cls.create_request(
            f'{settings.server.api_url}/contacts/{name}',
            RequestType.get
        )

        contact = response.json()

        response = await cls.create_request(
            f'{settings.server.api_url}/contacts/{name}',
            RequestType.put,
            {field_to_update: new_value}
        )

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
    async def get_all_logs_with_numbers(cls, name: str) -> Tuple[str, Dict[int, UUID]]:
        response = await cls.create_request(
            f'{settings.server.api_url}/logs/{name}/by_date',
            RequestType.get
        )
        logs = response.json()['data']
        numbers_to_log_id = response.json()['numbers_to_log_id']
        return await cls.convert_logs_to_str(logs), numbers_to_log_id

    @classmethod
    async def convert_logs_to_str(cls, logs):
        result_list = []
        for data in logs:
            result_list.append(f"\n{str(data['date'])}:")
            for log in data['logs']:
                result_list.append(f"— {log['number']}: {log['log']}")
        return '\n'.join(result_list)

    @classmethod
    async def get_all_logs(cls, name: str) -> str:
        response = await cls.create_request(
            f'{settings.server.api_url}/logs/{name}/by_date',
            RequestType.get
        )
        logs = response.json()['data']
        return await cls.convert_logs_to_str(logs)

    @classmethod
    async def add_log(cls, log_str: str, name: str, date: datetime.date | None = None):
        if not date:
            await cls.create_request(
                f'{settings.server.api_url}/logs/new',
                RequestType.post,
                {
                    'name': name,
                    'log': log_str
                }
            )
        else:
            await cls.create_request(
                f'{settings.server.api_url}/logs/new/{date}',
                RequestType.post,
                {
                    'name': name,
                    'log': log_str
                }
            )

    @classmethod
    async def add_empty_log(cls, name: str):
        response = await cls.create_request(
            f'{settings.server.api_url}/logs/new/empty',
            RequestType.post,
            {'name': name}
        )

    @classmethod
    async def get_contact_data_by_name(cls, name: str) -> Dict[str, str] | None:
        response = await cls.create_request(
            f'{settings.server.api_url}/contacts/{name}',
            RequestType.get,
        )
        contact = response.json()
        return contact

    @classmethod
    async def delete(cls, name: str):
        response = await cls.create_request(
            f'{settings.server.api_url}/contacts/{name}',
            RequestType.delete,
        )

    @classmethod
    async def get_last_contacts(cls):
        response = await cls.create_request(
            f'{settings.server.api_url}/contacts/get_last_contacts',
            RequestType.get,
        )
        return [contact['name'] for contact in response.json()]
