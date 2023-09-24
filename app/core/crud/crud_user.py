from ..models.user import User, UserCreate
from sqlalchemy.future import select
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_users(session: AsyncSession):
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user_by_id(id: int, session: AsyncSession):
    result = await session.execute(select(User).where(User.id == id))
    return result.first()


async def create_user(payload: UserCreate, session: AsyncSession):
    user = User(
        name=payload.name,
        age=payload.age,
        email=payload.email,
        about_me=payload.about_me,
        password=payload.password,
    )
    user.hashed_password()
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user.id


async def update_user(user_id: int, payload: UserCreate,
                      session: AsyncSession):
    statement = select(User).where(User.id == user_id)
    results = await session.execute(statement)
    user = results.scalars().first()
    user.name = payload.name
    user.age = payload.age
    user.email = payload.email
    user.about_me = payload.about_me
    user.password = payload.password
    user.hashed_password()
    user.datetime_login = func.now()
    await session.commit()
    """ result = await session.execute(select(User).where(User.id == id))
    return result.first() """


async def login(user_id: int, session: AsyncSession):
    statement = select(User).where(User.id == user_id)
    results = await session.execute(statement)
    user = results.scalars().first()
    user.datetime_login = func.now()
    await session.commit()
