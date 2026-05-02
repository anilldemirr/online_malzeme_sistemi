from fastapi import APIRouter

from src.api.v1.endpoints import auth, equipment, inventory, transactions, users


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["equipment"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
