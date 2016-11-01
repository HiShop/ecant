#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random
import urllib
import urllib2
import json
from BeautifulSoup import BeautifulSoup

class JDAnt:
    def __init__(self):
        pass

    def run(self, repos):
        cats = self.getCatagory()
        
        util = JDUtil()
        for c in cats: util.printTopCatagory(c)

    def getCatagory(self):
        url = 'http://dc.3.cn/category/get'
        request = urllib2.Request(url)
        res = urllib2.urlopen(request).read()
        js = json.loads(unicode(res, 'gb18030').encode('utf8'))

        cats = [self.walkCatagory(i, 0) for i in js['data']]
        return cats

    def walkCatagory(self, c, depth):
        r = {}
        if depth == 0:
            # 第一层分类使用组合名称
            subs = [self.parseCatagory(i['n']) for i in c['s']]
            r['name'] = ' / '.join([t['name'] for t in subs])
            r['url'] = ''
            r['zhuti'] = [self.parseZhuti(ts) for ts in c['t']]
            r['brands'] = [self.parseBrand(bs) for bs in c['b']]
        else:
            cat = self.parseCatagory(c['n']);
            r['name'] = cat['name']
            r['url'] = self.parseCatagoryLink(cat['url'])

        if 's' in c and len(c['s']) > 0:
            r["subs"] = [self.walkCatagory(s, depth + 1) for s in c['s']]

        return r

    def parseCatagoryLink(self, l):
        r = ''
        if '.' in l: r = 'http://' + l
        else: r = 'http://list.jd.com/list.html?cat=' + l.replace('-', ',')
        return r

    def parseZhuti(self, s):
        # 文本样例：jiadian.jd.com/|家电城||0
        sects = s.split("|")
        return {
            "name": sects[1],
            "url": sects[0]
        }

    def parseBrand(self, s):
        # 文本样例："//haier.jd.com/|海尔|vclist/jfs/t3211/96/3882705424/5364/76e60d4a/57f9fa89N6ddb14fc.jpg|"
        sects = s.split("|")
        return {
            "name": sects[1],
            "url": sects[0],
            "logo": sects[2]
        }

    def parseCatagory(self, s):
        # 文本样例：channel.jd.com/home.html|家居||0
        sects = s.split("|")
        return {
            "name": sects[1],
            "url": sects[0]
        }

class JDUtil:
    def printTopCatagory(self, c):
        names = ', '.join([t['name'] for t in c['zhuti']])
        print('共 %d 个主题馆：%s' % (len(c['zhuti']), names))

        brands = ', '.join([t['name'] for t in c['brands']])
        print('共 %d 个品牌：%s' % (len(c['brands']), brands))

        self.printTree(c, 0)

        print('')

    def printTree(self, c, depth):
        print '    ' * depth + c['name'] + ' ' + c['url']
        if 'subs' in c and len(c['subs']) > 0:
            for s in c['subs']: self.printTree(s, depth + 1)
