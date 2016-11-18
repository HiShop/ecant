#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging as LOG
import datetime
from pymongo import MongoClient

def name():
    return 'MongoDB存储'

def version():
    return '1.0.0'

def onLoad(ant):
    global db
    db = MongoClient('mongodb://ecantdbo:qwe123123@localhost/ecant').ecant

def onCategoryLoaded(ant, categories):
    for c in categories:
        #printExtraInfo(c)
        traverseCategory(None, c, 0)
        LOG.debug('')

def traverseCategory(p, c, depth):
    printCategoryInfo(c, depth)
    updateCategory(p, c)

    if 'subs' in c and len(c['subs']) > 0:
        for s in c['subs']: traverseCategory(c, s, depth + 1)

def updateCategory(p, c):
    catm = {
        '_id': c['cid'],
        'name': c['name'],
        'url': c['url'],
        'fetchable': c['fetchable'],
        'provider': 'JD',
        'last_update': datetime.datetime.now()
    }

    if 'subs' in c:
        catm['subs'] = [s['cid'] for s in c['subs']]

    if p:
        catm['parent'] = p['cid']
   
    query = {'_id': catm['_id']}
    update = {'$set': catm}

    db.categories.update_one(query, update, upsert = True)

def printExtraInfo(c):
    names = ', '.join([t['name'] for t in c['zhuti']])
    LOG.debug('共 %d 个主题馆：%s' % (len(c['zhuti']), names))

    brands = ', '.join([t['name'] for t in c['brands']])
    LOG.debug('共 %d 个品牌：%s' % (len(c['brands']), brands))

def printCategoryInfo(c, depth):
    lpad = '    ' * depth
    if c['fetchable']:
        LOG.debug('%s %s [%s] - %s' % (lpad, c['name'], c['cid'], c['url']))
    else:
        LOG.debug('%s %s' % (lpad, c['name']))

