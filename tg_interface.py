import asyncio

import telegram

import settings
from data import HolidayExtractor


class TelegramInterface:
    def __init__(self):
        self.bot = telegram.Bot(settings.TG_TOKEN)

    async def run(self):
        started_ids = await self._get_starts()
        self._save_ids(started_ids)

        await self._send_holidays()

    async def _get_starts(self):
        async with self.bot:
            updates = await self.bot.get_updates()

        ids = set()
        for update in updates:
            if update['message']['text'] == '/start':
                ids.add(update['message']['chat']['id'])

        return ids

    def _read_ids(self):
        if settings.IDS_DB.exists():
            with open(settings.IDS_DB, 'r') as ids_db:
                for line in ids_db.readlines():
                    if line.strip():
                        yield int(line.strip())

    def _save_ids(self, ids):
        existing_ids = set(self._read_ids())

        new_ids = set(existing_ids)
        new_ids.update(ids)

        with open(settings.IDS_DB, 'w') as ids_db:
            for id in new_ids:
                ids_db.write(f'{id}\n')

    def _get_message(self):
        holidays = HolidayExtractor()
        holidays_msg = '\n'.join(f'- {holiday}' for holiday in holidays.get())
        return settings.TG_MESSAGE.format(holidays=holidays_msg)

    async def _send_holidays(self):
        for user_id in self._read_ids():
            async with self.bot:
                await self.bot.send_message(
                    text=self._get_message(),
                    chat_id=user_id,
                )
