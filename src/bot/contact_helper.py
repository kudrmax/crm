import json

import requests

from src.bot.common import BASE_URL


class ContactHelper:
    @classmethod
    async def add_new_contact(cls, name: str):
        try:
            requests.post(BASE_URL + '/contacts', data=json.dumps({"name": name}))
        except Exception as e:
            return False
        return True
