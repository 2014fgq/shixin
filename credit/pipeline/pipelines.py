#-*- coding:utf8 -*-

import os
from credit.items import *
import json
import codecs

os.chdir("./")
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class JsonWithEncodingPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        self.file = codecs.open(spider.writeInFile, 'a')
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        self.file.close()
        return item

    def spider_closed(self, spider):
        pass
