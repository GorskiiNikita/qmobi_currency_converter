import argparse
import json
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
from urllib.parse import parse_qs

from data_loader import ParserCBRCurrencies
from utils import isfloat


USD_CODE = 'USD'
CURRENCY_CODE_PARAMETER = 'currency_code'
REQUESTED_AMOUNT_PARAMETER = 'amount'
currencies_parser = ParserCBRCurrencies()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def _json_response(self, data):
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_GET(self):
        GET_parameters = parse_qs(urlparse.urlparse(self.path).query)

        currency_code = GET_parameters.get(CURRENCY_CODE_PARAMETER)
        currency_code = currency_code[0] if currency_code else None

        amount = GET_parameters.get(REQUESTED_AMOUNT_PARAMETER)
        amount = amount[0] if amount else 1

        if currency_code == USD_CODE and isfloat(amount):
            converted_value = currencies_parser.convert_roubles(
                currency_code,
                float(amount)
            )

            self.send_response(200)
            self._set_headers()
            self._json_response({
                'currency_code': USD_CODE,
                'requested_amount': float(amount),
                'result_amount': converted_value
            })
        else:
            msg = ''
            if currency_code is None:
                msg = 'Not found "currency_code" parameter'
            elif currency_code and currency_code != USD_CODE:
                msg = 'ValueError in "currency_code" parameter.'
            elif not isfloat(amount):
                msg = 'ValueError: "amount" parameter must be a number'

            self.send_response(404)
            self._set_headers()
            self._json_response({
                'error': msg
            })


def run(server_class=ThreadingHTTPServer, handler_class=HTTPRequestHandler,
        addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    currencies_parser.load_currencies_data()
    thread_currencies_parser = threading.Thread(target=currencies_parser.check_forever)
    thread_currencies_parser.daemon = True
    thread_currencies_parser.start()

    arg_parser = argparse.ArgumentParser(description="Run a HTTP server")
    arg_parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    arg_parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )
    args = arg_parser.parse_args()
    run(addr=args.listen, port=args.port)
