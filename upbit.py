import pyupbit
import pandas as pd
import os
import sqlite3
import requests
import time
import datetime
import json


class Upbit:
    def __init__(self):
        with open("user_param.json") as f:
            self.user_param = json.load(f)
        self.upbit = pyupbit.Upbit(self.user_param['access_key'], self.user_param['secret_key'])

    def get_tickers(self):
        return pyupbit.get_tickers()

    def get_current_price(self, tickers: list):
        return pyupbit.get_current_price(tickers)

    def get_balance(self):
        return self.upbit.get_balance()

    def get_hoga(self, ticker):
        return pyupbit.get_orderbook(ticker)

    def buy_order(self, ticker, buy_price, quantity):
        try:
            res = self.upbit.buy_limit_order(ticker, buy_price, quantity)
        except Exception as e:
            print(e)
            return
        return pd.Series(res, name="buy_order").to_frame().T

    def sell_order(self, ticker, sell_price, quantity, type='limit'):
        if type == 'market':
            res = self.upbit.sell_market_order(ticker, sell_price, quantity)
        else:
            try:
                res = self.upbit.sell_limit_order(ticker, sell_price, quantity)
            except Exception as e:
                print(e)
                return
        return pd.Series(res, name="sell_order").to_frame().T

    def cancel_order(self, order_id):
        res = self.upbit.cancel_order(order_id)
        return pd.Series(res, name="cancel_order").to_frame().T
