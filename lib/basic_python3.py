#! /usr/bin/env

'''
These are helper functions for the Basic Programs with Python3 workshop. The
goal is to use only the standard library, to avoid complications of package
installations.

More information at http://ningyuan.io/basic-python3

All helper functions are defined in this one file for ease of import. To help
you navigate this file, the functions are divided into categories, each with
their own headers in a multiline comment. The headers (exact), and their
descriptions are:

    {HEADER NAME} - {DESCRIPTION}

    TELEGRAM API  - Functions which interact with the telegram API
    WEATHER API   - Functions which interact with the NEA air-temperature API

'''

import json, time, urllib.parse, urllib.request

'''
TELEGRAM API
'''

telegram_url = 'https://api.telegram.org/bot{key}/{method}'
weather_url = 'https://api.data.gov.sg/v1/environment/air-temperature?{param}={time}'

def telegram_whoami(key):
    """ GET telegram method getMe

    returns list(first_name: str, username: str)
    """
    assert type(key) == str, 'The argument must be of type str'
    url = telegram_url.format(key=key, method='getMe')
    resp = urllib.request.urlopen(url)
    body = resp.readline().decode()
    result = json.loads(body)['result']
    return [result['first_name'], result['username']]

def telegram_send(key, chat_id, text):
    """ POST telegram method sendMessage

    parse_mode is set to telegram's Markdown
        *bold*, _italics_, `inline code`
    returns True if successful, raises appropriate Exception otherwise
    """
    url = telegram_url.format(key=key, method='sendMessage')
    url = '{base}?chat_id={chat_id}&text={text}&parse_mode=Markdown'.format(
        base=url, chat_id=chat_id, text=urllib.parse.quote(text)
    )
    return urllib.request.urlopen(url).status == 200

"""
WEATHER API
"""

def weather_get_now():
    """ GET the latest weather data

    returns list<float>
    """
    url = weather_url.format(param='datetime', time=strftime_now())
    resp = urllib.request.urlopen(url)
    body = resp.readline().decode()
    result = json.loads(body)
    readings = result['items'][0]['readings']
    temperatures = map(lambda x: x['value'], readings)
    return list(temperatures)

def strftime_now():
    """ Returns current time in the format specified by the weather api

    returns YYYY-MM-DD[T]HH:mm:ss
    """
    return strftime(time.localtime())

def strftime(time_tuple):
    """ Returns given time tuple in the format specified by the weather api

    returns YYYY-MM-DD[T]HH:mm:ss
    """
    return time.strftime('%Y-%m-%dT%H:%M:%S', time_tuple)
