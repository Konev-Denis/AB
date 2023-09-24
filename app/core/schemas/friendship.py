from pydantic import BaseModel
from typing import List


class Friendship(BaseModel):
    user_id: int
    friends_id: List[int] = []
