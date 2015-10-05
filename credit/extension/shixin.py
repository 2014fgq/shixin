import datetime

from scrapy import signals
import pymongo
from scrapy.http import Request, FormRequest
import logging
logger = logging.getLogger(__name__)
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
        return o

    def spider_opened(self, spider):
        pass
    def spider_closed(self, spider, reason):
        pass
    def spider_idle(self, spider):
        logger.info("Reclac the Filter Url!")
        spider.df.clear();
        for item in spider.collection.find().sort("detailLink",pymongo.ASCENDING):
            try:
                url = str(item['detailLink'])
                spider.df.request_seen(spider.check_result_before_close(url))
            except Exception as e:
                cid = str(item['cid'])
                logger.error("check filer cid [%(cid)s] url [%(url)s] reason [%(Error)s]", {'cid':cid, 'url':url, 'Error':e})

        spider.startIdx = spider.startIdx + spider.step
        spider.endIdx = spider.startIdx + spider.step
        '''
        # for test
        spider.total = 20000 
        url = 'http://shixin.court.gov.cn/personMore.do'
        '''
        if (True != spider.dont_repush) and (0 != spider.total) and (spider.startIdx < spider.total+1):
            if spider.endIdx > spider.total+1:
                spider.endIdx = spider.total+1
            for i in range(1,spider.total+1)[spider.startIdx:spider.endIdx]:
                request = FormRequest(spider.start_urls[0],
                    formdata={'currentPage': str(i)},
                    callback=spider.listpare,dont_filter=True, meta={'pageNum':str(i)})
                spider.queue.push(request)
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
    
    def all_members(aClass):
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