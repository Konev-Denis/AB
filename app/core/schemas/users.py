from pydantic import BaseModel
import hashlib
import bcrypt
import base64


class User(BaseModel):
    name: str
    age: int
    email: str
    about_me: str
    password: str

    def hashed_password(self):
        password = self.password.encode('utf-8')
        hashed = bcrypt.hashpw(
            base64.b64encode(hashlib.sha256(password).digest()),
            bcrypt.gensalt()
        )
        self.password = hashed.decode('utf-8')
