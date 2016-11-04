#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

def name():
    return 'HiShop 云商城数据导入插件'

def version():
    return '1.0.0'

def onLoad(ant):
    pass

def onCatagoryLoaded(ant, catagories):
    logging.debug('共发现 %d 个顶级分类！' % len(catagories))
    for c in catagories:
        logging.debug('-> %s' % c['name'])
