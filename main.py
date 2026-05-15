from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: float
    description: str | None = Field(None, max_length=255)

    @field_validator('amount')
    def amount_must_be_posititve(cls, v: float) -> float:
        #Check amount is positive
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v
    
    @field_validator("wallet_name")
    def wallet_name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v

class CrateWalletRequest(BaseModel):
    name: str = Field(..., max_length=127)
    initial_balance: float = 0

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v
    
    @field_validator('initial_balance')
    def balance_not_negative(cls, v: float) -> float:
        #Check initial_balace is positive
        if v < 0:
            raise ValueError("Initial balace cannot be negative")
        return v

BALANCE = {}

@app.get("/balance")
def get_balance(wallet_name: str | None = None):
    #Если имя кошелька не указано, возвращаем сумму балансов всех кошельков
    if wallet_name is None:
        return {"total_balance": sum(BALANCE.values())}
    #Если кошелька нет в списке
    if wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{wallet_name}' not found"
        )
    #Возвращаем баланс конкретного кошелька 
    return {"wallet": wallet_name, "balance": BALANCE[wallet_name]}

@app.post("/wallets")
def create_wallet(wallet: CrateWalletRequest):
    if wallet.name in BALANCE:
        raise HTTPException(
            status_code=400,
            detail=f"Wallet '{wallet.name}' already exists"
        )
    BALANCE[wallet.name] = wallet.initial_balance
    return {
        "message": f"Wallet '{wallet.name}' created",
        "wallet": wallet.name,
        "balance": BALANCE[wallet.name]
    }


@app.post("/operations/income")
def add_income(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
 
    
    BALANCE[operation.wallet_name] += operation.amount
    return {
        "message": "Income added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }  
    

@app.post("/operations/expense")
def  add_expense(operation: OperationRequest):
    if operation.wallet_name not in BALANCE:
        raise HTTPException(
            status_code=404,
            detail=f"Wallet '{operation.wallet_name}' not found"
        )
    
    if BALANCE[operation.wallet_name] < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient funds. Available: {BALANCE[operation.wallet_name]}"
        )
    BALANCE[operation.wallet_name] -= operation.amount
    return {
         "message": "Expense added",
        "wallet": operation.wallet_name,
        "amount": operation.amount,
        "description": operation.description,
        "new_balance": BALANCE[operation.wallet_name]
    }