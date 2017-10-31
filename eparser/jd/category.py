#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urlparse
import json
import hashlib

class Category:
    def __init__(self):
        pass

    def getTree(self):
        url = 'http://dc.3.cn/category/get'
        request = urllib2.Request(url)
        res = urllib2.urlopen(request).read()
        js = json.loads(unicode(res, 'gb18030').encode('utf8'))

        cats = [self._traverse(i, 0) for i in js['data']]
        return cats

    def _traverse(self, c, depth):
        r = {}
        subjs = []
        r['depth'] = depth
        r['fetchable'] = False
        if depth == 0:
            # 第一层分类使用组合名称
            subs = [self._parseCategory(i['n']) for i in c['s']]
            r['name'] = ' / '.join([t['name'] for t in subs])
            r['url'] = ''
            r['zhuti'] = [self._parseZhuti(ts) for ts in c['t']]
            r['brands'] = [self._parseBrand(bs) for bs in c['b']]
            r['cid'] = self._cacuCid(r['name'])

            if 's' in c and 's' in c['s'][0]:
                subjs = c['s'][0]['s']
        else:
            cat = self._parseCategory(c['n']);
            r['name'] = cat['name']
            url = self._parseLink(cat['url'])
            jdcid = self._getCatId(url)
            r['cid'] = self._cacuCid(r['name'] + url)
            #r['cid'] = self._cacuCid(jdcid if jdcid else url)
            r['url'] = url
            if 's' in c:
                subjs = c['s']

        if len(subjs) > 0:
            r["subs"] = [self._traverse(s, depth + 1) for s in subjs]
        elif jdcid:
            r['fetchable'] = True

        return r

    def _cacuCid(self, data):
        md5 = hashlib.md5()
        md5.update(data)
        return md5.hexdigest()

    def _getCatId(self, url):
        qs = urlparse.parse_qs(urlparse.urlsplit(url).query)
        return qs['cat'][0] if 'cat' in qs else None

    def _parseLink(self, l):
        r = ''
        if '.' in l: r = 'http://' + l
        else: r = 'http://list.jd.com/list.html?cat=' + l.replace('-', ',')
        return r

    def _parseZhuti(self, s):
        # 文本样例：jiadian.jd.com/|家电城||0
        sects = s.split("|")
        return {
            "name": sects[1],
            "url": sects[0]
        }

    def _parseBrand(self, s):
        # 文本样例："//haier.jd.com/|海尔|vclist/jfs/t3211/96/3882705424/5364/76e60d4a/57f9fa89N6ddb14fc.jpg|"
        sects = s.split("|")
        return {
            "name": sects[1],
            "url": sects[0],
            "logo": sects[2]
        }

    def _parseCategory(self, s):
        # 文本样例：channel.jd.com/home.html|家居||0
        sects = s.split("|")
        return {
            "name": sects[1],
            "url": sects[0]
        }

