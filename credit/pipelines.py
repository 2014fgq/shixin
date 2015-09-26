#-*- coding:utf8 -*-

import os
from credit.items import *
import json
import codecs

os.chdir("./")

class CreditPipeline(object):
    def process_item(self, item, spider):
        """
        doc
        """
        if isinstance(item, IdItem):
            spider.file_handler.write(item['content'])
        else:
            # writeIn = str(item["cid"])+"\001"+item["name"]+"\001"+str(item["caseCode"])+"\001"+str(item["age"])+"\001"+item["sex"]+"\001"+str(item["cardNum"])+"\001"+item["courtName"]+"\001"+item["areaName"]+"\001"+item["partyTypeName"]+"\001"+str(item["gistId"])+"\001"+str(item["regDate"])+"\001"+item["gistUnit"]+"\001"+item["duty"]+"\001"+item["performance"]+"\001"+item["disruptTypeName"]+"\001"+item["publishDate"]  #writeIn for personMore
            writeIn = str(item["cid"])+"\001"+item["name"]+"\001"+str(item["caseCode"])+"\001"+item["businessEntity"]+"\001"+str(item["cardNum"])+"\001"+item["courtName"]+"\001"+item["areaName"]+"\001"+str(item["gistId"])+"\001"+str(item["regDate"])+"\001"+item["gistUnit"]+"\001"+item["duty"]+"\001"+item["performance"]+"\001"+item["disruptTypeName"]+"\001"+item["publishDate"]   #writeIn for unitMore
            f = open(spider.writeInFile, "a")
            #f.write("\001".join([str(i) for i in item.values()]) + '\n')
            f.write(writeIn+"\n")
            f.close()

class JsonWithEncodingPipeline(object):
    def __init__(self):
        pass
        #self.file = codecs.open('shixin.txt', 'w')

    def process_item(self, item, spider):
        self.file = codecs.open('shixin.txt', 'a')
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        #self.file.write(",".join([unicode(str(i),'gbk')  for i in item.values()]) + '\n')
        self.file.write(line)
        self.file.close()
        return item

    def spider_closed(self, spider):
        pass
        #self.file.close()