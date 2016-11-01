#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from jdant import JDAnt

#def fetchJDBooks(listUrl):
#    req = urllib2.Request(listUrl)
#    res = urllib2.urlopen(req).read()
#
#    soup = BeautifulSoup(res)
#    books = [
#        str(tag.a.em).replace('<em>', '').replace('</em>', '').strip() for tag in soup.findAll("div", { "class" : "p-name" })
#    ]
#
#    return books, soup.find("a", { "class" : "pn-next" })
#
#def createSKU(sku, productId, productName, color, size, version, price, stock):
#    url = 'http://localhost:16666/1/sku'
#    data = {
#        'sku': sku,
#        'shop_id': 160,
#        'shop_name': '测试专场店',
#        'product_id': productId,
#        'product_name': productName,
#        'color': color,
#        'size': size,
#        'version': version,
#        'price': price,
#        'stock': stock
#    }
#
#    request = urllib2.Request(
#        url = url,
#        data = urllib.urlencode(data)
#    )
#    
#    res = urllib2.urlopen(request).read()
#    return res
#
#JD = 'http://list.jd.com'
#url = JD + '/list.html?cat=1315%2C1343%2C9719&go=0'
#
#colors = ['红', '橙', '黄', '绿', '青', '蓝', '紫']
#size = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
#version = ['青葱', '复古', '潮流', '清新']
#
#count = 0
#skus = 0
#while skus < 1000000:
#    books, link = fetchJDBooks(url)
#
#    for b in books:
#        if b != '' and b != 'None':
#            b = b[0: b.rfind(' ')]
#            b = b[0: b.rfind(' ')]
#            count += 1
#            print '%04d - [%s]' % (count, b)
#
#            for i in range(random.randint(1, 5)):
#                skus += 1
#                sku = 'SKU' + ('%08d' % (skus + 1))
#                createSKU(
#                    sku, 'P%04d' % count, b,
#                    colors[random.randint(0, len(colors) - 1)],
#                    size[random.randint(0, len(size) - 1)],
#                    version[random.randint(0, len(version) - 1)],
#                    12.5, 1000000
#                )
#            
#
#    url = JD + link['href']

def runAnt(ant, repo):
    ant.run(repo)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf8")
    
    runAnt(JDAnt(), './data/jd')
