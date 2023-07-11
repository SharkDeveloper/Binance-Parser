import requests
import asyncio
from aiogram import Bot, types
import time

TOKEN = ''  # Тут вписываете API вашего бота
bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
charid = 123  # тут ваш чат айди


def parse_orders():  # Функция парсинга ордеров p2p
    headers = {
        'authority': 'p2p.binance.com',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9',
        'c2ctype': 'c2c_merchant',
        'clienttype': 'web',
        'content-type': 'application/json',
        'lang': 'ru',
        'origin': 'https://p2p.binance.com',
        'referer': 'https://p2p.binance.com/ru/trade/TinkoffNew/USDT?fiat=RUB', #тут тоже нужно изменить Тинькофф на нужный вам банк, ну или оставить
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    json_data = {
        'proMerchantAds': False,
        'page': 1,
        'rows': 10,
        'payTypes': [
            'TinkoffNew',
            # тут указываете название вашего банка. Узнать можно тут https://p2p.binance.com/ru/trade/all-payments/USDT, all-payments поменяется на ваш банк.
        ],
        'countries': [],
        'publisherType': None,
        'asset': 'USDT',
        'fiat': 'RUB',
        'tradeType': 'BUY',
    }

    response = requests.post(
        'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
        headers=headers,
        json=json_data,
    )

    data = response.json()
    return data


def parse_price_usd():  # Парсим курс с ЦБ РФ
    global price

    headers = {
        'authority': 'www.cbr.ru',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.cbr.ru/currency_base/daily/', headers=headers)
    data = response.text.split()
    for count, i in enumerate(data):
        try:
            if i == 'США</td>':
                price = data[count + 1].split('<td>')[1].split('</td>')[0].replace(',', '.')  # тут вытаскиваем курс USD
        except:
            print('Нет элемента для парсинга')

    return price


async def check_price():  # Функция сравнения и отстука в тг
    valid_usd = parse_price_usd()

    valid_usd = round(float(valid_usd) * (4 / 100) + float(valid_usd),
                      2)  # Тут прибавляем 4 процента, что почти равно p2p ордерам на бинансе
    min_procent = 50  # Минимальный процент от биржевой стоимости. Тут указано 50, т.е USD стоит 60 - 50% = 30 руб
    max_procent = 5  # Максимальный процент
    min_usd = valid_usd - (valid_usd * min_procent / 100)  # Высчитываем минимальную сумму
    max_usd = valid_usd - (valid_usd * max_procent / 100)  # Максимальная сумма
    print(valid_usd, ' цена в цб рф')
    print(min_usd, ' минимальная цена')
    print(max_usd, ' максимальная цена')
    data = parse_orders()
    print(float(data['data'][0]['adv']['price']), 'p2p цена')
    print('--------------------------------------')
    for i in range(0, 10):
        if min_usd < float(
                data['data'][i]['adv']['price']) < max_usd:  # тут мы сравниваем наши прайсы и если подходит стучим в тг
            print('подходит')
            await bot.send_message(charid, f'<b>Цена</b> -  {data["data"][i]["adv"]["price"]}\n'
                                           f'<b>Ник</b> -  {data["data"][i]["advertiser"]["nickName"]}\n'
                                           f'<b>Ссылка на профиль</b> - https://p2p.binance.com/ru/advertiserDetail?advertiserNo={data["data"][i]["advertiser"]["userNo"]}\n'
                                           f'<b>Доступно</b> - {data["data"][i]["adv"]["tradableQuantity"]}$\n'
                                           f'<b>Количество сделок</b> - {str(data["data"][i]["advertiser"]["monthOrderCount"])}\n'
                                           f'<b>Лимит</b> - {data["data"][i]["adv"]["minSingleTransAmount"]} - {data["data"][i]["adv"]["maxSingleTransAmount"]}\n',
                                   disable_web_page_preview=True)
    else:
        pass


if __name__ == '__main__':
    while True:
        try:
            asyncio.run(check_price())
            time.sleep(1.5)
        except:
            print('Слишком много запросов')
            time.sleep(300)