import json
from typing import List, Dict, Any

import requests

from src.bot.common import BASE_URL


class ContactHelper:
    @classmethod
    async def add_new_contact(cls, name: str) -> bool | None:
        try:
            res = requests.post(BASE_URL + '/contacts', data=json.dumps({"name": name}))
            if res.status_code == 409:
                return None
            return True
        except Exception as e:
            return None

    @classmethod
    async def find_contact_by_name(cls, name: str) -> List[str] | None:
        try:
            contacts = (requests.get(f'{BASE_URL}/contacts/search/{name}')).json()
            contact_names = [contact['name'] for contact in contacts]
            return contact_names
        except Exception as e:
            return None

    @classmethod
    async def update_contact(cls, name: str, field_to_update: str, new_value: Any) -> Dict[str, str] | None:
        field_to_update = field_to_update.lower()
        try:
            print(name, field_to_update, new_value)
            contact = (requests.get(f'{BASE_URL}/contacts/name/{name}')).json()
            id = contact['id']
            requests.put(
                f'{BASE_URL}/contacts/{id}',
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
            contact = (requests.get(f'{BASE_URL}/contacts/name/{name}')).json()
            return contact
        except Exception as e:
            return None

    @classmethod
    async def print_contact_data(cls, contact: Dict[str, str]) -> str:
        answer = ""
        for key, value in contact.items():
            answer += f"{key}: {value}\n"
        return answer
