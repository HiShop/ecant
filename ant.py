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
	for filename in os.listdir("plugins"):
	    if not filename.endswith(".py") or filename.startswith("__"):
		continue
	   
            moduleName = os.path.splitext(filename)[0]
            self.plugins[moduleName] = self.loadPlugin(moduleName) 

    def loadPlugin(self, moduleName):
	m = __import__("plugins." + moduleName, fromlist=[moduleName])
        m.onLoad(self)
        logging.debug('加载插件：%s（v%s）[plugins/%s.py]' % (
            m.name(),
            m.version(),
            moduleName
        ))
        return m

    def notifyCatagoryLoaded(self, catagories):
        for k in self.plugins:
            self.plugins[k].onCatagoryLoaded(self, catagories)
