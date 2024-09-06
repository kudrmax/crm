from typing import List

import requests

contact_fields: List[str] = [
    'name',
    'telegram',
    'phone',
    'birthday',
]

BASE_URL = 'http://0.0.0.0:8000'


def print_contact_by_name(name: str):
    contact = requests.get(f'{BASE_URL}/contacts/name/{name}').json()
    return "\n".join([
        f"{field.capitalize()}: {value}" for field, value in contact.items() if value
    ])
