from aiogram import Dispatcher

from src.bot.middlewares.middleware import Middleware

def include_middlewares(dp: Dispatcher):
    dp.message.middleware(Middleware())