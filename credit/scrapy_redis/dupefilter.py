#!/usr/bin/python
#-*-coding:utf-8-*-

import redis
import time

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from scrapy.utils.url import canonicalize_url

class RFPDupeFilter(BaseDupeFilter):
    """Redis-based request duplication filter"""

    def __init__(self, server, key):
        """Initialize duplication filter

        Parameters
        ----------
        server : Redis instance
        key : str
            Where to store fingerprints
        """
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', 'localhost')
        port = settings.get('REDIS_PORT', 6379)
        server = redis.Redis(host, port)
        # create one-time key. needed to support to use this
        # class as standalone dupefilter with scrapy's default scheduler
        # if scrapy passes spider on open() method this wouldn't be needed
        key = "dupefilter:%s" % int(time.time())
        return cls(server, key)
 
    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_reseen(self, response, request, spider):
        if 200 != response.status :
            fp = request_fingerprint(request)
            if self.server.sismember(self.key,fp):
                self.server.srem(self.key, fp)
                print "reseen [sts]%d [url]%s!" % (response.status, request.url)

    def request_seen(self, request):
        """
            use sismember judge whether fp is duplicate.
        """
        
        fp = request_fingerprint(request)
        if self.server.sismember(self.key,fp):
            return True
        self.server.sadd(self.key, fp)
        with open('sinxin_debug', 'a') as f:
            f.write("[url]%s [url2]%s [mode]%s\n" % (request.url, canonicalize_url(request.url), request.method))
        return False

    def close(self, reason):
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        """Clears fingerprints data"""
        with open('sinxin_debug', 'w') as f:
            f.write("")
        self.server.delete(self.key)

    def __len__(self):
        """Return the length of the duperfilter"""
        return self.server.scard(self.key)