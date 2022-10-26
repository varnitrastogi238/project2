import logging
from django.http import HttpResponse
import telepot
from django.shortcuts import render
from .helpful_scripts.strategy import *
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth.models import User
from django.contrib import messages
import threading
from datamanagement.models import strategy
import random
import string
from .models import positions,  strategy
from datamanagement.helpful_scripts.background_functions import *
from smartapi import SmartConnect
import time as tim
from smartapi import SmartConnect
from smartapi import SmartWebSocket
from django.contrib.auth import authenticate,  login, logout
from django.shortcuts import render, redirect
# logger = logging.getLogger('dev_log')
import requests
import pandas as pd
from datetime import datetime,time
from pytz import timezone
# obj = SmartConnect(api_key="NuTmF22y")
# data = obj.generateSession("Y99521", "abcd@1234")
# refreshToken = data['data']['refreshToken']
# feedToken = obj.getfeedToken()
# print(feedToken)
sleep_time=0
# working_day_calculation(0)


def this_scripts():
    url="https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    data=requests.get(url=url)
    data=data.json()
    df = pd.DataFrame(data)
    df1=df[:1]
    for i in range(len(df)):
        print(i)
        if 'BANKNIFTY' in df['symbol'][i][:12] and 'NFO' in df['exch_seg'][i]:
            df1.loc[len(df1.index)] = df.loc[i] 
        else:
            continue
    df1.to_csv("datamanagement/helpful_scripts/scripts.csv")

def extra_work():
    check_val=0
    print("klsjfkljslkdfj")
    while True:
        try:
            if time(9,15) <= datetime.now(timezone("Asia/Kolkata")).time() and check_val == 0:
                check_val=1
                strategy1=strategy.objects.get(username="VVZV1042")
                strategy1.bot="on"
                strategy1.save()
                this_scripts()
                t = threading.Thread(target=do_something, args=[strategy1])
                t.setDaemon(True)
                t.start()
            if time(8, 1) <= datetime.now(timezone("Asia/Kolkata")).time() and time(8, 15) >= datetime.now(timezone("Asia/Kolkata")).time() and check_val==1:
                check_val=0
            tim.sleep(600)
        except Exception as e:
            print(e)
            # logger.info(str(e))

th = threading.Thread(target=extra_work)
th.setDaemon(True)
th.start()


@login_required(login_url='/option_bot/login_page')
def index(request):
    strategy1=strategy.objects.get(username="VVZV1042")
    return render(request, "index.html",{'list':strategy1})

@login_required(login_url='/option_bot/login_page')
def position(request):

    position = positions.objects.filter(status="OPEN")
    return render(request, "position.html",    {
        'list': position
    })
@login_required(login_url='/option_bot/login_page')
def stop_symbol(request):
    symboll=request.POST['symbol']
    stop = stop_symboll(
            symbol=symboll,
        )
    stop.save()
    position = positions.objects.filter(status="OPEN")
    return render(request, "position.html",{'list':position})

@login_required(login_url='/option_bot/login_page')
def stop_all(request):
    position = positions.objects.filter(status="OPEN")
    for p in position:
        stop = stop_symboll(
            time_in=p.time_in,
        )
        stop.save()
    return render(request, "index.html",{'list':position})

@login_required(login_url='/option_bot/login_page')
def closed_positions(request):
    position = positions.objects.filter(status="CLOSED")
    return render(request, "closed_position.html",    {
        'list': position
    })


def start_strategy(request):
    if request.method == "POST":
        # monthly_expiry=request.POST['monthly_expiry']
        strategy1=strategy.objects.get(username="VVZV1042")
        strategy1.angel_api_keys=request.POST['angel_api_keys']
        strategy1.angel_client_id=request.POST['angel_client_id']
        strategy1.angel_password=request.POST['angel_password']
        strategy1.totp=request.POST['totp']
        strategy1.amount_invested=request.POST[ 'amount_invested']
        strategy1.stoploss=request.POST['stoploss']
        strategy1.takeprofit=request.POST['takeprofit']
        strategy1.paper=request.POST['paper']
        strategy1.bot=request.POST['bot']
        strategy1.amount_invested=request.POST['amount_invested']
        strategy1.difference=request.POST['difference']
        strategy1.bb=request.POST['bb']
        strategy1.weekly_expiry=request.POST['expiry']
        strategy1.save()
        # if strategy1.bots_started==0:
        
        return redirect("../../option_bot/index")

    strategy1=strategy.objects.get(username="VVZV1042")
    return redirect("../../option_bot/index")


def do_something(strategy):
    print("hii2")
    strat = run_strategy(strategy)
    value=strat.run()
    if value!=None:
        return value




######################################################################################################################

def login_page(request):
    return render(request, "login.html")


def handleLogin(request):

    if request.user.is_authenticated:
        return redirect('/../../option_bot/index')
    if request.method == "POST":

        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        # user = authenticate(username=loginusername, password=loginpassword)
        if loginpassword=="Zopper@123" and loginusername=="VVZV1042":
            user=User.objects.get(username=loginusername)
            login(request, user)
            return redirect("/../../option_bot/index")
        else:
            print(loginusername)
            print(loginpassword)
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/option_bot/login_page")
    return redirect("/option_bot/login_page")


def handleLogout(request):
    logout(request)
    return redirect('../../option_bot/login_page')