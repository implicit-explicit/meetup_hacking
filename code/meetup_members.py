#!/usr/bin/env python3

import requests
import json
import sys

api_url = 'https://api.meetup.com/2/'
query = 'members'

def main(argv):

    page_size = 200

    api_key = argv[0]
    group_urlname = argv[1]
    if(len(argv) > 2):
        page_size = argv[2]

    get_members(api_key, group_urlname, page_size)


def get_members(api_key, group_urlname, page_size=200):

    offset = 0
    results = None
    users = []

    while True:
        request_string = '{}{}?key={}&group_urlname={}&page={}&offset={}'.format(api_url, query, api_key, group_urlname, page_size, offset)

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

        if num != page_size:
            break

        offset += 1

    print(json.dumps(users, indent=2))

if __name__ == "__main__":
    main(sys.argv[1:])