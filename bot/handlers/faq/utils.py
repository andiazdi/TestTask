from db import connection
from sqlalchemy import select
from models import Question


@connection
async def get_similar_questions(session, question):
    query = select(Question).where(Question.question.ilike(f"%{question}%"))
    result = await session.execute(query)
    return result.scalars().all() if result else []
