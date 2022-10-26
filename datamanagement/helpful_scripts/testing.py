from tracemalloc import start
import yfinance as yf
from datetime import time, datetime
from pytz import timezone

start_of_candle=-1
while True:
    if start_of_candle!=datetime.now(timezone("Asia/Kolkata")).minute:
        start_of_candle=datetime.now(timezone("Asia/Kolkata")).minute
        df=yf.download("^NSEBANK",period='2d',interval="1m")
        print(df)