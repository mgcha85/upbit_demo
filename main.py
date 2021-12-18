from buy import Buy
from sell import Sell
from upbit import Upbit
import sqlite3
import json
import os


with open("user_param.json") as f:
    user_param = json.load(f)


fpath = os.path.join("D:/upbit", "order.db")
con = sqlite3.connect(fpath)


upbit = Upbit()
buy = Buy(user_param, upbit, con, cond)
sell = Sell(user_param, upbit, con, cond)

