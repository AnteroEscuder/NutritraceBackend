def test_register_login_and_get_current_user(client):
    register_response = client.post(
        "/auth/register",
        json={"name": "Ana", "email": "ana@example.com", "password": "secret123"},
    )

    assert register_response.status_code == 201
    registered = register_response.json()
    assert registered["name"] == "Ana"
    assert registered["email"] == "ana@example.com"
    assert "password" not in registered
    assert "password_hash" not in registered

    login_response = client.post(
        "/auth/login",
        data={"username": "ana@example.com", "password": "secret123"},
    )

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    assert token

    me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

    assert me_response.status_code == 200
    assert me_response.json()["email"] == "ana@example.com"


def test_register_rejects_duplicate_email(client):
    payload = {"name": "Ana", "email": "ana@example.com", "password": "secret123"}

    assert client.post("/auth/register", json=payload).status_code == 201
    response = client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "El email ya está registrado"


def test_login_rejects_bad_credentials(client):
    client.post(
        "/auth/register",
        json={"name": "Ana", "email": "ana@example.com", "password": "secret123"},
    )

    response = client.post(
        "/auth/login",
        data={"username": "ana@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales incorrectas"
