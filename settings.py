from pathlib import Path

HOLIDAYS_URL = 'https://sogodnisvyato.com.ua/'
TG_TOKEN = '***'  # set in local_settings
IDS_DB = Path('ids_db.txt')
TG_MESSAGE = 'Доброго ранку! Сьогодні ти можешь випити за такі свята:\n{holidays}'


try:
    from local_settings import *
except ImportError:
    pass
