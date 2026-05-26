def test_create_user(client, db_session):
    #Act 
    response = client.post(
        "/api/v1/users",
        json={
            "login": "test"
        }
    )

    #Assert
    assert response.status_code == 200


def test_create__user_name(client, db_session):
    #Act 
    response = client.post(
        "/api/v1/users",
        json={
            "login": "    "
        }
    )

    #Assert
    assert response.status_code == 422

def test_create_duplicate_user(client, db_session, test_user):
    response = client.post(
        "/api/v1/users",
        json={
            "login": "test"
        }
    )

    #Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exist"

def test_get_user_unauthorized(client, test_user):
    response = client.get(
        "/api/v1/users/me",        
        headers={"Authorization": f"Bearer notexists"}
    )

    assert response.status_code == 401

def test_get_user_authorized(client, test_user, auth_headers):
    response = client.get(
        "/api/v1/users/me",        
        headers=auth_headers
    )

    assert response.status_code == 200

