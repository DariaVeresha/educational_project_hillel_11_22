import requests
from datetime import datetime, date
from urllib import parse


def get_currency_iso_code(currency: str) -> int:
    currency_dict = {
        'UAH': 980,
        'USD': 840,
        'EUR': 978,
        'GBP': 826,
        'AZN': 944,
        'CAD': 124,
        'PLN': 985,
    }
    try:
        return currency_dict[currency]
    except:
        raise KeyError('Currency not found! Update currencies information')


def get_currency_exchange_rate(currency_a: str,
                               currency_b: str) -> str:
    currency_code_a = get_currency_iso_code(currency_a)
    currency_code_b = get_currency_iso_code(currency_b)

    response = requests.get('https://api.monobank.ua/bank/currency')
    json = response.json()

    if response.status_code == 200:
        for i in range(len(json)):
            if json[i].get('currencyCodeA') == currency_code_a and json[i].get('currencyCodeB') == currency_code_b:
                date = datetime.fromtimestamp(
                    int(json[i].get('date'))
                ).strftime('%Y-%m-%d %H:%M:%S')
                rate_buy = json[i].get('rateBuy')
                rate_sell = json[i].get('rateSell')
                return f'exchange rate {currency_a} to {currency_b} for {date}: \n rate buy - {rate_buy} \n rate sell - {rate_sell}'
            return f'Not found: exchange rate {currency_a} to {currency_b}'

    else:
        return f"Api error {response.status_code}: {json.get('errorDescription')}"


def get_pb_exchange_rate(convert_currency: str,
                         bank: str,
                         rate_date: str) -> str:

    params = {

        'json': '',
        'date': rate_date   # TODO додати функцію валідації формату дати
    }
    query = parse.urlencode(params)
    api_url = 'https://api.privatbank.ua/p24api/exchange_rates?'
    response = requests.get(api_url+query)
    json = response.json()

    if response.status_code == 200:
        rates = json['exchangeRate']
        for rate in rates:
            if rate['currency'] == convert_currency:
                if bank == 'NBU' or bank == 'nbu':
                    try:
                        sale_rate = rate['saleRateNB']
                        purchase_rate = rate['purchaseRateNB']
                        return f'Exchange rate UAH to {convert_currency} for {rate_date} at {bank}: sale={sale_rate}, purchase={purchase_rate}'
                    except:
                        return f'There is no exchange rate NBU for {convert_currency}'
                elif bank == 'PB' or bank == 'pb' or bank == 'Privatbank' or bank == 'PrivatBank' and rate_date == '01-11-2022':
                    try:
                        sale_rate = rate['saleRate']
                        purchase_rate = rate['purchaseRate']
                        return f'Exchange rate UAH to {convert_currency} for {rate_date} at {bank}: sale={sale_rate}, purchase={purchase_rate}'
                    except:
                        return f'There is no exchange rate PB for {convert_currency}'
    else:
        return f'Error {response.status_code}'


result = get_pb_exchange_rate('USD', 'PB', '01.11.2022')
print(result)





