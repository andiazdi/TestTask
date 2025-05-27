from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from .utils import get_similar_questions
import uuid

router = Router()


@router.inline_query()
async def faq_handler(inline_query: InlineQuery):
    query_text = inline_query.query.strip().lower()
    questions = await get_similar_questions(query_text)

    articles = []
    for q in questions:
        articles.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=q.question,
                description=q.answer[:30] + "...",
                input_message_content=InputTextMessageContent(
                    message_text=f"❓ {q.question}\n\n💬 {q.answer}"
                ),
            )
        )

    await inline_query.answer(articles, cache_time=500)
