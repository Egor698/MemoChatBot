import asyncio
from aiogram import Dispatcher, Bot

from src.bot.handlers import include_routers
from src.bot.middlewares import include_middlewares

from src.core.agent.phoenix_demo.tracing import tracing

from src.config import settings


async def main():
    bot = Bot(token=settings.BOT_TOKEN)

    dp = Dispatcher()

    include_routers(dp)
    include_middlewares(dp)
    dp.startup.register(startup)

    await dp.start_polling(bot)


async def startup():
    tracing()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass