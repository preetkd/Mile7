
from datetime import timedelta
from urllib.request import urlopen
import csv
import urllib3
import re
import pandas as pd
from datetime import datetime, date
from pandas.tseries.offsets import BDay
import calendar



def MonthlyPay(date):
    preddate = date + timedelta(days=30)
    preddate1 = preddate
    if preddate.weekday() == 6:
        preddate1 = preddate - timedelta(days=2)
    if preddate.weekday() == 5:
        preddate1 = preddate - timedelta(days=1)

    p_dt = preddate1.month                               # Checking for month to be may '5'
    if p_dt == 4:
        preddate1 = preddate1+timedelta(days=7)
    preddate12 = preddate1.strftime('%Y-%m-%d')
    return preddate12


def BiWeeklyPay(dateL, dateF , dateF0):
    print('biweek@@@@@@@@@@@@@@@@', dateL ,dateF,dateF0)
    preddate = dateL+ timedelta(days=1)         # Creating a date variable
    print('weekdays %%%%%%%',dateF.day,dateF0.day)
    if dateF.day == dateF0.day:
        preddate = dateF + timedelta(days=30)
        print(preddate,"iiifffffflooop")
    else:preddate = dateL + timedelta(days=14)
    print(preddate, "ooouttlooop")
    p_dt = preddate.month
    if p_dt == 4:                                       # Checking for month to be may '5'
       preddate = preddate + timedelta(days=7)
    #preddate = date + BDay(11)
    return convert_to_weekday(preddate)


def ThreeWeeklyPay(dateF, dateL):
    preddate = dateF + timedelta(days=14)
    p_dt = preddate.month
    if p_dt == 4:  # Checking for month to be may '5'
        preddate = preddate + timedelta(days=7)
    # preddate = date + BDay(11)
    return convert_to_weekday(preddate)


def WeeklyPay(dateF, dateL):
    pre_date = dateF + timedelta(days=7)

    if pre_date.weekday() == 6:
        pre_date = pre_date + timedelta(days=1)
    if pre_date.weekday() == 5:
        pre_date1 = pre_date + timedelta(days=2)

    p_dt = pre_date.month  # Checking for month to be may '5'
    if p_dt == 4:
        pre_date = pre_date + timedelta(days=7)

    pre_date1 = pre_date.strftime('%Y-%m-%d')
    return pre_date1


def DefaultPay(dateF, dateL):
    delta_diff = 0
    delta = 0
    if dateL == dateF:
       pre_date = dateL + timedelta(days=7)
    else: delta_diff = dateF - dateL     # F - L to avoid negative delta Diff
    if delta_diff == 0:
            delta=7
    else: delta = delta_diff.days

                   # Getting Int of no os days difference
    pre_date = dateF + timedelta(days=delta)
    preddate1 = pre_date

    if pre_date.weekday() == 6:
        preddate1 = pre_date - timedelta(days=2)
    if pre_date.weekday() == 5:
        preddate1 = pre_date - timedelta(days=1)

    p_dt = preddate1.month                      # Checking for month to be may
    if p_dt == 4:
        preddate1 = preddate1 + timedelta(days=7)
    preddate12 = preddate1.strftime('%Y-%m-%d')

    return preddate12


def convert_to_weekday(pay_date):
    rtn_date = pay_date
    if rtn_date.weekday() == 6:
        rtn_date = pay_date - timedelta(days=2)
    if rtn_date.weekday() == 5:
        rtn_date = pay_date - timedelta(days=1)

    rtn_date = rtn_date.strftime('%Y-%m-%d')
    return rtn_date