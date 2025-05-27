from models import User
from db import connection
from aiogram.types import User as AiogramUser
from sqlalchemy import select


@connection
async def save_user(session, user: AiogramUser) -> User:
    user_id = str(user.id)
    result = await session.execute(select(User).where(User.telegram_id == user_id))
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        new_user = User(
            telegram_id=user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
        )
        session.add(new_user)
        await session.commit()
        return new_user
