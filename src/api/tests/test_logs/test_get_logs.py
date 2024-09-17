async def test_get_contacts(client):
    name = 'Name'
    client.post("api/v1/contacts/new", json={'name': name})

    log_data_1 = {'name': name, 'log': 'log 1'}
    log_data_2 = {'name': name, 'log': 'log 2'}
    client.post("api/v1/logs/new/", json=log_data_1)
    client.post("api/v1/logs/new/", json=log_data_2)

    resp = client.get(f"api/v1/logs/{name}")
    assert resp.status_code == 200
    lst = resp.json()
    assert len(lst) == 2
    assert lst[0]['log'] == log_data_1['log']
    assert lst[1]['log'] == log_data_2['log']

