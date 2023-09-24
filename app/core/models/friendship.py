from sqlmodel import SQLModel, Field, UniqueConstraint


class FriendshipsBase(SQLModel):
    __table_args__ = (
        UniqueConstraint('user_id_one',
                         'user_id_two',
                         name='unique_1_2'),
    )
    user_id_one: int = Field(index=True, foreign_key="user.id")
    user_id_two: int = Field(index=True, foreign_key="user.id")


class FriendshipsCreate(FriendshipsBase):
    pass


class Friendships(FriendshipsBase, table=True):
    id_friendships: int = Field(primary_key=True)
