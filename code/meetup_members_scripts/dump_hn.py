#!/usr/bin/env python3

import eventlet
eventlet.monkey_patch()

import requests
import json
from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Integer
from elasticsearch_dsl.connections import connections

API_URL = 'https://hacker-news.firebaseio.com/v0'
ELASITCSEARCH_URL = ''
EVENTLET_CONCURRENCY = 50

connections.create_connection(hosts=[ELASITCSEARCH_URL])

def main():
    max_id = get_max_item_id()
    min_id = 0

    Item.init()
    get_items(min_id, max_id)

class Item(DocType):
    user = String()
    hnid = Integer()
    descendants = Integer()
    kids = String(index='not_analyzed')
    score = Integer()
    text = String(analyzer='snowball')
    time = Date()
    title = String(analyzer='snowball', fields={'raw': String(index='not_analyzed')})
    type = String()
    url = String(index='not_analyzed')


    class Meta:
        index = 'hackernews'


def get_max_item_id():
    query = 'maxitem.json'
    request_string = '{}/{}'.format(API_URL, query)

    r = requests.get(request_string)
    try:
        result = json.loads(r.content.decode('utf-8'))
    except Exception as e:
        print(e)
    return result

def get_item(item_id):
    query = 'item'
    request_string = '{}/{}/{}.json'.format(API_URL, query, item_id)

    r = requests.get(request_string)
    try:
        result = json.loads(r.content.decode('utf-8'))
    except Exception as e:
        print(e)
    return result


def get_items(min_id, max_id):

    pool = eventlet.GreenPool(EVENTLET_CONCURRENCY)
    ids = reversed(range(min_id, max_id))
    for id in pool.imap(save_item, ids):
        print('Finnished processing {}'.format(id))


def save_item(id):
    item = get_item(id)
    if not item:
        item = {'id': 0, 'by': '_failed'}
    descendants = item.get('descendants', 0)
    kids = item.get('kids', None)
    score = item.get('score', None)
    text = item.get('text', None)
    title = item.get('title', None)
    url = item.get('url', None)
    type = item.get('type', None)
    time_unix = item.get('time', 0)
    time = datetime.fromtimestamp(time_unix)
    if item.get('deleted', None):
        print('Skipping item {}'.format(item['id']))
    else:
        try:
            print('Saving item {} with data: {}'.format(item['id'], str(item)))
            es_item = Item(hnid=item['id'], user=item['by'], descendants=descendants, kids=kids, score=score, text=text,
                           time=time, title=title, type=type, url=url)
            es_item.save()
        except KeyError:
            print('Item with missing fields: {}'.format(str(item)))
    return id


if __name__ == "__main__":
    main()