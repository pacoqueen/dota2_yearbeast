#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, curl, datetime
from dateutil import tz
from collections import OrderedDict

DEBUG = True

def parse_json_data(sdata):
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
    c = curl.Curl()
    data = c.get("http://2015.yearbeast.com/history.json")
    data = parse_json_data(data)
    if DEBUG:
        for fh in reversed(data.keys()):
            print "-->", fh.strftime("%d/%m/%Y %H:%M")
    return data

def adivinar(history):
    last_event = history.keys()[0]
    delta = last_event - history.keys()[1]
    return [last_event + delta]

def main():
    history = get_json_data()
    next_matches = adivinar(history)
    for nm in next_matches:
        print nm.strftime("%d/%m/%Y %H:%M")

if __name__ == "__main__":
    main()
