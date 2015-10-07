#-*- coding:utf8 -*-
#IMAGES_EXPIRES = 1000
BOT_NAME = 'credit'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['credit.spiders']
NEWSPIDER_MODULE = 'credit.spiders'

USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

#LOG_FILE = './log_unit_increment'
LOG_LEVEL = 'DEBUG'
REDIRECT_ENABLED = False
RETRY_ENABLED = True
RETRY_TIMES = 200  # initial response + 2 retries = 3 requests
RETRY_HTTP_CODES = [302, 500, 502, 503, 504, 400, 408]
DNSCACHE_ENABLED = True
COOKIES_ENABLED = False

CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 500
CONCURRENT_REQUESTS_PER_DOMAIN = 400
CONCURRENT_REQUESTS_PER_IP = 0

#DOWNLOAD_TIMEOUT = 30      # 0.5mins

SPIDER_MIDDLEWARES = {
    #状态码非200的响应
    #'credit.middlewares.Not200Middleware': 48,
    #处理常见的连接超时等错误
    #'credit.middlewares.RecordWrongPageMiddleware': 930
}

DOWNLOADER_MIDDLEWARES = {
    # handle downloadtimeout error
    'credit.middlewares.DownloadTimeoutRetryMiddleware': 375,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'credit.contrib.downloadmiddleware.rotate_useragent.RotateUserAgentMiddleware':400,
    'credit.contrib.downloadmiddleware.scrapy_crawlera.CrawleraMiddleware': None
}

ITEM_PIPELINES = {
    'credit.pipeline.pipelines.JsonWithEncodingPipeline': 375,
    'credit.pipeline.scrapy_mongodb.MongoDBPipeline':300,
}

EXTENSIONS = {
    'credit.extension.UShell_server.UShellConsole': 0,
    'scrapy.telnet.TelnetConsole': None,
    'credit.extension.shixin.shixin_extension': 0,
    'credit.extension.telnet.UTelnet': 0,
}

MONGODB_URI = 'mongodb://192.168.1.200:27017'
MONGODB_DATABASE = 'credit'
MONGODB_COLLECTION = 'credit'
MONGODB_UNIQUE_KEY = 'detailLink'
#MONGODB_BUFFER_DATA = 512

SCHEDULER = "credit.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'credit.scrapy_redis.queue.SpiderPriorityQueue'

REDIS_HOST = '192.168.1.200'
REDIS_PORT = 6379

TELNETCONSOLE_HOST = '0.0.0.0'

USHELLCONSOLE_ENABLED = True
USHELLCONSOLE_PORT = [31500, 31600]
USHELLCONSOLE_HOST = '0.0.0.0'

CRAWLERA_ENABLED = False
CRAWLERA_USER = ''
CRAWLERA_PASS = ''