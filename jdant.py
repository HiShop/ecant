#!/usr/bin/env python
# -*- coding: utf-8 -*-

import signal
import time
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool
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
        len(goods),
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
        self.doCrawl(fetchList)
        #self.parallelCrawl2(fetchList)

    def crawl(self, c):
        return crawl(c)

    def doCrawl(self, tasks):
        return self.crawl(tasks[0])
        for c in tasks: self.crawl(c)
    
    def parallelCrawl3(self, tasks):
        pool = ThreadPool(processes=50)
        results2 = pool.map(crawl, tasks)
        pool.close()
        pool.join()

    def parallelCrawl2(self, tasks):
        futures = set()
        with ThreadPoolExecutor(max_workers=50) as executor:
#                for param, result in zip(tasks, executor.map(self.crawl, tasks)):
#                    print('%s test: %s' % (param['name'], result))
            for c in tasks:
                future = executor.submit(self.crawl, c)
                futures.add(future)
        
            try:
                for future in concurrent.futures.as_completed(futures):
                    err = future.exception()
                    if err is not None: raise err
            except KeyboardInterrupt:
                LOG.debug('任务强制中断！')
                executor._threads.clear()
                concurrent.futures.thread._threads_queues.clear()

    def parallelCrawl(self, tasks):
        pool = Pool(50, init_worker)
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
