import datetime
import pause
import time
import pandas as pd


class Sell:
    def __init__(self, upbit, user_param, con, cond):
        self.upbit = upbit
        self.user_param = user_param
        self.con = con
        self.cond = cond

    def sell_algo(self, ticker):
        return True

    def run(self):
        while True:
            df_hold = pd.read_sql("SELECT * FROM 'hold_list'", self.con)
            if not df_hold.empty:
                trade_prices = self.upbit.get_current_price(df_hold['ticker'])
                if trade_prices is None:
                    time.sleep(1)
                    continue

                df_hold = df_hold.set_index('ticker')
                for ticker, current_price in trade_prices.items():
                    buy_price = df_hold.loc[ticker, 'buy_price']
                    sell_price = df_hold.loc[ticker, 'sell_price']  # 목표가
                    stop_price = df_hold.loc[ticker, 'stop_price']  # stoploss
                    side = df_hold.loc[ticker, 'side']
                    order_id = df_hold.loc[ticker, 'id']
                    due_date = datetime.datetime.strptime(df_hold.loc[ticker, 'due_date'], '%Y-%m-%d %H:%M:%S')
                    qty = df_hold.loc[ticker, 'qty']
                    now = datetime.datetime.now().replace(microsecond=0)

                    # stoploss
                    if self.sell_algo(ticker):
                        self.upbit.sell_order(ticker, sell_price, qty)
                    elif current_price <= stop_price:
                        self.upbit.sell_order(ticker, 0, qty, type='market')
                        sell_price = current_price
                    elif current_price >= sell_price:
                        self.upbit.sell_order(ticker, sell_price, qty)
                    elif due_date >= now:
                        self.upbit.sell_order(ticker, 0, qty, type='market')
                        sell_price = current_price

                    df_hold.loc[ticker, 'sell_price'] = sell_price
                    df_hold.loc[ticker, 'sell_date'] = str(datetime.datetime.now().replace(microsecond=0))
                    df_hold.loc[ticker, 'profit'] = (df_hold.loc[ticker, 'sell_date'] - df_hold.loc[ticker, 'buy_date']) * df_hold.loc[ticker, 'qty']

            df_hold.to_sql('order_history', self.con, if_exists='append')
            time.sleep(0.25)
