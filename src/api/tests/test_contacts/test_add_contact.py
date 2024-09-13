async def test_create_contact(client):
    user_data = {"name": "Name"}
    contact = client.post("api/v1/contacts/new/", json=user_data)
    assert contact.json()['name'] == user_data['name']
    contacts = client.get(f"api/v1/contacts/")
    assert contacts.status_code == 200
    assert len(contacts.json()) == 1


async def test_create_existing_contact(client):
    user_data_1 = {"name": "Max"}
    user_data_2 = {"name": "Nikita"}
    user_data_3 = {"name": "Nikita"}
    contact_1 = client.post("api/v1/contacts/new/", json=user_data_1)
    assert contact_1.status_code == 200
    contact_2 = client.post("api/v1/contacts/new/", json=user_data_2)
    assert contact_2.status_code == 200
    contact_3 = client.post("api/v1/contacts/new", json=user_data_3)
    assert contact_3.status_code == 409
    contacts = client.get(f"api/v1/contacts/")
    assert len(contacts.json()) == 2


async def test_create_contact_bad_data(client):
    user_data = {"not_name": "Max"}
    contact = client.post("api/v1/contacts/new", json=user_data)
    assert contact.status_code == 422

    user_data = {"name": "Rishat", 'not_name': 'Not Rishat'}
    contact = client.post("api/v1/contacts/new", json=user_data)
    assert contact.status_code == 200
