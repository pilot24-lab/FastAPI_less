from fastapi import APIRouter, HTTPException
from app.services import wallets as wallets_service
from app.schemas import CrateWalletRequest


router = APIRouter()

@router.get("/balance")
def get_balance(wallet_name: str | None = None):
    return wallets_service.get_balance(wallet_name)
    

@router.post("/wallets")
def create_wallet(wallet: CrateWalletRequest):
    return wallets_service.create_wallet(wallet)
    