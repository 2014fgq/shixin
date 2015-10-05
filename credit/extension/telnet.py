"""
Scrapy Telnet Console extension

See documentation in docs/topics/telnetconsole.rst
"""


import pprint
from scrapy.utils.trackref import print_live_refs
from scrapy.utils.engine import print_engine_status
try:
    import guppy
    hpy = guppy.hpy()
except ImportError:
    hpy = None
import logging    
logger = logging.getLogger(__name__)
from scrapy.telnet import TelnetConsole
update_telnet_vars = object()
class UTelnet(TelnetConsole):

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
            logger.info("Change Log Level to %(level)s", {'level':level})
        except Exception as e:
            logger.error("%(exception)s", {'exception':e})
            
    def _get_telnet_vars(self):
        # Note: if you add entries here also update topics/telnetconsole.rst
        telnet_vars = {
            'engine': self.crawler.engine,
            'spider': self.crawler.engine.spider,
            'slot': self.crawler.engine.slot,
            'crawler': self.crawler,
            'extensions': self.crawler.extensions,
            'stats': self.crawler.stats,
            'settings': self.crawler.settings,
            'est': lambda: print_engine_status(self.crawler.engine),
            'p': pprint.pprint,
            'prefs': print_live_refs,
            'hpy': hpy,
            'setlevel':self.set_level,
            'help': "This is Scrapy telnet console. For more info see: " \
                "http://doc.scrapy.org/en/latest/topics/telnetconsole.html",
        }
        self.crawler.signals.send_catch_log(update_telnet_vars, telnet_vars=telnet_vars)
        return telnet_vars

    def get_level(self, level):
        print logger.getLevelName(level)