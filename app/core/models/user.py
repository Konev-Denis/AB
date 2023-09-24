from datetime import datetime
import typing as tp
from typing import Optional
from sqlmodel import Column, Field, SQLModel, TIMESTAMP, text

import hashlib
import bcrypt
import base64


class UserBase(SQLModel):
    name: str
    age: int
    email: str
    about_me: tp.Optional[str] = None


class UserCreate(UserBase):
    password: str

    def hashed_password(self):
        password = self.password.encode('utf-8')
        hashed = bcrypt.hashpw(
            base64.b64encode(hashlib.sha256(password).digest()),
            bcrypt.gensalt()
        )
        self.password = hashed.decode('utf-8')


class User(UserCreate, table=True):
    id: int = Field(primary_key=True)
    datetime_login: Optional[datetime] = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
