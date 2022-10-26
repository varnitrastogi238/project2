import json
from datetime import datetime
import random
from sqlalchemy import false
from sympy import div
from datamanagement.models import *
import yfinance as yf
import math
import pandas as pd
import time as tim
from smartapi import SmartConnect
from smartapi import SmartWebSocket
from .background_functions import *
from pytz import timezone
import traceback
import sys
import yfinance as yf
from finta import TA
import pyotp

#######################################
# CHECKING BOTS
try:
    import telepot
    bot = telepot.Bot('5764368331:AAGrun4IEIUf75APRxcp_IXZmUz_oeavUGo')
    bot.getMe()
except:
    pass
#######################################

from datetime import time, datetime
# import telepot
# bot = telepot.Bot("5448843199:AAEKjMn2zwAyZ5tu8hsLIgsakxoLf980BoY")
# bot.getMe()
import logging
# logger = logging.getLogger('dev_log')


class run_strategy():

    def __init__(self, strategy):
        self.parameters = strategy
        self.current = -1
        self.till_buy = -1
        self.till_sell = -1
        self.stoploss = -1
        self.take_profit = -1
        self.position = "off"
        self.position_buy = "off"
        self.parameters.stoploss = int(self.parameters.stoploss)
        self.parameters.takeprofit = int(self.parameters.takeprofit)
        self.parameters.amount_invested = int(self.parameters.amount_invested)
        self.parameters.bb = int(self.parameters.bb)
        self.parameters.difference = int(self.parameters.difference)

    def ltp_nifty_options(self):
        # print()
        self.current = self.obj.ltpData(
            "NSE", 'BANKNIFTY', "26009")['data']['ltp']

    def main(self):
        self.current = self.obj.ltpData(
            "NSE", 'BANKNIFTY', "26009")['data']['ltp']
        if self.current < self.stoploss and self.position == "on":
            # close position
            self.real_orders(self.current_position.symbol, "SELL")
            self.current_position.status = "CLOSED"
            self.current_position.price_out = self.current
            self.current_position.time_out = datetime.now(
                timezone("Asia/Kolkata"))
            self.current_position.pnl = self.current-self.current_position.price_in
            self.current_position.save()
            self.position = "off"
            self.position_buy = "off"
            # buy

        if self.current > self.take_profit and self.position == "on":
            # close position
            self.real_orders(self.current_position.symbol, "SELL")
            self.current_position.status = "CLOSED"
            self.current_position.price_out = self.current
            self.current_position.time_out = datetime.now(
                timezone("Asia/Kolkata"))
            self.current_position.pnl = self.current-self.current_position.price_in
            self.current_position.save()
            self.position = "off"
            self.position_buy = "off"
            # sell

    def login(self):
        try:
            self.obj = SmartConnect(api_key=self.parameters.angel_api_keys)
            data = self.obj.generateSession(
                self.parameters.angel_client_id, self.parameters.angel_password, pyotp.TOTP(self.parameters.totp).now())
            refreshToken = data['data']['refreshToken']
            self.feedToken = self.obj.getfeedToken()
        except:
            tim.sleep(1)

    def buy_check(self, msl_high):
        print("x")
        self.current = self.obj.ltpData(
            "NSE", 'BANKNIFTY', "26009")['data']['ltp']
        if self.current > msl_high and self.position == "off":
            print("x1")
            itm = int(self.current/100)
            itm *= 100
            if self.current % 100:
                itm += 100
            temp_symbol = 'BANKNIFTY' + \
                str(self.parameters.weekly_expiry)+str(itm)+'CE'
            self.add_positions(temp_symbol, "BUY", self.current, 0, 0)
            # buy
            self.position = "on"
            self.position_buy = "on"
            self.till_buy = 1
            self.stoploss = self.current-self.parameters.stoploss
            self.take_profit = self.current+self.parameters.takeprofit

    def sell_check(self, msh_low):
        print("y")
        self.current = self.obj.ltpData(
            "NSE", 'BANKNIFTY', "26009")['data']['ltp']
        if self.current < msh_low and self.position == "off":
            print("y1")
            # sell
            itm = int(self.current/100)
            itm *= 100
            if self.current % 100:
                itm += 100
            temp_symbol = 'BANKNIFTY' + \
                str(self.parameters.weekly_expiry)+str(itm)+'PE'
            self.add_positions(temp_symbol, "BUY", self.current, 0, 0)
            self.position = "on"
            self.position_buy = "on"
            self.till_sell = 1
            self.stoploss = self.current-self.parameters.stoploss
            self.take_profit = self.current+self.parameters.takeprofit

    def websocket(self):
        self.login()
        start_of_candle = -1
        self.df = yf.download("^NSEBANK", period='2d', interval="1m")
        bot_candle=-1
        while True:
            try:
                if time(15, 15) <= datetime.now(timezone("Asia/Kolkata")).time():
                    if self.position == "on":
                        self.real_orders(self.current_position.symbol, "SELL")
                        self.current_position.status = "CLOSED"
                        self.current_position.save()
                        self.position = "off"
                        self.position_buy = "off"
                    return "done_fire_fire"
                temp = strategy.objects.get(username="VVZV1042")
                if bot_candle != datetime.now(timezone("Asia/Kolkata")).minute and datetime.now(timezone("Asia/Kolkata")).time().minute % 10 == 0:
                    bot_candle = datetime.now(
                        timezone("Asia/Kolkata")).minute
                    try:
                        bot.sendMessage(
                            1190128536, f"lets see if it works,position-{self.position},buy-{self.poition_buy},sell-{self.position_sell},till buy-{self.till_buy},till sell-{self.till_sell}")
                    except:
                        pass
                if temp.bot == "off":
                    return "done_double_fire"
                if self.position == "on":
                    self.current_position.pnl = self.current-self.current_position.price_in
                    self.current_position.current_price = self.current
                    self.current_position.save()
                    temp2 = stop_symboll.objects.filter(
                        symbol=self.current_position.symbol)
                    if temp2:
                        self.real_orders(self.current_position.symbol, "SELL")
                        self.current_position.status = "CLOSED"
                        self.current_position.price_out = self.current
                        self.current_position.time_out = datetime.now(
                            timezone("Asia/Kolkata"))
                        self.current_position.pnl = self.current-self.current_position.price_in
                        self.current_position.save()
                        self.position = "off"
                        self.position_buy = "off"
                        stop_symboll.objects.all().delete()
                if start_of_candle != datetime.now(timezone("Asia/Kolkata")).minute:
                    start_of_candle = datetime.now(
                        timezone("Asia/Kolkata")).minute
                    tim.sleep(5)
                    self.df = yf.download(
                        "^NSEBANK", period='2d', interval="1m")
                if self.position == "off" and self.df['Close'][-2] > self.df['Open'][-2] and self.df['Close'][-4] <= self.df['Open'][-4] and self.df['Close'][-3] <= self.df['Open'][-3] and self.df['Close'][-4] >= self.df['Close'][-3] and self.df['Close'][-2] > self.df['Close'][-4]:
                    if self.till_buy == -1 and self.till_sell == -1:
                        self.buy_check(self.df['High'][-2])
                    else:
                        self.df1 = TA.BBANDS(self.df, self.parameters.bb)
                        for i in range(4):
                            if self.df['Low'][-(i+3)] < self.df1['BB_LOWER'][-(i+3)]:
                                if self.df['Low'][-2] < self.df1['BB_LOWER'][-2] or self.df['Low'][-3] < self.df1['BB_LOWER'][-3]:
                                    if self.df1['BB_LOWER'][-2]-self.df['Low'][-2] < self.parameters.difference:
                                        self.buy_check(self.df['High'][-2])
                                else:
                                    self.buy_check(self.df['High'][-2])
                if self.position == "off" and self.df['Open'][-2] > self.df['Close'][-2] and self.df['Open'][-4] <= self.df['Close'][-4] and self.df['Close'][-3] <= self.df['Open'][-3] and self.df['Close'][-4] >= self.df['Close'][-3] and self.df['Close'][-2] < self.df['Close'][-3]:
                    if self.till_sell == -1 and self.till_buy == -1:
                        self.sell_check(self.df['Low'][-2])
                    else:
                        self.df1 = TA.BBANDS(self.df, self.parameters.bb)
                        for i in range(4):
                            if self.df['High'][-(i+3)] > self.df1['BB_UPPER'][-(i+3)]:
                                if self.df['High'][-2] < self.df1['BB_UPPER'][-2] or self.df['High'][-3] < self.df1['BB_UPPER'][-3]:
                                    if self.df1['BB_UPPER'][-2]-self.df['High'][-2] < self.parameters.difference:
                                        self.sell_check(self.df['Low'][-2])
                                else:
                                    self.sell_check(self.df['Low'][-2])
                if self.position == "on":
                    self.main()

            except Exception as e:
                print(traceback.format_exc())
                try:
                     bot.sendMessage(
                            1190128536, f"exception aagya bro {e}")
                except:
                    pass
                #logger.info(str(traceback.format_exc()))

    def real_orders(self, symbol, side):
        dff = pd.read_csv('datamanagement/helpful_scripts/scripts.csv')
        token = "hi"
        for i in range(len(dff)):
            if symbol in dff['symbol'][i]:
                token = dff.loc[i]['token']
                break
            else:
                continue
        if self.parameters.paper == "off":
            if side == "LONG":
                side = "BUY"
            else:
                side = "SELL"
            try:
                orderparams = {
                    "variety": "NORMAL",
                    "tradingsymbol": str(symbol),
                    "symboltoken": str(token),
                    "transactiontype": str(side),
                    "exchange": "NFO",
                    "ordertype": "MARKET",
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "quantity": str(int(self.parameters.amount_invested)*25)
                }
                orderId = self.obj.placeOrder(orderparams)
                print("The order id is: {}".format(orderId))
            except Exception as e:
                print("Order placement failed: {}".format(e.message))

    def add_positions(self, symbol, side, price_in, time_out, price_out):
        print("z")
        dff = pd.read_csv('datamanagement/helpful_scripts/scripts.csv')
        token = "hi"
        for i in range(len(dff)):
            if symbol in dff['symbol'][i]:
                token = dff.loc[i]['token']
                break
            else:
                continue
        strategy1 = positions(
            symbol=symbol,
            time_in=datetime.now(timezone("Asia/Kolkata")),
            side=str(side),
            price_in=float(price_in),
            time_out=datetime.now(timezone("Asia/Kolkata")),
            price_out=float(price_out),
            status="OPEN",
            token=str(token),
            quantity=int(self.parameters.amount_invested)*25
        )
        self.current_position = strategy1
        strategy1.save()
        self.real_orders(symbol, side)

    def run(self):
        try:
            value = self.websocket()
            return value
        except Exception:
            print(traceback.format_exc())
            # logger.info(str(traceback.format_exc()))
