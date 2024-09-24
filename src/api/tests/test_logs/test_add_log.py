async def test_add_log(client):
    user_data = {"name": "Name"}
    client.post("api/v1/contacts/new/", json=user_data)

    log_data = {
        "name": user_data['name'],
        "log": "Log str"
    }
    log = client.post("api/v1/logs/new/", json=log_data)
    assert log.json()['log'] == log_data['log']
    assert log.status_code == 200
    assert 'datetime' in log.json()
    assert 'contact_id' in log.json()


async def test_add_log_bad_data(client):
    user_data = {"name": "Name"}
    client.post("api/v1/contacts/new/", json=user_data)

    log_data = {
        "log": "Log str"
    }
    log = client.post("api/v1/logs/new/", json=log_data)
    assert log.status_code == 422

    log_data = {
        "name": user_data['name'],
        "log": "Log str",
        "some_field": "some_field"
    }
    log = client.post("api/v1/logs/new/", json=log_data)
    assert log.status_code == 200

async def test_add_empty_log(client):
    user_data = {"name": "Name"}
    client.post("api/v1/contacts/new/", json=user_data)

    log_data = {
        "name": user_data['name'],
    }
    log = client.post("api/v1/logs/new/empty/", json=log_data)
    assert log.json()['log'] == ""
    assert log.status_code == 200
    assert 'datetime' in log.json()
    assert 'contact_id' in log.json()