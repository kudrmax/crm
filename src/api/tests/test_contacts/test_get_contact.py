async def test_get_one_contact(client):
    user_data = {"name": "Max"}
    contact = client.post("/contacts/", json=user_data)
    id = contact.json()["id"]
    name = contact.json()["name"]

    contacts = client.get(f"/contacts/")
    assert contacts.status_code == 200
    assert len(contacts.json()) == 1

    contact = client.get(f"/contacts/{id}")
    assert contact.status_code == 200
    assert contact.json()['name'] == user_data['name']

    contact = client.get(f"/contacts/name/{name}")
    assert contact.status_code == 200
    assert contact.json()['name'] == user_data['name']

    not_uuid = '123'
    contact = client.get(f"/contacts/{not_uuid}")
    assert contact.status_code == 422

    not_in_db_uuid = '91f2818f-0cd2-4ed4-a674-3f82b55f7585'
    contact = client.get(f"/contacts/{not_in_db_uuid}")
    assert contact.status_code == 200
    assert contact.json() is None


async def test_get_contacts(client):
    client.post("/contacts/", json={'name': '1'})
    client.post("/contacts/", json={'name': '2'})
    client.post("/contacts/", json={'name': '3'})
    contacts = client.get(f"/contacts/")
    assert contacts.status_code == 200
    assert len(contacts.json()) == 3