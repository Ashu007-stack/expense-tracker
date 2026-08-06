from fastapi import APIRouter

from app.api.routes.user import router as user_router
from app.api.routes.expense import router as expense_router
from app.api.routes.dashboard import router as dashboard_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(expense_router)
api_router.include_router(dashboard_router)