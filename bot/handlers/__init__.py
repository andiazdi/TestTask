from aiogram import Dispatcher

from .basket import router as basket_router
from .catalog import router as catalog_router
from .faq import router as faq_router
from .commands import router as commands_router

dp = Dispatcher()
routers = (basket_router, catalog_router, faq_router, commands_router)

for router in routers:
    dp.include_router(router)
