import requests
from CurrencyClientCache import CurrencyClientCache
import time
import datetime


class CurrencyClient:

    def __init__(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        # The CurrencyClient constructor has the same parameters as timedelta constructor
        self.url = 'https://v6.exchangerate-api.com/v6/b413d708c11abb88688ef53c/latest/USD'
        self.params = {'access_key': 'b413d708c11abb88688ef53c'}
        self.time_in_seconds = datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours,
                                                  weeks).total_seconds()
        self.cache = {}

    def request_currency_from_site(self, currency):
        # Takes a currency abbreviation for example "EUR", "GBP", "USD"...
        # Returns the conversion rate to USD as a float.
        # For example with EUR that would be the value EUR/USD
        response = requests.get(url=self.url, params=self.params)
        print("A request is executed")
        data = response.json()
        conversion_rates = data['conversion_rates']
        return conversion_rates[currency]

    def get_currency(self, currency):
        if currency not in self.cache:
            self.cache[currency] = CurrencyClientCache(self.time_in_seconds)

        # get cached exchange rate from the cache
        exchange_rate = self.cache[currency].exchange_rate
        # If nothing is cached
        # get exchange rate from site and store it in cache
        if exchange_rate is None:
            exchange_rate = self.request_currency_from_site(currency)
            self.cache[currency].exchange_rate = exchange_rate

        return exchange_rate

    def set_interval(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
        # Change the interval time for the cache.
        # All cache items learn the new interval.
        self.time_in_seconds = datetime.timedelta(days, seconds, microseconds, milliseconds, minutes, hours,
                                                  weeks).total_seconds()
        new_cache = {}
        for currency in self.cache:
            self.cache[currency].set_interval(self.time_in_seconds)
