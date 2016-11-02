#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from jdant import JDAnt 

def runJDAnt():
    ant = JDAnt()
    ant.run()

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding("utf8")
    
    runJDAnt()
