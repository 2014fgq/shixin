import datetime
import traceback
from liepin.utils import color
from scrapy import log
from pymongo import MongoClient
class SingleMongodbPipeline(object):
    """
        save the data to mongodb.
    """

    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DB = "zhaopin"

    def __init__(self):
        """
            The only async framework that PyMongo fully supports is Gevent.
            
            Currently there is no great way to use PyMongo in conjunction with Tornado or Twisted. PyMongo provides built-in connection pooling, so some of the benefits of those frameworks can be achieved just by writing multi-threaded code that shares a MongoClient.
        """
        
        self.style = color.color_style()
        try:
            client = MongoClient(self.MONGODB_SERVER,self.MONGODB_PORT) 
            self.db = client[self.MONGODB_DB]
        except Exception as e:
            print self.style.ERROR("ERROR(SingleMongodbPipeline): %s"%(str(e),))
            traceback.print_exc()

    @classmethod
    def from_crawler(cls, crawler):
        cls.MONGODB_SERVER = crawler.settings.get('SingleMONGODB_SERVER', 'localhost')
        cls.MONGODB_PORT = crawler.settings.getint('SingleMONGODB_PORT', 27017)
        cls.MONGODB_DB = crawler.settings.get('SingleMONGODB_DB', 'books_fs')
        pipe = cls()
        pipe.crawler = crawler
        return pipe

    def process_item(self, item, spider):
        zhaopin_detail = {
            'jobs':item.get('jobs',''),
            'salary':item.get('salary',''),
            'company':item.get('company',''),
            'city':item.get('city',''),
            'detailLink':item.get('detailLink', ''),
            #'book_file':item.get('book_file',''),
            #'original_url':item.get('original_url',''),
            'time':item.get('time',''),
            'update_time':datetime.datetime.utcnow(),
        }
        
        result = self.db['liepin'].update({'url':zhaopin_detail['detailLink']}, zhaopin_detail, True)
        item["mongodb_id"] = str(result)

        log.msg("Item %s wrote to MongoDB database %s/book_detail" %
                    (result, self.MONGODB_DB),
                    level=log.DEBUG, spider=spider)
        return item