from ..models.database import database, chats, party, messages


""" chats = Table(
    "chats",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)

party = Table(
    "party",
    metadata,
    Column("chat_id", Integer, ForeignKey(chats.c.id)),
    Column("user_id", Integer, ForeignKey(users.c.id)),
    UniqueConstraint("user_id_one", "user_id_two", name="uniq_1"),
)

messages = Table(
    "messages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("chat_id", Integer, ForeignKey(chats.c.id)),
    Column("user_id", Integer, ForeignKey(users.c.id)),
    Column("content", String),
    Column("date", DateTime(timezone=True), server_default=func.now()),
) """


class Chat:
    @classmethod
    async def get_chat_by_id(cls, id):
        query = party.select(party.c.chat_id).where(party.c.user_id == id)
        return await database.fetch_one(query)

    @classmethod
    async def create_chat(cls, name=None, **users_id):
        query = chats.insert().values(name)
        chat_id = await database.execute(query)
        values = [{"chat_id": chat_id, "user_id": id} for id in users_id]
        print(values)
        query = party.insert()
        await database.execute(query, values)
        return chat_id

    @classmethod
    async def send_message(cls, chat_id, user_id, content):
        query = messages.insert().values(chat_id, user_id, content)
        return await database.execute(query)

    @classmethod
    async def get_message(cls, chat_id, user_id, content):
        query = messages.select(messages.c.user_id,
                                messages.c.content,
                                messages.c.date) \
                        .where(messages.c.chat_id == chat_id)
        return await database.execute(query)
