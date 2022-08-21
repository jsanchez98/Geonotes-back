def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, world!'

def test_csrf(client):
    response = client.get('/api/csrf')
    assert "CSRF token set" in str(response.data)

def test_no_csrf(client):
    response = client.post('/login', json={
        "username": "test",
        "password": "test"
    })
    status_code = response.status_code
    assert status_code > 399 and status_code < 410

def test_login(client):
    response = client.login("test", "test")
    assert response.status_code == 200

def test_logout(client):
    client.login("test", "test")
    response = client.get('logout')
    assert "success" in str(response.data)

def test_add_post(client):
    client.login("test", "test")
    response = client.post('/addpost', headers={
            "X-CSRFToken": client.csrf_token
        }, json={
        'text': "new note",
        'coordinates': '[0,0]'
    })
    print(response.data)
    assert 'test note' in str(response.data)

def test_get_posts(client):
    client.login("test", "test")
    response = client.get('/posts')
    print(str(response.data))
    assert True