from aiogram import Dispatcher
from src.bot.handlers.message import router

def include_routers(dp: Dispatcher):
    dp.include_routers(router)