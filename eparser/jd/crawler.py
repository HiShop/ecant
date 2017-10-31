#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import logging as LOG
import random
import json
import time
import urllib
import urllib2
from urlparse import urlparse
from scrapy.selector import Selector

class Crawler:
    def __init__(self):
        pass

    def start(self, url):
        goods = []
        link = url
        while True:
            gc, link = self.parsePage(link)
            goods += gc
            if link is None: break

        return goods

    def parsePage(self, url):
        LOG.debug('分析分类列表页 %s' % url)
        html = urllib2.urlopen(url, timeout=30).read()
        se = Selector(text=html)

        script = se.xpath('//script/text()')[0].extract()
        area = re.search(r'"area":"([,0-9]+)"', script).group(1).replace(',', '_')
        
        plist = se.xpath('//div[@id="plist"]')
        skus = plist.xpath('//div[contains(@class, "j-sku-item")]/@data-sku').extract()
        
        prices = self.collectPrices(area, skus)
        goodsEls = se.xpath('//li[@class="gl-item"]')
        goods = [self.parseGoods(e, prices) for i, e in enumerate(goodsEls)]

        #for i, g in enumerate(goods): print("%d: %s" % (i, g['image']))

        next = se.xpath('//a[@class="pn-next"]/@href').extract()
        if len(next) > 0:
            o = urlparse(url);
            link = '%s://%s%s' % (o.scheme, o.netloc, next[0])
            return goods, link
        else:
            return goods, None

    def collectPrices(self, area, skus):
        skuGroup = []
        prices = {}

        for i, sku in enumerate(skus):
            skuGroup.append(sku)
            if (i + 1) % 10 == 0 or i == (len(skus) - 1):
                prices.update(self.getPricesGroup(area, skuGroup))
                skuGroup = []

        return prices
            
    def getPricesGroup(self, area, skus):
        skuIds = 'J_' + '%2CJ_'.join(skus)
        url = 'http://p.3.cn/prices/mgets?type=1&area=%s&skuIds=%s&pduid=%d' % (
            area,
            skuIds,
            int(time.time())
        )

        r = {}
        prices = json.loads(urllib2.urlopen(url, timeout=30).read())
        for s in prices:
            r[s['id'][2:]] = {
                'p': float(s['p']),
                'm': float(s['m']),
                'op': float(s['op'])
            }
            
        return r

    def parseGoods(self, e, prices):
        sku = e.xpath('.//div[contains(@class, "j-sku-item")]/@data-sku').extract()[0]
        img = e.xpath('.//div[@class="p-img"]/a/img/@src')
        img = img if img else e.xpath('.//div[@class="p-img"]/a/img/@data-lazy-img')
        
        title = re.sub(r'[\n\'",]', '', ''.join(
            e.xpath('.//div[@class="p-name"]/a/em/text()').extract()
        )).strip()

        g = {
            'sku': sku,
            'title': title,
            'image': img[0].extract(),
            'page': e.xpath('.//div[@class="p-name"]/a/@href').extract()[0],
            'price': prices[sku]
        }
        return g;

