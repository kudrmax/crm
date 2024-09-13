import json

import pytest


async def test_delete_user_good_data(client):
    user_data = {"name": "Max"}
    contact = client.post("api/v1/contacts/new", json=user_data)

    response = client.delete(f"api/v1/contacts/{user_data['name']}")
    assert response.status_code == 200
    assert response.json()['name'] == user_data['name']

    response = client.delete(f"api/v1/contacts/{user_data['name']}")
    assert response.status_code == 200
    assert response.json() is None


# @pytest.mark.parametrize('bad_id, status_code', [
#     ('91f2818f-0cd2-4ed4-a674-3f82b55f7585', 200),
#     ('123', 422),
# ])
# async def test_delete_user_bad_data(client, bad_id, status_code):
#     response = client.delete(f"api/v1/contacts/{bad_id}")
#     assert response.status_code == status_code
