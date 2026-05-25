def test_register(client):

    response = client.post(
        "/auth/register",
        json={
            "email": "test@gmail.com",
            "password": "Password123!"
        }
    )
    
    print(response.status_code)
    print(response.get_json())

    assert response.status_code == 201

def test_login(client):

    # first register user
    client.post("/auth/register", json={
        "email": "test@gmail.com",
        "password": "123456"
    })

    # then login
    response = client.post("/auth/login", json={
        "email": "test@gmail.com",
        "password": "123456"
    })

    assert response.status_code == 200

    data = response.get_json()

    assert "access_token" in data