#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import random
import urllib
import urllib2
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup

class Crawler:
    def __init__(self):
        pass

    def start(self, url):
        return self.parsePage(url)

    def parsePage(self, url):
        request = urllib2.Request(url)
        html = urllib2.urlopen(request).read()

        soup = BeautifulSoup(html)
        goods = [
            self.parseGoods(gl) for gl in soup.findAll("li", { "class" : "gl-item" })
        ]

        for g in goods: print(g['title'])

        next = soup.find("a", { "class" : "pn-next" })
        if next:
            o = urlparse(url);
            link = '%s://%s%s' % (o.scheme, o.netloc, next['href'])
            return len(goods) + self.parsePage(link)
        else:
            return len(goods)

    def parseGoods(self, tag):
        g = {
            'title': tag.find("div", { "class" : "p-name" }).find("em").text
        }
        return g;

