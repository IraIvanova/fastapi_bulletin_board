import requests
import constants


class CurrencyConverter:
    def __init__(self):
        self.base_currency = 'UAH'  # Базовая валюта, в которой хранятся курсы
        self.exchange_rates = self.get_exchange_rates()

    def get_exchange_rates(self):
        # Замените URL на актуальный адрес API НБУ
        api_url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            rates = {currency['cc']: currency['rate'] for currency in data}
            rates[self.base_currency] = 1.0
            return rates
        else:
            raise Exception(f"Failed to fetch exchange rates. Status code: {response.status_code}")

    def convert(self, amount: float, from_currency: str, to_currency: str = constants.UAH):
        if from_currency not in self.exchange_rates or to_currency not in self.exchange_rates:
            raise ValueError("Invalid currency code")

        from_rate = self.exchange_rates[from_currency]
        to_rate = self.exchange_rates[to_currency]
        converted_amount = amount * from_rate if to_currency == constants.UAH else amount * (to_rate / from_rate)

        return converted_amount
