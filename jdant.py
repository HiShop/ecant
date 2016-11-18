#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
import logging as LOG
from eparser.jd.category import Category
from eparser.jd.crawler import Crawler
from ant import Ant

def crawl(c):
    LOG.debug('开始爬取 %s [%s] ...' % (
        c['name'],
        c['cid']
    ))

    crawler = Crawler();
    goods = crawler.start(c['url'])
    LOG.debug('[%d] %s %s' % (
        goods,
        c['name'],
        c['url'])
    )

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

class JDAnt(Ant):
    def __init__(self):
        super(JDAnt, self).__init__()

    def run(self):
        cat = Category()
        categories = cat.getTree()
        self.notifyCategoryLoaded(categories);

        fetchList = []
        for c in categories: self.traverseToList(c, 0, fetchList)
        #self.doCrawl(fetchList)
        self.parallelCrawl2(fetchList)

    def crawl(self, c):
        LOG.debug('开始爬取 %s [%s] ...' % (
            c['name'],
            c['cid']
        ))

        crawler = Crawler();
        goods = crawler.start(c['url'])
        LOG.debug('[%d] %s %s' % (
            goods,
            c['name'],
            c['url'])
        )


    def doCrawl(self, tasks):
        for c in tasks: self.crawl(c)

    def parallelCrawl2(self, tasks):
        with ThreadPoolExecutor(max_workers=10) as executor:
            try:
                for param, result in zip(tasks, executor.map(self.crawl, tasks)):
                    print('%s test: %s' % (param['name'], result))
            except KeyboardInterrupt:
                LOG.debug('任务强制中断！')
                executor.shutdown(wait=False)

    def parallelCrawl(self, tasks):
        pool = Pool(20, init_worker)
        try:
            results = []
            LOG.debug('开始并行处理')
            for c in tasks:
                results.append(pool.apply_async(crawl, args=(c,)))

            LOG.debug('任务已经启动，按Ctrl + C中止！')
            time.sleep(60*60*24)

            pool.close()
            pool.join()
        except KeyboardInterrupt:
            LOG.debug('任务强制中断！')
            pool.terminate()
            pool.join()

    def traverseToList(self, c, depth, list):
        if c['fetchable']: list.append(c)
        if 'subs' in c and len(c['subs']) > 0:
            for s in c['subs']: self.traverseToList(s, depth + 1, list)
