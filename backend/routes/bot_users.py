from fastapi import APIRouter, Body, Depends
from starlette.status import HTTP_201_CREATED

from backend.models.bot_users import BotUsersCreate, BotUsersPublic
from backend.db.repositories.bot_users import BotUsersRepository
from backend.api.dependencies.database import get_repository

router = APIRouter(prefix="/bot_users")

@router.post("/register", response_model=BotUsersPublic, name="bot_users:register-bot_user", status_code=HTTP_201_CREATED)
async def create_new_bot_user(
    new_bot_user: BotUsersCreate = Body(..., embed=True),
    bot_users_repo: BotUsersRepository = Depends(get_repository(BotUsersRepository)),
) -> BotUsersPublic:
    created_bot_user = await bot_users_repo.create_bot_user(new_bot_user=new_bot_user)

    return created_bot_user

@router.get("/login")
async def login_bot_user():
    # sso authorization
    pass