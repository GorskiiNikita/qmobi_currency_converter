import re
import time
import urllib.request
from urllib.error import URLError

from utils import trim_tags

CBR_CURRENCY_DAILY_PAGE_URL = 'https://www.cbr.ru/currency_base/daily/'
TD_TAG_START = '<td>'
TD_TAG_END = '</td>'


class ParserCBRCurrencies:
    def __init__(self, html=None):
        self.currencies = {}

    def load_currencies_data(self, html=None):
        if html is None:
            request = urllib.request.urlopen(CBR_CURRENCY_DAILY_PAGE_URL)
            html = request.read().decode()

        table = re.search(r'<table class="data">[\s\S]+</table>', html).group(0)
        raw_data = list(re.findall(r'<td>.+</td>', table))

        for i in range(0, len(raw_data), 5):
            currency_code = trim_tags(raw_data[i + 1], TD_TAG_START, TD_TAG_END)
            currency_value = float(
                trim_tags(raw_data[i + 4], TD_TAG_START, TD_TAG_END).replace(',', '.')
            )
            self.currencies[currency_code] = currency_value

    def convert_roubles(self, currency_code, amount):
        return amount * self.currencies[currency_code]

    def check_forever(self):
        while True:
            try:
                self.load_currencies_data()
            except URLError:
                pass
            time.sleep(30)
