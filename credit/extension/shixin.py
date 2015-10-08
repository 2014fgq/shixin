import datetime

from scrapy import signals
import pymongo
from scrapy.http import Request, FormRequest
import logging
from scrapy.item import Item
logger = logging.getLogger(__name__)
from timeit import timeit as timeit  
import time
class shixin_extension(object):

    def __init__(self, crawler):
        self.crawler = crawler
        
        pass
    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(o.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(o.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(o.response_received, signal=signals.response_received)
        crawler.signals.connect(o.spider_idle, signal=signals.spider_idle)
        #crawler.signals.connect(o.update_telnet_vars, signal=signals.update_telnet_vars)
        return o

    #def update_telnet_vars(self):
    #    pass

    def add_requests(self, urls):
        try:
            for url in urls:
                yield self.crawler.spider.check_result_before_close(url)
        except Exception as e:
            logger.error("add_requests Error %(error)s",  {'error':e})
    def reclac_filter_url(self, spider):
        time1= time.time()
        self.scheduler.df.clear()        
        urls = []
        for item in spider.collection.find().sort("detailLink",pymongo.ASCENDING):
            try:
                urls.append(str(item['detailLink']))
            except:
                cid = str(item['cid'])
                logger.error("check filer cid [%(cid)s] url [%(url)s] reason [%(Error)s]", {'cid':cid, 'url':url, 'Error':e})
        print time.time() - time1
        time1= time.time()
        while '' in urls:
            urls.remove('')
        add_requests = self.add_requests(urls)
        print time.time() - time1

        time1= time.time()
        while True:
            try:
                request = add_requests.next()
                self.scheduler.df.request_seen(request)
            except StopIteration as e:
                break
            except Exception as e:
                logger.error("Exception %(error)s", {'error':e})
        print time.time() - time1 
        logger.info("Reclac the Filter Url use time %(time)ds", {'time':(time.time()-time1)})
        #logger.info("Reclac the Filter Url use time %(time)d" % (time.time()-time1))
    def test1(self):
        time1= time.time()
        self.reclac_filter_url(self.crawler.spider)
        time2= time.time()
        print time2 - time1    
    def test2(self):
        time1= time.time()
        self.scheduler.df.clear();  
        time2= time.time()
        print time2 - time1
    def reclac_filter_url1(self, spider):
        self.scheduler.df.clear();
        for item in spider.collection.find().sort("detailLink",pymongo.ASCENDING):
            try:
                url = str(item['detailLink'])
                self.scheduler.df.request_seen(spider.check_result_before_close(url))
            except Exception as e:
                cid = str(item['cid'])
                logger.error("check filer cid [%(cid)s] url [%(url)s] reason [%(Error)s]", {'cid':cid, 'url':url, 'Error':e})
        logger.info("Reclac the Filter Url!")
        
    def spider_opened(self, spider):
        self.scheduler = self.crawler.engine.slot.scheduler
        self.reclac_filter_url(spider)
        pass
    def spider_closed(self, spider, reason):
        pass
    def spider_idle(self, spider):
        self.reclac_filter_url(spider)
        '''
        # for test
        spider.total = 20000 
        url = 'http://shixin.court.gov.cn/personMore.do'
        '''
        if (True != spider.dont_repush):
            spider.startIdx = spider.startIdx + spider.step
            spider.endIdx = spider.startIdx + spider.step
            if (0 != spider.total) and (spider.startIdx < spider.total+1):
                if spider.endIdx > spider.total+1:
                    spider.endIdx = spider.total+1
                for i in range(1,spider.total+1)[spider.startIdx:spider.endIdx]:
                    request = FormRequest(spider.start_urls[0],
                        formdata={'currentPage': str(i)},
                        callback=spider.listpare,dont_filter=True, meta={'pageNum':str(i)})
                    self.scheduler.queue.push(request)
                if spider.endIdx == spider.total+1:
                    spider.startIdx = spider.endIdx
                self.crawler.engine.slot.nextcall.schedule()
                logger.info("Repush the Crawl Url [%(startIdx)d] to [%(endIdx)d]!",
                            {'startIdx':spider.startIdx, 'endIdx':spider.endIdx})
        pass
    def item_scraped(self, item, spider):
        pass
    def response_received(self, spider):
        pass
    def item_dropped(self, item, spider, exception):
        pass
    
    def all_members(self, aClass):
        try:
            #new type class
            mro = list(aClass.__mro__)
        except AttributeError:
            #old type class
            def getmro(aClass,recurse):
    #            print 'getmro:',aClass.__name__
                mro = [aClass]
                for base in aClass.__bases__:
                    mro.extend(recurse(base,recurse))
                return mro
            def getmro1(aClass):
                mro = [aClass]
                for base in aClass.__bases__:
                    mro.extend(getmro1(base))
                return mro
            mro = getmro(aClass,getmro)
    #        mro = getmro1(aClass)
        mro.reverse()
        print aClass.__name__," mro:",mro
        members = {}
        for someClass in mro:
            members.update(vars(someClass))
        return members