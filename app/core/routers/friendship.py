from fastapi import Depends, APIRouter, HTTPException
import jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.database import get_session
from ..models.friendship import FriendshipsCreate
from ..crud.crud_friendship import get_friends_by_id, create_friendship
from ..config import SECRET_JWT


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        data = jwt.decode(token, SECRET_JWT, algorithms=["HS256"])
        data["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return data


router = APIRouter(prefix="/friendship",
                   tags=["friendship"],
                   responses={404: {"description": "Not found"}})


@router.post("/create")
async def create(friend_id: int,
                 user_data: dict = Depends(verify_token),
                 session: AsyncSession = Depends(get_session)):
    if user_data["sub"] == friend_id:
        return {"status": "unsuccessfully",
                "message": "unsuccessfully friend id"}
    try:
        friendship = FriendshipsCreate(user_id_one=user_data["sub"],
                                       user_id_two=friend_id)
        await create_friendship(friendship, session)
    except Exception:
        return {"status": "unsuccessfully",
                "message": "friendship already exists"}
    return {"status": "successfully"}


@router.get("/{user_id}")
async def get_friends(user_id: int,
                      session: AsyncSession = Depends(get_session)):
    return await get_friends_by_id(user_id, session)
