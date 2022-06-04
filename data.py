import requests
from bs4 import BeautifulSoup

import settings


class HolidayExtractor:
    USER_AGENT = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/605.1.15 (KHTML, like Gecko) '
        'Version/15.4 Safari/605.1.15'
    )

    def __init__(self, amount=2):
        self.amount = amount

    def get(self):
        html = self._get_holiday_html()
        yield from self._parse_holiday_html(html)

    def _get_holiday_html(self):
        response = requests.get(
            settings.HOLIDAYS_URL,
            headers={
                'User-Agent': self.USER_AGENT,
            }
        )
        response.raise_for_status()

        return response.text

    def _parse_holiday_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        holidays = soup.find_all('li')
        holidays = holidays[:self.amount]

        for holiday in holidays:
            yield holiday.text.strip().split('\t')[-1]


if __name__ == '__main__':
    extractor = HolidayExtractor()
    for holiday in extractor.get():
        print(holiday)
