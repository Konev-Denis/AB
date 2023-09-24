from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi import Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
import jwt
import os

from ..config import SECRET_JWT
from .friendship import get_friends


router = APIRouter(prefix="/chat",
                   tags=["chat"],
                   responses={404: {"description": "Not found"}})

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    @staticmethod
    def _create_tuple(user_id: int, friend_id: int):
        if user_id < friend_id:
            return (user_id, friend_id)
        return (friend_id, user_id)

    async def connect(self, websocket: WebSocket, user_id: int, friend_id: int):
        await websocket.accept()
        chat = self._create_tuple(user_id, friend_id)
        if chat not in self.active_connections:
            self.active_connections[chat] = []
        self.active_connections[chat].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int, friend_id: int):
        chat = self._create_tuple(user_id, friend_id)
        self.active_connections[chat].remove(websocket)

    async def send_message(self, message: str, user_id: int, friend_id: int):
        chat = self._create_tuple(user_id, friend_id)
        for connection in self.active_connections[chat]:
            await connection.send_text(message)


# async def verify_token(authorization: str = Header("")):
async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        data = jwt.decode(token, SECRET_JWT, algorithms=["HS256"])
        data["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized user")
    return data


manager = ConnectionManager()
path_templates = os.path.abspath(os.path.join(__file__ , "../..", "templates"))
templates = Jinja2Templates(directory=path_templates)


@router.get("/{friend_id}")
async def get_chat(request: Request,
                   friend_id: int,
                   user_data: dict = Depends(verify_token)):
    if friend_id not in await get_friends(user_data["sub"]):
        raise HTTPException(status_code=403, detail="Friend not found")
    return templates.TemplateResponse("chat.html",
                                      {"request": request,
                                       "friend_id": friend_id,
                                       "user_id": user_data["sub"]})


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,
                             user_id: int,
                             friend_id: int):
    await manager.connect(websocket, user_id, friend_id)
    await manager.send_message(f"User #{user_id} join the chat",
                               user_id, friend_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"User #{user_id} says: {data}",
                                       user_id, friend_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"User #{user_id} left the chat",
                                user_id, friend_id)
