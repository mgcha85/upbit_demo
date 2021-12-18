import datetime
import pause
import time
import pandas as pd


class Buy:
    def __init__(self, upbit, user_param, con, cond):
        self.upbit = upbit
        self.user_param = user_param
        self.con = con
        self.cond = cond

    def algorithm(self):
        # input: None
        # output: 사야할 코인의 tickers
        return ['KRW-BTC']

    def run(self):
        while True:
            tickers = self.algorithm()

            if len(tickers) > 0:
                #  내 계좌의 현재 베팅 가능 금액을 리턴
                balance = self.upbit.get_balance()
                # 매수 하려는 tickers의 현재가를 리턴
                prices = self.upbit.get_current_price(tickers)

                # 각 코인의 베팅금액을 계산
                each_bet = balance / len(tickers)
                contents = []
                for ticker in tickers:
                    price = prices[ticker]
                    qty = each_bet / price
                    res = self.upbit.buy_order(ticker, price, qty)
                    now = datetime.datetime.now().replace(microsecond=0)
                    contents.append([res['order_id'], ticker, price, qty, now, 'buy', 'yet'])

                df_order = pd.DataFrame(contents, columns=['order_id', 'ticker', 'price', 'qty', 'buy_time', 'side', 'status'])
                df_order.to_sql('order_list', self.con, if_exists='append')

            time.sleep(0.25)

