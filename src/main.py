# -*- coding: utf-8 -*-
import os
import json
import re
from datetime import date
from datetime import timedelta
from datetime import datetime
import requests

SLACK_URL = os.environ.get('SLACK_URL')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', None)
SLACK_MESSAGE_PREFIX = os.environ.get('SLACK_MESSAGE_PREFIX', u"さぁて今週の connpass イベントは？")
CONNPASS_SERIES_IDS = os.environ.get('CONNPASS_SERIESES', '4071,1717').split(',')

def _seq_days(start=None, max_offset=7):
    if start is None:
        start = date.today()
    for offset in range(max_offset):
        yield start + timedelta(days=offset)

def _get_events(series_id, start_date=None, duration_days=7):
    url = 'https://connpass.com/api/v1/event/'
    for held_date in _seq_days(start=start_date, max_offset=duration_days):
        results_start = 1
        params = {
           'series_id': series_id,
           'ymd': held_date.strftime("%Y%m%d"),
           'start': results_start
        }
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        tail = data['results_returned'] + data['results_available']
        for event in data['events']:
            yield event
        #if tail >= data['results_available']:
        #    raise StopIteration()

def _post_slack(message, url, channel=None):
    headers = { 'Content-type': 'application/json' }
    payload = { 'text': message }
    if channel is not None:
       payload['channel'] = channel
    res = requests.post(url, headers=headers, data=json.dumps(payload))
    res.raise_for_status()

timezone_pattern = re.compile('(.*[\+\-]\d\d):(\d\d)$')
def _date_str(d_str):
    m = timezone_pattern.match(d_str)
    if m is not None:
        d_str = timezone_pattern.sub('\\1\\2', d_str)    
    return datetime.strptime(d_str, "%Y-%m-%dT%H:%M:%S%z").strftime('%m/%d %H:%M')

def my_handler(event, context):
    u'''event handler for AWS Lamnbda'''
    events = []
    for s_id in CONNPASS_SERIES_IDS:
        for event in _get_events(s_id):
            events.append(event)
    events = sorted(events, key=lambda x: x['started_at'])

    message = SLACK_MESSAGE_PREFIX + "\n"
    for event in events:
        date_str = _date_str(event['started_at'])
        message += u'{d} から <{event_url}|{title}>\n'.format(d=date_str, **event)

    if len(events) > 0:
        message += u"の {} 本でお届けします！".format(len(events))
    else:
        message += u"NO PLAN です！"
    _post_slack(url=SLACK_URL, message=message)

if __name__ == '__main__':
    my_handler(None, None)

