import time

# The CurrencyClientCache should have the following properties:
#  It takes a time (float, seconds) as one argument
#  The property .exchange_rate takes the value from the site in store and
#  returns the cached value
#  If the cache is empty or outdated, .exchange_rate returns None
#  The method set_interval changes the time argument of an existing cache element


class CurrencyClientCache:
    def __init__(self, time_in_seconds):
        self.time_in_seconds = time_in_seconds
        self._exchange_rate = None
        self.storage_time = time.time()-self.time_in_seconds

    @property
    def exchange_rate(self):
        if self.storage_time + self.time_in_seconds > time.time():
            print("We take cached data")
            return self._exchange_rate

    @exchange_rate.setter
    def exchange_rate(self, rate):
        self._exchange_rate = rate
        self.storage_time = time.time()

    def set_interval(self, time_in_seconds):
        self.time_in_seconds = time_in_seconds
