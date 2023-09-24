from ..models.user import User
from ..models.friendship import Friendships, FriendshipsCreate
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_friends_by_id(id: int, session: AsyncSession):
    query1 = select(Friendships.user_id_two.label('id')).\
        where(Friendships.user_id_one == id)
    query2 = select(Friendships.user_id_one.label('id')).\
        where(Friendships.user_id_two == id)
    union = query1.union(query2).subquery()
    stmt = select(User).select_from(union).\
        join(User, union.c.id == User.id).\
        order_by(User.datetime_login.desc(), User.id)
    results = await session.execute(stmt)
    return results.scalars().all()


async def create_friendship(payload: FriendshipsCreate,
                            session: AsyncSession):
    friendships = Friendships(
        user_id_one=payload.user_id_one,
        user_id_two=payload.user_id_two,
    )
    session.add(friendships)
    await session.commit()
    await session.refresh(friendships)
    return friendships
