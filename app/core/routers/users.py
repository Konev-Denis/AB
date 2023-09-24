from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import hashlib
import bcrypt
import base64
import jwt

from ..models.database import get_session
from ..config import SECRET_JWT
from ..models.user import User, UserCreate
from ..crud.crud_user import get_all_users, get_user_by_id
from ..crud.crud_user import create_user, update_user, login


router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={404: {"description": "Not found"}})


@router.get("/")
async def get_list_users(session: AsyncSession = Depends(get_session)):
    return await get_all_users(session)


@router.get("/{user_id}")
async def get_user(user_id: int,
                   session: AsyncSession = Depends(get_session)):
    user = await get_user_by_id(user_id, session)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/create")
async def create(user: UserCreate,
                 session: AsyncSession = Depends(get_session)):
    print("await create_user")
    last_record_id = await create_user(user, session)
    print("return create_user")
    return {"id": last_record_id, **user.dict()}


@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(),
                     session: AsyncSession = Depends(get_session)):
    # в текущей задаче form_data.username это user_id
    user_id = int(form_data.username)
    user = await get_user(user_id, session)
    user = user[User]
    password_base64 = base64.b64encode(
        hashlib.sha256(form_data.password.encode('utf-8')).digest())
    if bcrypt.checkpw(password_base64, user.password.encode('utf-8')):
        jwt_token = jwt.encode(
            {"sub": user.id, "name": user.name},
            SECRET_JWT,
            algorithm="HS256",
            headers={"alg": "HS256", "typ": "JWT"},)
        await login(user_id, session)
        return {"access_token": jwt_token, "token_type": "bearer"}
    raise HTTPException(status_code=403, detail="Incorrect password")


@router.put("/edit")
async def edit_user(user: UserCreate, user_id: int,
                    session: AsyncSession = Depends(get_session)):
    user.hashed_password()
    await update_user(user_id, user, session)
    return {"status": "successfully"}
