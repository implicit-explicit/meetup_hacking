#!/usr/bin/env python3
import eventlet
eventlet.monkey_patch()

import json
import sys

import arrow
import requests
from flask import Flask, request
app = Flask(__name__, static_url_path='')

API_URL = 'https://api.meetup.com/2/'
QUERY = 'members'
API_KEY = '5c5b2c745132111c686cb32d136428'
PAGE_SIZE = 200

logger = app.logger

def main(argv):

    page_size = 200

    api_key = argv[0]
    group_urlname = argv[1]
    if(len(argv) > 2):
        page_size = argv[2]

    get_members(api_key, group_urlname, page_size)


def get_members(api_key, group_urlname, page_size=200):

    results = None
    users = []

    request_string = '{}{}?key={}&group_urlname={}&page={}'.format(API_URL, QUERY, api_key, group_urlname, page_size)

    while True:

        # print(request_string)

        r = requests.get(request_string)
        try:
            results = json.loads(r.content.decode('utf-8'))
        except Exception as e:
            print(e)

        # print(results)

        num = len(results['results'])
        users += results['results']

        # print(num)

        try:
            if len(results['meta']['next']) <= 0:
                break
        except e:
            print(e)
            break

        request_string = results['meta']['next']

    return users


def members_over_time(members):
    timezone = "CET"
    members.sort(key = lambda member: member['joined'])

    count = 0
    last_bucket = None
    buckets = {}

    for member in members:
        joined = arrow.get(member['joined']/1000).to(timezone)
        bucket = joined.replace(hour=0, minute=0, second=0)

        if last_bucket and last_bucket != bucket:
            buckets[last_bucket.timestamp] = count

        count += 1
        last_bucket = bucket

    return buckets


@app.route('/meetup')
def get_meetup_members():
    name = request.args.get('name')
    logger.info('Pulling info for group {}'.format(name))
    members = get_members(API_KEY, name, PAGE_SIZE)
    members_series = members_over_time(members)
    logger.info('Finished request for group {}'.format(name))
    return json.dumps(members_series)


@app.route("/")
def index():
    return app.send_static_file('members.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
