# Тестовое задание "Конвертер валют"

Была поставлена задача реализации простого api для конвертера валют RUB => USD.
Реализовать сервис нужно не прибегая к сторонним зависимостям. 

Данные о валюте брать из любого источника, но только это должны быть html документы, не апи.
В качестве источника был взят сайт цбр https://www.cbr.ru/currency_base/daily/. 
У него простой и структурированный html код. Также там всегда актуальные данные и этому источнику можно доверять.
Класс <code>ParserCBRCurrencies</code> из <code>data_loader.py</code> является классом парсера сайта ЦБ.
Парсер является универсальным, он поддерживает все валюты представленные на сайте ЦБ РФ на странице с актуальными курсами.

Так как мы хотим чтобы пользователь не ждал, пока мы сделаем http запрос к сайту ЦБ и распарсим html, 
мы запускаем парсер в отдельном потоке, и каждые n секунд он обновляет свои данные. А для пользователей считываем данные о курсе из памяти.

## Описание API
Для того, чтобы получить корректный ответ, нужно сделать запрос по адресу, где запущен сервер 
и добавить корректный GET параметр в адресной строке. 

Параметры: 

"currency_code" - код валюты в верхнем регистре. 

"amount" - количество, которое хотим конверировать. По умолчанию равно 1.


Примеры запроса:

Запрос: <code> http://127.0.0.1:8000/?currency_code=USD&amount=1500 </code>

Ответ: <code> {"currency": "USD", "requested_amount": 1500.0, "result_amount": 113743.05} </code>


## Запуск сервера

Команда запуска:

<code> python3 server.py [OPTION] </code>

-p, --port  - Порт. По умолчанию 8000.


-l, --listen - Адрес. По умолчанию 0.0.0.0


## Тестирование проекта

<code>python3 tests.py </code>

Файлы "cbr_pages.html", "currencies.json" - данные для тестирования.


## Docker

docker build: <code>docker build -t converter-http-server:1.0.0 .</code>

docker run: <code>docker run -e PORT=8000 -p 8000:8000 --rm --name converter-server-running converter-http-server:1.0.0</code>