# Standard Libraries
import time
import sys
from os.path import join

# Exchanges / Data Sources
from lib.coinmarketcap import Coinmarketcap

# GTK related imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject

class Application():
    def __init__(self):
        # TODO: Make the options available through cmd line param.
        self.__viewmode = 1
        self.__timemode = 1
        self.__ticker = Coinmarketcap()


        # Get the GTK Builder Object for Glade Files
        self.builder = Gtk.Builder()

        # Select the right GUI
        # TODO: There is probably a better way of doing this with just one glade file
        if self.__viewmode == 0:
            self.builder.add_from_file( join("res","CryptoTicker-horizontal.glade") )
        else:
            self.builder.add_from_file( join("res","CryptoTicker-vertical.glade") )

        # Load Main window
        self.window = self.builder.get_object("CryptoTicker")
        self.window.show_all()

        # all_objects = self.builder.get_objects()

        self.label = {}
        self.label['ETH'] = self.builder.get_object("lbETH")
        self.label['LTC'] = self.builder.get_object("lbLTC")
        self.label['BTC'] = self.builder.get_object("lbBTC")
        self.label['BCN'] = self.builder.get_object("lbBCN")
        self.label['XMR'] = self.builder.get_object("lbXMR")

        self.lastupdate_label = {}
        self.lastupdate_label['ETH'] = self.builder.get_object("lastUpdateETH")
        self.lastupdate_label['LTC'] = self.builder.get_object("lastUpdateLTC")
        self.lastupdate_label['BTC'] = self.builder.get_object("lastUpdateBTC")
        self.lastupdate_label['BCN'] = self.builder.get_object("lastUpdateBCN")
        self.lastupdate_label['XMR'] = self.builder.get_object("lastUpdateXMR")

        # map functions to handlers that are defined in the glade file
        handlers = {
                "onDeleteWindow": Gtk.main_quit,
        }
        self.builder.connect_signals(handlers)


        self.__timeout_id = GObject.timeout_add(30*1000,
                                                self.__refreshTicker)

        # First refresh of all label fields
        self.__refreshTicker()

    def __refreshTicker(self):
        for (currency, lblObj) in self.label.items():
            try:
                old_price = float(self.label[currency].get_text())
            except(ValueError):
                old_price = float(self.__ticker.getCrypto(currency).getPrice())
            ticker_price = float(self.__ticker.getCrypto(currency).getPrice())

            if ticker_price > old_price:
                color="green"
            elif ticker_price < old_price:
                color="red"
            else:
                color="black"
            lblObj.set_markup(
                "<span foreground='{}'>{:13.7f} </span>".format(color, ticker_price)
            )

        for (currency, lblObj) in self.lastupdate_label.items():
            if self.__timemode == 0:
                t_lastupdated = str( time.ctime(self.__ticker.getCrypto(currency).getLastUpdated()) )
            else:
                t_lastupdated = str(
                    int(time.time()) - self.__ticker.getCrypto(currency).getLastUpdated()
                )
            lblObj.set_text(t_lastupdated)

        # Required so that the timeout keeps running
        return True

    def start(self):
        # We have to start somewhere...
        Gtk.main()

if __name__ == '__main__':
    t = Application()
    t.start()

