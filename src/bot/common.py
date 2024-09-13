import difflib
from typing import List

import requests

BASE_URL = 'http://0.0.0.0:8000/api/v1'


def print_contact_by_name(name: str):
    contact = requests.get(f'{BASE_URL}/contacts/{name}').json()
    if not contact:
        return f'Something went wrong ({name = })'
    return "\n".join([
        f"{field.capitalize()}: {value}" for field, value in contact.items() if value
    ])
