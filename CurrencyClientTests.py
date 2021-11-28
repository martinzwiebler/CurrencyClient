from unittest.mock import MagicMock, patch
from CurrencyClient import CurrencyClient
import time

test_cache_timer = 5  # Seconds. Very short times can lead to unexpected behaviour


def test1():
    fake_value = 1j

    # The first access should always be to the site.
    client = CurrencyClient(seconds=test_cache_timer)
    client.request_currency_from_site = MagicMock(return_value=fake_value)
    assert client.get_currency("EUR") == fake_value


def test2():
    fake_value = 1j

    # The first access should always be to the website.
    client = CurrencyClient(seconds=test_cache_timer)
    # Should be a floating point, should be positive
    value = client.get_currency("EUR")
    assert isinstance(value, type(0.1))
    assert value > 0
    # Second access should not be to the website and should be the same as previous value
    client.request_currency_from_site = MagicMock(return_value=fake_value)
    assert client.get_currency("EUR") == value


def test3():
    fake_value = 1j

    # The first access should always be to the website.
    client = CurrencyClient(seconds=test_cache_timer)
    client.get_currency("EUR")
    time.sleep(test_cache_timer - 1)

    # Access without website request shortly before the cache time is over

    client.request_currency_from_site = MagicMock(return_value=fake_value)
    value = client.get_currency("EUR")
    assert isinstance(value, type(0.1))
    assert value > 0
    time.sleep(2)
    # Access with website request shortly after the cache time is over
    assert client.get_currency("EUR") == fake_value


def test4():
    fake_value = 1j
    # The first access should always be to the website.
    client = CurrencyClient(seconds=test_cache_timer)
    client.get_currency("EUR")
    time.sleep(test_cache_timer + 1)
    client.get_currency("EUR")

    shorter_cache_timer = test_cache_timer - 3
    # Test of the functionality: Cache timer change
    client.set_interval(seconds=shorter_cache_timer)
    time.sleep(shorter_cache_timer - 1)

    # With new timer, first access should still see the cache
    client.request_currency_from_site = MagicMock(return_value=fake_value)
    value = client.get_currency("EUR")
    assert isinstance(value, type(0.1))
    assert value > 0
    time.sleep(2)
    # Second access shortly after the cache time is over, should request from site
    assert client.get_currency("EUR") == fake_value


if __name__ == "__main__":
    test1()
    test2()
    test3()
    test4()
    print("All tests complete")
