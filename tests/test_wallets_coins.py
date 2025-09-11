def test_user(client) -> dict:
    """

    :param client: TestClient
    :return: Bearer token
    """
    client.post("/signup", json={
        "username": "walletuser",
        "email": "wallet@example.com",
        "password": "pass123"
    })
    login = client.post("/login", data={"username": "walletuser", "password": "pass123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return headers


def test_recharge_account(client):
    headers = test_user(client)
    response = client.post("/user/recharge", json={"amount": 1000}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 1000


def test_add_coin(client):
    headers = test_user(client)
    response = client.post("/coin/add", json={"symbol": "PI", "name" : "PI Coin"}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "PI"


def test_create_wallet(client):
    headers = test_user(client)
    response = client.post("/wallets/create", json={"coin_id": 1}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["coin_id"] == 1


def test_deposit_wallet(client):
    headers = test_user(client)
    response = client.post("/wallets/deposit", json={"wallet_id" : 1,"amount": 100}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 100


def test_withdraw_wallet(client):
    headers = test_user(client)
    response = client.post("/wallets/withdraw", json={"wallet_id" : 1,"amount": 50}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["balance"] == 50


def test_buy_coin(client):
    headers = test_user(client)
    response = client.post("/coin/buy", json={
  "coin_id": 1,
  "quantity": 2,
  "price": 3
}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Buy order submitted"


def test_sell_coin(client):
    headers = test_user(client)
    response = client.post("/coin/sell", json={
  "coin_id": 1,
  "quantity": 1,
  "price": 15
}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Sell order submitted"

