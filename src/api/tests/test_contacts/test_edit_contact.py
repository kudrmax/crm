import pytest


async def test_edit_contact_good_data(client):
    user_data = {"name": "Max"}
    contact = client.post("api/v1/contacts/new", json=user_data)

    good_data = {
        'phone': '+79999999999',
        'telegram': '@telegram',
    }
    contact = client.put(f"api/v1/contacts/{user_data['name']}", json=good_data)
    assert contact.json()['name'] == user_data['name']
    assert contact.json()['phone'] == good_data['phone']
    assert contact.json()['telegram'] == good_data['telegram']
    assert contact.status_code == 200


@pytest.mark.parametrize('bad_data, status_code', [
    ({'ajshlkfdjhasdlkjfhsadl': '+79999999999'}, 200),
    ({}, 200),
])
async def test_edit_contact_bad_data(client, bad_data, status_code):
    user_data = {"name": "Max"}
    contact = client.post("api/v1/contacts/new", json=user_data)

    contact = client.put(f"api/v1/contacts/{user_data['name']}", json=bad_data)
    assert contact.status_code == status_code


async def test_edit_contact_name(client):
    user_data = {"name": "Maxim"}
    contact = client.post("api/v1/contacts/new", json=user_data)

    good_data = {'name': 'Max'}
    contact = client.put(f"api/v1/contacts/{user_data['name']}", json=good_data)
    assert contact.json()['name'] == good_data['name']
    assert contact.status_code == 200

    client.post("api/v1/contacts/new", json={'name': 'Nikita'})
    bad_data = {'name': 'Nikita'}
    contact = client.put(f"api/v1/contacts/{user_data['name']}", json=bad_data)
    assert contact.status_code == 409
