# -*- coding: utf-8 -*-
#

# Requests fuer die Abfrage
import requests
import json
import time

class CryptoCurrency:
    def __init__(self, data):
        if type(data) != type(dict()):
            raise Exception()
        self.__raw_data = data

        # Extract or extrapolate the useful data from the raw data
        self.symbol = self.__raw_data['symbol']
        self.last_updated = float(self.__raw_data['last_updated'])

        self.price = dict()
        self.price['eur'] = self.__raw_data['price_eur']
        self.price['usd'] = self.__raw_data['price_usd']

        self.percent = dict()
        self.percent['1h'] = self.__raw_data['percent_change_1h']
        self.percent['1d'] = self.__raw_data['percent_change_24h']
        self.percent['7d'] = self.__raw_data['percent_change_7d']

    def getChangesInPercent(self):
        return (float(self.percent['1h']),
                float(self.percent['1d']),
                float(self.percent['7d']) )

    def getPrice(self, fiat='eur'):
        if fiat is 'eur':
            return float(self.price['eur'])
        else:
            return float(self.price['usd'])
    def getLastUpdated(self):
        # return float(time.time()-self.last_updated)
        return int(self.last_updated)

#------------------------------------------------------------------------------
class Coinmarketcap:
    def __init__(self):
        self.api_url = "https://api.coinmarketcap.com/v1/ticker/"
        self.api_parameter = {
            "convert": "EUR",
            "limit": 150,
        }
        self.api_method = "GET"
        # Dict for all CryptoCurrencies from the market 
        self.__cryptos = {}

        # Hold the time the data was updated
        self.__lastupdated = 0

        # Retrieve the data from the API
        self.update()

    def update(self):
        r = requests.get(self.api_url, params=self.api_parameter)
        if r.status_code != 200:
            return False
        self.__raw_data = json.loads(r.text)

        self.__lastupdated = time.time()
        self.__update_cryptos()

    def __update_cryptos(self):
        for crypto in self.__raw_data:
            self.__cryptos[crypto['symbol']] = CryptoCurrency(crypto)

    def getCrypto(self, symbol):
        # TODO: Find a better solution for autoupdating the currencies 
        if time.time()-self.__lastupdated >= 5:
            self.update()

        if symbol.upper() in self.__cryptos:
            return self.__cryptos[symbol.upper()]

        # TODO: Create a Custom Exception for this use-case
        raise Exception("Currency not found")

if __name__ == '__main__':

    test1 = Coinmarketcap()
    test1.update()
    print(test1.getCrypto('BCN').getChangesInPercent())
    print(test1.getCrypto('BCN').getPrice())

