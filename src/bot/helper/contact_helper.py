import json
from datetime import datetime

import requests
from typing import List, Dict, Any

from src.settings import BASE_URL_REQUESTS


class ContactHelper:
    @classmethod
    async def create_contact(cls, name: str) -> bool | None:
        response = requests.post(BASE_URL_REQUESTS + '/contacts/new', data=json.dumps({"name": name}))
        if response.status_code == 409:
            return False
        return True

    @classmethod
    async def find_contact_by_name(cls, name: str) -> List[str] | None:
        try:
            contacts = (requests.get(f'{BASE_URL_REQUESTS}/contacts/{name}/search')).json()
            contact_names = [contact['name'] for contact in contacts]
            return contact_names
        except Exception as e:
            return None

    @classmethod
    async def update_contact(cls, name: str, field_to_update: str, new_value: Any) -> Dict[str, str] | None:
        field_to_update = field_to_update.lower()
        try:
            print(name, field_to_update, new_value)
            contact = (requests.get(f'{BASE_URL_REQUESTS}/contacts/{name}')).json()
            requests.put(
                f'{BASE_URL_REQUESTS}/contacts/{name}',
                data=json.dumps({field_to_update: new_value})
            )
            return {
                'field': field_to_update.title(),
                'old_value': contact[field_to_update],
                'new_value': new_value
            }
        except Exception as e:
            return None

    @classmethod
    async def get_contact_data_by_name(cls, name: str) -> Dict[str, str] | None:
        try:
            contact = (requests.get(f'{BASE_URL_REQUESTS}/contacts/{name}')).json()
            return contact
        except Exception as e:
            return None

    @classmethod
    async def print_contact_data(cls, contact: Dict[str, str]) -> str:
        answer = ""
        for key, value in contact.items():
            answer += f"{key}: {value}\n"
        return answer

    @classmethod
    async def get_all_logs(cls, name: str) -> str | None:
        try:
            logs = requests.get(f'{BASE_URL_REQUESTS}/logs/{name}')
            result_list = []
            date_set = set()
            for log in logs.json():
                log_str = log['log']
                log_datetime_str: datetime = log['datetime']
                log_datetime_obj = datetime.strptime(log_datetime_str, "%Y-%m-%dT%H:%M:%S.%f")
                log_date_str = f"{log_datetime_obj.date().strftime("%d-%m-%Y")}:"
                if log_date_str not in date_set:
                    result_list.append(log_date_str)
                    date_set.add(log_date_str)
                result_list.append('- ' + log_str)
            return '\n'.join(result_list)
        except Exception as e:
            print(e)
            return None

    @classmethod
    async def add_log(cls, log_str: str, name: str):
        try:
            requests.post(f'{BASE_URL_REQUESTS}/logs/new', json={
                'name': name,
                'log': log_str
            })
            return True
        except Exception as e:
            return None
