# !/usr/bin/env python
# -*-encoding: utf-8-*-
# author:LiYanwei
# version:0.1

import sys
import os
from scrapy.cmdline import execute
# sys.path —— 动态地改变Python搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "zhihuInterlocution"])
# execute(["scrapy", "crawl", "zhihuUser"])