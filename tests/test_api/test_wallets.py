from decimal import Decimal


def test_wallet_get_balance(client, test_wallet, auth_headers):
    response = client.get(
        "/api/v1/balance",
        params={"wallet_name": test_wallet.name},
        headers=auth_headers
    )

    assert response.status_code == 200

def test_wallet_get_balance_not_name(client, test_wallet, auth_headers):
    response = client.get(
        "/api/v1/balance",      
        headers=auth_headers
    )

    assert response.status_code == 200

def test_wallet_get_balance_not_auth(client, test_wallet, ):
    response = client.get(
        "/api/v1/balance",        
        headers={"Authorization": f"Bearer notexists"}
    )

    assert response.status_code == 401

def test_create_wallet(client, test_user, auth_headers):
    response = client.post(
        "/api/v1/wallets",
        json={
            "name": "card", 
            "initial_balance": 10
        },
        headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json()["wallet"] == "card"
    assert response.json()["message"] == "Wallet 'card' created"
    assert Decimal(str(response.json()["balance"]))  == Decimal(10)

def test_create_wallet_not_name(client, test_user, auth_headers):
    response = client.post(
        "/api/v1/wallets",
        json={
            "name": "   ", 
            "initial_balance": 10
        },
        headers=auth_headers
    )
    assert response.status_code == 422

def test_create_wallet_negative_init_balance(client, test_user, auth_headers):
    response = client.post(
        "/api/v1/wallets",
        json={
            "name": "card", 
            "initial_balance": -10
        },
        headers=auth_headers
    )
    assert response.status_code == 422
   
def test_create_wallet_duplicate_name(client, test_wallet, auth_headers):
    response = client.post(
        "/api/v1/wallets",
        json={
            "name": "card", 
            "initial_balance": 10
        },
        headers=auth_headers
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Wallet 'card' already exists"

def test_create_wallet_missing_name(client, test_user, auth_headers):
    """Тест: создание кошелька без указания имени"""
    response = client.post(
        "/api/v1/wallets",
        json={"initial_balance": 100},
        headers=auth_headers
    )
    
    assert response.status_code == 422
    
def test_create_wallet_name_too_long(client, test_user, auth_headers):
    """Тест: создание кошелька со слишком длинным именем"""
    long_name = "a" * 256  # Предположим, лимит 255 символов
    response = client.post(
        "/api/v1/wallets",
        json={"name": long_name, "initial_balance": 100},
        headers=auth_headers
    )
    
    assert response.status_code == 422