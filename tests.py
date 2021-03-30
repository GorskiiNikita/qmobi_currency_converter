import json
import threading
import time
import unittest
import urllib.request
from urllib.error import HTTPError

import utils

from data_loader import ParserCBRCurrencies
from server import currencies_parser, run


class TestParserCBR(unittest.TestCase):
    def setUp(self) -> None:
        with open('currencies.json', 'r') as fp:
            self.currencies = json.load(fp)

        with open('cbr_page.html', 'r') as fp:
            html = fp.read()

        self.parser = ParserCBRCurrencies()
        self.parser.load_currencies_data(html)

    def test_parse_html_code(self):
        self.assertEqual(self.currencies, self.parser.currencies)

    def test_convert_roubles(self):
        for code, price in self.currencies.items():
            self.assertEqual(price * 5, self.parser.convert_roubles(code, 5))
            self.assertEqual(price * 1005, self.parser.convert_roubles(code, 1005))
            self.assertEqual(price * 0.5, self.parser.convert_roubles(code, 0.5))


class TestUtilsFunctions(unittest.TestCase):
    def test_trim_tags(self):
        html = '<tr><td></td><td></td></tr>'
        html_trimmed = '<td></td><td></td>'
        self.assertEqual(html_trimmed, utils.trim_tags(html, '<tr>', '</tr>'))

    def test_isfloat(self):
        self.assertTrue(utils.isfloat('0'))
        self.assertTrue(utils.isfloat('1'))
        self.assertTrue(utils.isfloat('1.02'))
        self.assertTrue(utils.isfloat('100000'))
        self.assertTrue(utils.isfloat('-1'))
        self.assertFalse(utils.isfloat('lorem'))
        self.assertFalse(utils.isfloat('2t2'))


class TestRequests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with open('cbr_page.html', 'r') as fp:
            html = fp.read()

        currencies_parser.load_currencies_data(html)

        server_thread = threading.Thread(target=run)
        server_thread.setDaemon(True)
        server_thread.start()
        time.sleep(1)

    def test_correct_request(self):
        amount = 50
        currency_code = 'USD'
        request = urllib.request.urlopen(f'http://localhost:8000/?currency_code={currency_code}&amount={amount}')
        resp_data = json.loads(request.read().decode())

        self.assertEqual(200, request.code)
        self.assertEqual(currency_code, resp_data['currency_code'])
        self.assertEqual(amount, resp_data['requested_amount'])
        self.assertEqual(currencies_parser.convert_roubles('USD', amount), resp_data['result_amount'])

    def test_incorrect_request(self):
        amount = 'XII'
        currency_code = 'EUR'
        try:
            request = urllib.request.urlopen(f'http://localhost:8000')
            self.assertEqual(404, request.code)
        except HTTPError as e:
            self.assertEqual(404, e.code)

        try:
            request = urllib.request.urlopen(f'http://localhost:8000/?currency_code={currency_code}&amount={amount}')
            self.assertEqual(404, request.code)
        except HTTPError as e:
            self.assertEqual(404, e.code)


if __name__ == "__main__":
    unittest.main()
