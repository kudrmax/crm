async def test_get_one_contact(client):
    user_data = {"name": "Max"}
    contact = client.post("api/v1/contacts/new", json=user_data)
    name = contact.json()["name"]

    contacts = client.get(f"api/v1/contacts/")
    assert contacts.status_code == 200
    assert len(contacts.json()) == 1

    contact = client.get(f"api/v1/contacts/{name}")
    assert contact.status_code == 200
    assert contact.json()['name'] == user_data['name']

    not_in_db_name = '123456789'
    contact = client.get(f"api/v1/contacts/{not_in_db_name}")
    assert contact.status_code == 404


async def test_get_contacts(client):
    client.post("api/v1/contacts/new", json={'name': '1'})
    client.post("api/v1/contacts/new", json={'name': '2'})
    client.post("api/v1/contacts/new", json={'name': '3'})
    contacts = client.get(f"api/v1/contacts/")
    assert contacts.status_code == 200
    assert len(contacts.json()) == 3
