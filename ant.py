#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

class Ant(object):
    def __init__(self):
        self.plugins = {}

        logging.debug('开始加载本地插件...');
        self.loadLocalPlugins()

    def loadLocalPlugins(self):
        ignores = []
        for line in open('./plugins/.ignore'):
            ignores.append(line.replace('\n', '').replace('\r', ''))

	for filename in os.listdir("plugins"):
	    if not filename.endswith(".py") or filename.startswith("__"):
		continue
	  
	    if filename in ignores:
		continue

            moduleName = os.path.splitext(filename)[0]
            self.plugins[moduleName] = self.loadPlugin(moduleName) 

    def loadPlugin(self, moduleName):
	m = __import__("plugins." + moduleName, fromlist=[moduleName])
        logging.debug('加载插件：%s（v%s）[plugins/%s.py]' % (
            m.name(),
            m.version(),
            moduleName
        ))
        m.onLoad(self)
        return m

    def notifyCategoryLoaded(self, categories):
        for k in self.plugins:
            self.plugins[k].onCategoryLoaded(self, categories)

    def notifyGoodsCollected(self, category, goods):
        for k in self.plugins:
            self.plugins[k].onGoodsCollected(self, category, goods)
