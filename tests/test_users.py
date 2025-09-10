# tests/test_users.py
def test_create_user(client):
    response = client.post("/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_create_existing_user(client):
    response = client.post("/signup", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 409, response.text


def test_login_and_get_info(client):
    # Login first
    response = client.post("/login", data={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]

    # Use token to get user info
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/user/info", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


def test_login_with_wrong_creds(client):
    response = client.post("/login", data={
        "username": "testuser",
        "password": "pass123"
    })
    assert response.status_code == 401, response.text



