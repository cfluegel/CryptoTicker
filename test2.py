from lib.coinmarketcap import Coinmarketcap

import time, sys

Ticker = Coinmarketcap()

ETHOLD=0.0
BTCOLD=0.0
XMROLD=0.0
BCNOLD=0
XRPOLD=0


while True:

    ETH=Ticker.getCrypto('ETH').getPrice()
    if ETHOLD == 0:
        ETHOLD=ETH
    print("ETH Price:\t{:13.7f} € ({:13.7f}) ({}s) ".format(ETH, ETHOLD-ETH, Ticker.getCrypto('ETH').getLastUpdated()))

    BTC=Ticker.getCrypto('BTC').getPrice()
    if BTCOLD == 0:
        BTCOLD=BTC
    print("BTC Price:\t{:13.7f} € ({:13.7f}) ({}s)".format(BTC, BTCOLD-BTC, Ticker.getCrypto('BTC').getLastUpdated()))

    XMR=Ticker.getCrypto('XMR').getPrice()
    if XMROLD == 0:
        XMROLD=XMR
    print("XMR Price:\t{:13.7f} € ({:13.7f}) ({}s)".format(XMR, XMROLD-XMR, Ticker.getCrypto('XMR').getLastUpdated()))

    BCN=Ticker.getCrypto('BCN').getPrice()
    if BCNOLD == 0:
        BCNOLD=BCN
    print("BCN Price:\t{:13.7f} € ({:13.7f}) ({}s)".format(BCN, BCNOLD-BCN, Ticker.getCrypto('BCN').getLastUpdated()))

    XRP=Ticker.getCrypto('XRP').getPrice()
    if XRPOLD == 0:
        XRPOLD=XRP
    print("XRP Price:\t{:13.7f} € ({:13.7f}) ({}s)".format(XRP, XRPOLD-XRP, Ticker.getCrypto('XRP').getLastUpdated()))
    print('='*40)

    ETHOLD=ETH
    BTCOLD=BTC
    XMROLD=XMR
    BCNOLD=BCN
    XRPOLD=XRP

    time.sleep(10)
