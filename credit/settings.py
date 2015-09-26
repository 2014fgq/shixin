#-*- coding:utf8 -*-
#IMAGES_EXPIRES = 1000
BOT_NAME = 'credit'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['credit.spiders']
NEWSPIDER_MODULE = 'credit.spiders'
DEFAULT_ITEM_CLASS = 'credit.items.CreditItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

#LOG_FILE = './log_unit_increment'
LOG_LEVEL = 'DEBUG'
REDIRECT_ENABLED = False
RETRY_ENABLED = True
RETRY_TIMES = 200  # initial response + 2 retries = 3 requests
RETRY_HTTP_CODES = [302, 500, 502, 503, 504, 400, 408]
SPIDER_MIDDLEWARES = {
    #状态码非200的响应
    'credit.middlewares.Not200Middleware': 48,
    #处理常见的连接超时等错误
    'credit.middlewares.RecordWrongPageMiddleware': 930
}

DOWNLOADER_MIDDLEWARES = {
    # handle downloadtimeout error
    'credit.middlewares.DownloadTimeoutRetryMiddleware': 375,
}

ITEM_PIPELINES = {
    'credit.pipelines.JsonWithEncodingPipeline': 375,
}
