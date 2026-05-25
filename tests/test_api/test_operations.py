from decimal import Decimal


def test_add_expense_succes(client, test_wallet, auth_headers):
    #Arrange  

    #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": test_wallet.name,
            "amount": 50.0,
            "description": "Food"
        },
        headers=auth_headers
    )

    #Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Expense added"
    assert response.json()["wallet"] == test_wallet.name
    assert Decimal(str(response.json()["amount"]))  == Decimal(50)
    assert Decimal(str(response.json()["new_balance"]))  == Decimal(150)
    assert response.json()["description"] == "Food"

def test_add_expense_negative_amount(client, auth_headers):
    #Arrange
    
    #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": -50.0,
            "description": "Food"
        },
        headers=auth_headers
    )
    #Assert
    assert response.status_code == 422

def test_name_not_empty(client, auth_headers):
    #Arrange
   
    #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "   ",
            "amount": 50.0,
            "description": "Food"
        },
        headers=auth_headers
    )
    #Assert
    assert response.status_code == 422

def test_add_expense_wallet_not_exists(client, test_user):
    #Arrange 
    
    #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer {test_user.login}"}
    )
    #Assert
    assert response.status_code == 404

def test_add_expense_unauthorized(client):
    #Arrange
    
        #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 50.0,
            "description": "Food"
        },
        headers={"Authorization": f"Bearer notexists"}
    )
    #Assert
    assert response.status_code == 401

def test_add_expense_not_enought_money(client, test_wallet, auth_headers):
    #Arrange
    
    #Act
    response = client.post(
        "/api/v1/operations/expense",
        json={
            "wallet_name": "card",
            "amount": 201.0,
            "description": "Food"
        },
        headers=auth_headers
    )

    #Assert
    assert response.status_code == 400