#-*- coding:utf-8 -*-
"""
从法院官网爬被执行人公布的名单
"""
from scrapy.spider import Spider
from scrapy.http import Request,FormRequest
from scrapy import signals
from scrapy import log
import re
from credit.items import *
import base64
import json
from scrapy.utils.response import get_base_url
import logging
logger = logging.getLogger(__name__)
class PersonageCredit(Spider):
    download_delay=0
    download_timeout=30
    name = 'credit'
    handle_httpstatus_all = True
    writeInFile = "personMore"
    start_urls = ['http://shixin.court.gov.cn/personMore.do']
    allowed_domains=['shixin.court.gov.cn']
    startIdx = 545
    step = 1
    total = 0
    dont_repush = False
    def __init__(self):
        self.queue = None
        self.df = None
        self.collection = None
        pass
    
    def make_requests_from_url(self,url):
        return Request(url, callback=self.gettotal,dont_filter=True)
    
    def set_level(self, level):
        try:
            logging.root.setLevel(level)
            #self.log(logger.level,logging.root.level,logger.root.level,)
           
            for key,value in logger.manager.loggerDict.items():
                try:
                    level = logging._checkLevel(level)
                    value.level = level
                except Exception as e:
                    print key, "Error %s" % e
                    pass
        except Exception as e:
            logger.error("%(exception)s", {'exception':e})
    def get_level(self, level):
        print logger.getLevelName(level)
    def check_result_before_close(self, url):
        return Request(url, callback=self.detail,meta={'url':url})
        pass
    def gettotal(self,response):
        hxs = response.selector
        try:
            total = hxs.xpath(u"//a[contains(text(),'尾页')]/@onclick").extract()[0]
            total = int(re.findall("\d+",total)[0])
            self.total = total
            endIdx = self.startIdx + self.step
            for i in range(1,total+1)[self.startIdx:endIdx]:
                yield FormRequest(response.url,
                        formdata={'currentPage': str(i)},
                        #headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
                        callback=self.listpare,dont_filter=True, meta={'pageNum':str(i)})
        except Exception, e:
            log.msg("total error_info=%s, url=%s" %(e, response.url),level=log.ERROR)
    def listpare(self, response):
        if response.status == 200:
            hxs = response.selector
            datalist =  hxs.xpath("//table[@id='Resultlist']/tbody/tr[position()>1]")
            base_url = get_base_url(response)
            item = PersonMore()
            if len(datalist) == 0:
                log.msg("datalist_empty error_info=%s, url=%s,pageNum=%s" %(e, response.url,meta['pageNum']),level=log.ERROR)
            try:
                for da in datalist:
        #            name = da.select('td[2]/a/text()').extract()[0]
        #            causeserial = da.select('td[3]/text()').extract()[0]
        #            causedate = da.select('td[4]/text()').extract()[0]
                    id = da.xpath('./td[6]/a/@id').extract()[0]
                    url ="http://shixin.court.gov.cn/detail?id=%s" % id
                    yield Request(url,callback=self.detail,meta={'url':url})
                    
                    item["detailLink"] = url
                    #yield item
            except Exception,e:
                log.msg("datalist error_info=%s, url=%s,pageNum=%s" %(e, response.url,meta['pageNum']),level=log.ERROR)
        else:
            log.msg("undowndloaded page=%s" %meta["pageNum"],level=log.ERROR) #当请求不成立的状况下记录下页数
    
    def for_ominated_data(self,in_dict, tag_str,response):
        """
        for some data are ominated
        """
        try:
            re_data = base64.b64encode(str(in_dict[tag_str]))  #base64要求转换的是字符串
        except Exception,e:
            re_data = ""    #原数据中没有该项
            log.msg("for_ominated_data error_info=%s, key=%s,url=%s" %(e,tag_str,response.url))  #记录下出现空值的项以备验查
        return re_data

    def detail(self,response):
        if response.status == 200:
            jsonresponse = json.loads(response.body_as_unicode())
            base_url = get_base_url(response)
            item = PersonMore()
            try:
                item["cid"] = jsonresponse["id"]
                item["name"] = jsonresponse["iname"]
                item["caseCode"] = jsonresponse["caseCode"]
                item["age"] = jsonresponse["age"]
                item["sex"] = jsonresponse["sexy"]
                #item['focusNumber'] = jsonresponse['focusNumber']
                item["cardNum"] = jsonresponse["cardNum"]
                item["courtName"] = jsonresponse["courtName"]
                item["areaName"] = jsonresponse["areaName"]
                item["partyTypeName"] = jsonresponse["partyTypeName"]
                item["gistId"] = jsonresponse["gistId"]
                item["regDate"] = jsonresponse["regDate"]
                item["gistUnit"] = jsonresponse["gistUnit"]
                item["duty"] = jsonresponse["duty"]
                item["performance"] = jsonresponse["performance"]
                #if "performedPart" in json.loads(response.body):
                #    item["performedPart"] = jsonresponse["performedPart"]
                #    item["unperformPart"] = jsonresponse["unperformPart"]
                #else:
                #    item["performedPart"] = "NA"
                #    item["unperformPart"] = "NA"
                item["disruptTypeName"] = jsonresponse["disruptTypeName"]
                item["publishDate"] = jsonresponse["publishDate"]
                item["detailLink"] = base_url
            except Exception,e:
                log.msg("item error_info=%s url=%s item_key=%s" %(e, response.url,"\001".join(str(i) for i in [item.values()])), level=log.ERROR)
            yield item       
        else:
            log.msg("undownloaded info url=%s"%meta["url"],level=log.ERROR)   #如果请求不成功（状态码不为200）记录下来
