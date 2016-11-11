#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eparser.jd.category import Category
from eparser.jd.crawler import Crawler
from ant import Ant

class JDAnt(Ant):
    def __init__(self):
        super(JDAnt, self).__init__()

    def run(self):
        cat = Category()
        categories = cat.getTree()
        self.notifyCategoryLoaded(categories);

        for c in categories: self.printTopCategory(c)

    def printTopCategory(self, c):
        names = ', '.join([t['name'] for t in c['zhuti']])
        print('共 %d 个主题馆：%s' % (len(c['zhuti']), names))

        brands = ', '.join([t['name'] for t in c['brands']])
        print('共 %d 个品牌：%s' % (len(c['brands']), brands))

        #self.crawl(c, 0)
        self.printAvlTree(c, 0)

        print('')

    def printTree(self, c, depth):
        print '    ' * depth + c['name'] + ' ' + c['url']
        if 'subs' in c and len(c['subs']) > 0:
            for s in c['subs']: self.printTree(s, depth + 1)

    def printAvlTree(self, c, depth):
        if 'subs' in c and len(c['subs']) > 0:
            print '    ' * depth + c['name']
            for s in c['subs']: self.printAvlTree(s, depth + 1)
        else:
            if 'http://list.jd.com/list.html?cat=' in c['url']:
                print '    ' * depth + c['name'] + ' ' + c['url']

    def crawl(self, c, depth):
        if 'subs' in c and len(c['subs']) > 0:
            print '    ' * depth + c['name']
            for s in c['subs']: self.crawl(s, depth + 1)
        else:
            if 'http://list.jd.com/list.html?cat=' in c['url']:
                crawler = Crawler();
                goods = crawler.start(c['url'])
                print('%s [%d] %s %s' % (
                    '    ' * depth,
                    goods,
                    c['name'],
                    c['url'])
                )
