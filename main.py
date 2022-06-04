import asyncio

from tg_interface import TelegramInterface


if __name__ == '__main__':
    ti = TelegramInterface()
    asyncio.run(ti.run())
