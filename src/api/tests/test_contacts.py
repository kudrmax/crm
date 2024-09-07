async def test_test():
    assert True == True


async def test_create_contact(client):
    user_data = {
        "name": "New name"
    }

    response = client.post("/contacts/", json=user_data)
    response_data = response.json()

    assert response.status_code == 200, response.text
    assert user_data['name'] == response_data['name']
    assert response_data['phone'] is None

    id = response_data['id']
    response = client.get(f"/contacts/{id}")
    response_data = response.json()
    assert response.status_code == 200, response.text
    assert user_data['name'] == response_data['name']
    assert response_data['phone'] is None

    response = client.get(f"/contacts/")
    response_data = response.json()
    assert response.status_code == 200, response.text
    assert len(response_data) == 1


async def test_edit_contact(client, create_contact_in_database):
    # response = client.post(f"/contacts/")
    # response_data = response.json()
    res = await create_contact_in_database('Max')
    print(res)
    response = client.get(f"/contacts/")
    response_data = response.json()
    assert response.status_code == 200, response.text
    assert len(response_data) == 1
