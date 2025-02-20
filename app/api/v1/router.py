from fastapi import APIRouter
from . import auth, admin, members

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
)

api_router.include_router(
    admin.router,
    tags=["admin"]
)

api_router.include_router(
    members.router,
    tags=["members"]
)

