from requests import get


OK = 200
CREATED = 201
URL = 'http://127.0.0.1:8001/main'
headers = {
    'Authorization': 'admin {a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3}'
}
data = {
    "title": "this is first title"
}


def test_requests():
    assert get(URL, headers=headers).status_code == OK


if __name__ == '__main__':
    # here you should use setup_env and setup_db if it was not used before
    test_requests()
