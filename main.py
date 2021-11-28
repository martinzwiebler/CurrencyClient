from CurrencyClient import CurrencyClient


if __name__ == "__main__":

    client = CurrencyClient(minutes=5)
    current_exchange_rate = client.get_currency("EUR")
    print("EUR/USD = %s" % current_exchange_rate)