from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=127)
    amount: Decimal
    description: str | None = Field(None, max_length=255)

    @field_validator('amount')
    def amount_must_be_posititve(cls, v: Decimal) -> Decimal:
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
    initial_balance: Decimal = 0

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Wallet name cannot be empty")
        return v
    
    @field_validator('initial_balance')
    def balance_not_negative(cls, v: Decimal) -> Decimal:
        #Check initial_balace is positive
        if v < 0:
            raise ValueError("Initial balace cannot be negative")
        return v