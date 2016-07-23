#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import csv
import json
import requests
import ConfigParser

COUNTER_DIR = '/tmp'
GOOGLE_API_URL = 'https://www.googleapis.com/urlshortener/v1/url?key='
CHATWORK_API_URL = 'https://api.chatwork.com/v1/rooms/'

def shorten_url(api_key, long_url):
    api_url = GOOGLE_API_URL + api_key
    long_url = long_url.encode('utf-8')
    body = '{longUrl: "%s"}' % long_url
    headers = {'Content-Type': 'application/json'}
    req = requests.session()
    res = req.post(api_url, data=body, headers=headers)
    return json.loads(res.text).get('id')

def get_counter(counter_file):
    f = open(counter_file, "r+")
    count = int(f.read())
    f.close()
    return count

def update_counter(counter_file):
    f = open(counter_file, "r+")
    count = int(f.read())
    count += 1
    f.seek(0)
    f.write(str(count))
    f.close()

def reset_counter(counter_file, initial_count):
    f = open(counter_file, "w")
    f.write(str(initial_count))
    f.close()

def send_chatwork(room_id, token, message):
    url = CHATWORK_API_URL + room_id + '/messages'
    headers = {'X-ChatWorkToken': token}
    req = requests.session()
    res = req.post(url, data={'body': message}, headers=headers)

if __name__ == "__main__":
    args = sys.argv
    argc = len(args)

    if argc != 3:
        print '%s chatwork_room_id csv_filename' % (args[0])
        quit()

    chatwork_room_id = args[1]
    csv_filename = args[2]

    cwd = os.path.abspath(os.path.dirname(__file__))
    env_file = cwd + '/.env'

    if not os.path.isfile(env_file):
        print 'ERROR: %s is not found' % env_file
        quit()

    config = ConfigParser.SafeConfigParser()
    config.read(env_file)
    google_api_key = config.get("google", "api_key")
    chatwork_token = config.get("chatwork", "token")

    csv_file = cwd + '/' + csv_filename
    if not os.path.isfile(csv_file):
        print 'ERROR: %s is not found' % csv_file
        quit()

    name, ext = os.path.splitext(csv_filename)
    counter_file = COUNTER_DIR + '/' + name + '.cnt'

    if not os.path.isfile(counter_file):
        reset_counter(counter_file, 1)

    article_count = get_counter(counter_file)

    f = open(csv_file, "rb")
    reader = csv.reader(f)

    # 先頭行はメインタイトル
    main_title = reader.next()[0]

    line_count = 0
    for row in reader:
        line_count += 1
        if line_count != article_count:
            continue
        title = row[0]
        if len(row) == 2:
            short_url = str(shorten_url(google_api_key, row[1]))
        else:
            short_url = ''
        message = '[info][title]' + main_title + '[/title]' + title + ' ' + short_url + '[/info]'
        send_chatwork(chatwork_room_id, chatwork_token, message)
    f.close()

    if article_count == line_count:
        reset_counter(counter_file, 1)
    else:
        update_counter(counter_file)
