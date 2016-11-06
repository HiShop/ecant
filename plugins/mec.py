#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import urllib
import urllib2
import cookielib
import logging

_APPBASE = 'http://2.4.ysctest.kuaidiantong.cn'
_COOKIES = cookielib.CookieJar()
_OPENER = None

def defaultHeaders():
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36'
    headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
    headers['Connection'] = 'keep-alive'
    headers['Cache-Control'] = 'no-cache'
    headers['Pragma'] = 'no-cache'
    return headers

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code
        return result
    
    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)
        result.status = code
        loc = headers['Location']

        if loc.find('index.htm') >= 0:
            _HOME_INDEX = loc
        return result

def name():
    return 'HiShop 云商城数据导入插件'

def version():
    return '1.0.0'

def onLoad(ant):
    _OPENER = urllib2.build_opener(
        urllib2.HTTPCookieProcessor(_COOKIES),
        SmartRedirectHandler()
    )

    doAdminLogin(_OPENER)

def onCatagoryLoaded(ant, catagories):
    logging.debug('共发现 %d 个顶级分类！' % len(catagories))
    for c in catagories:
        logging.debug('-> %s' % c['name'])

def doAdminLogin(opener):
    url = _APPBASE + '/Admin/Login'
    html = opener.open(url).read()
    rexp = r' type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="(.+)"'

    r = re.search(rexp, html)

    viewState = r.group(1)

    headers = defaultHeaders()
    headers['Content-Type'] = 'application/x-www-form-urlencoded'

    data = {
        '__LASTFOCUS': '',
        '__VIEWSTATE': viewState,
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'txtAdminName': 'admin',
        'txtAdminPassWord': 'admin888',
        'btnAdminLogin': '登   录',
        'ErrorTimes': 0
    };

    request = urllib2.Request(url = url, data = urllib.urlencode(data), headers = headers)
    html = opener.open(request).read()
    for ck in _COOKIES:
        if ck.name == '.Hidistro':
            return True

    logging.error('登录云商城后台失败！');
    return False
