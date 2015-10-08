"""
Scrapy Telnet Console extension

See documentation in docs/topics/telnetconsole.rst
"""
import logging    
logger = logging.getLogger(__name__)
from scrapy.telnet import TelnetConsole
update_telnet_vars = object()
class UTelnet(TelnetConsole):
    def set_level(self, level):
        try:
            logging.root.setLevel(level)
            try:
                level = logging._checkLevel(level)
            except Exception:
                level = 0
            for key,value in logger.manager.loggerDict.items():
                try:
                    value.level = level
                except Exception as e:
                    logger.error("key%(key)s, Error %(Error)s",  {'key':key, 'Error':e})
                    pass
                
            logger.info("Change Log Level to %(level)s", {'level':logging.getLevelName(level)})
        except Exception as e:
            logger.error("Change Log Level Error [reason]%(exception)s", {'exception':e})
            
    def _get_telnet_vars(self):
        telnet_vars = TelnetConsole._get_telnet_vars(self)  
        utelnet_vars = {
            'setlevel':self.set_level,
            'shixin':self.crawler.extensions.middlewares[2],
            'scheduler':self.crawler.engine.slot.scheduler,
            'downloader':self.crawler.engine.downloader
        }
        utelnet_vars = dict(telnet_vars.items() + utelnet_vars.items())
        self.crawler.signals.send_catch_log(update_telnet_vars, telnet_vars=utelnet_vars)
        return utelnet_vars

    def get_level(self, level):
        print logger.getLevelName(level)