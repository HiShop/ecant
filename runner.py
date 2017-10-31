#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
from jdant import JDAnt 

def runJDAnt():
    ant = JDAnt()
    ant.run()

if __name__ == '__main__':
    if os.path.isfile('log.txt'):
        os.remove('log.txt')
        
    logging.basicConfig(filename = 'ecant.log', level = logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())

    reload(sys)
    sys.setdefaultencoding("utf8")
    
    runJDAnt()
