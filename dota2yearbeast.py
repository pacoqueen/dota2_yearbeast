#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, curl, datetime
from dateutil import tz
from collections import OrderedDict
import pandas as pd

DEBUG = True

def parse_json_data(sdata):
    """
    Load data from string (json) and parse dates to local time.
    Return an ordered dict (reversed in time) with raw data and dates as keys.
    """
    data = json.loads(sdata)
    # parsing date data
    _data = OrderedDict()
    for d in data:
        fechahora = datetime.datetime.utcfromtimestamp(float(d['timestamp']))
        # UTC -> local time
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        fechahora = fechahora.replace(tzinfo = from_zone)
        fechahora = fechahora.astimezone(to_zone)
        _data[fechahora] = d
    return _data

def get_json_data():
    """
    Load pasts events from http://2015.yearbeast.com/ (reddit powah!)
    """
    c = curl.Curl()
    data = c.get("http://2015.yearbeast.com/history.json")
    data = parse_json_data(data)
    if DEBUG:
        for fh in reversed(data.keys()):
            if fh >= datetime.datetime.now(tz.tzlocal()):
                print "==>",
            else:
                print "-->",
            print fh.strftime("%d/%m/%Y %H:%M")
    return data

def extract_abs_hours(history):
    """
    Only extract hours as string for frequency table.
    """
    # TODO: PORASQUI.
    return history

def adivinar(history):
    """
    Naive guess of future nexts events based on deltas between past dates and
    confirmed new one (probably on future).
    Deltas always between 2 and 3 hours. Sure, Volvo? (I think it doesn't count
    interval time when beast is alive. So it's 2 and 3 hours but between
    events' end time and start time.
    """
    horas = extract_abs_hours(history)
    s = pd.Series(horas)
    if DEBUG:
        print s
    try:
        last_event = history.keys()[0]
        delta = last_event - history.keys()[1]
    except IndexError:
        res = ["Not enough data"]
    else:
        res = [last_event + delta]
    return res

def main():
    """
    Get json data from past events and try to guess the next one.
    """
    history = get_json_data()
    next_matches = adivinar(history)
    for nm in next_matches:
        print nm.strftime("%d/%m/%Y %H:%M")

if __name__ == "__main__":
    main()
