#coding:utf-8
'''
Created on 2015-8-18

@author: Haier
'''

import pprint
import logging

from scrapy.exceptions import NotConfigured
from scrapy import signals
from scrapy.utils.trackref import print_live_refs
from scrapy.utils.engine import print_engine_status
import threading
import socket, traceback
import subprocess
import UShell_json
import sys
try:
    import guppy
    hpy = guppy.hpy()
except ImportError:
    hpy = None
    
logger = logging.getLogger(__name__)

def est(args):
    print_engine_status(ushell.crawler.engine)

def set_level(self, level):
    try:
        logging.root.setLevel(level)
        for key,value in logger.manager.loggerDict.items():
            try:
                level = logging._checkLevel(level)
                value.level = level
            except Exception as e:
                print key, "Error %s" % e
                pass
    except Exception as e:
        logger.error("%(exception)s", {'exception':e})

class UShellConsole(threading.Thread):
    def __init__(self, crawler):
        threading.Thread.__init__(self)
        self.sock = None
        self.crawler = crawler
        self.parser = UShell_json.json_factory().create_json_parser('pshell_json')
        self.portrange = [int(x) for x in crawler.settings.getlist('USHELLCONSOLE_PORT')]
        self.host = crawler.settings['USHELLCONSOLE_HOST']
        
    def start_listening(self):
        self.port = self.bind(self.host, self.portrange)
        self.setDaemon(True)
        self.start()
        logger.info("UShell console listening on %(host)s:%(port)d",
                     {'host': self.host, 'port': self.port},
                     extra={'crawler': self.crawler})

    def bind(self, host, portrange):
        if len(portrange) == 1:
            return self.do_bind(host, str(portrange[0]))
        for x in range(portrange[0], portrange[1]+1):
            try:
                return self.do_bind(host, str(x))
            except error.CannotListenError:
                if x == portrange[1]:
                    raise

    def do_bind(self, ip='127.0.0.1', port = '31501'):
        try:
            IP = ip
            Port = int(port)
            self.address = (IP,Port)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(self.address)
            return Port
            #logger.info('Bind %(IP)s:%(Port)d', {'IP':IP, 'Port':Port})
        except Exception,e:
            #logger.error('Bind Fail %(Exception)s', {'Exception':e})
            raise

    def stop_listening(self):
        pass
        #self.stop()
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('USHELLCONSOLE_ENABLED'):
            raise NotConfigured

        obj = cls(crawler)
        crawler.signals.connect(obj.start_listening, signals.engine_started)
        crawler.signals.connect(obj.stop_listening, signals.engine_stopped)
        crawler.ushell = obj
        global ushell
        ushell = obj
        return obj
        
    def Run_syscmd(self, cmd):
        p = subprocess.Popen(cmd, shell=True)
        stdout, stderr = p.communicate()
        if stdout != None : print stdout
        if stderr != None : print stderr
    
    def ParaFunc(self, Func):
        mods = str(Func).split('.')
        key = None
        for i in range(0, len(mods)):
            func = mods[i]
            mod = sys.modules[__name__] if i==0 else key
            key = getattr(mod, func) if hasattr(mod, func) else None
            if key == None : break
        return key
         
    def SetPara(self, Func, value):
        mods = str(Func).split('.')
        key = None
        for i in range(0, len(mods)):
            func = mods[i]
            mod = sys.modules[__name__] if i==0 else key
            key = getattr(mod, func) if hasattr(mod, func) else None
            if key == None : break
        if key != None:
            setattr(mod, func, value)
            return value
        return None
    def parse_cmd(self, cmd=''):
        logger.debug(cmd)
        cmd = self.parser.json_parse(cmd)[0]
        if cmd['type'] == 'CMD_INIT_CALL':
            pass
        elif cmd['type'] == 'CMD_SYS_CALL':
            self. Run_syscmd(cmd['Mod'])
        else:
            do_func = self.ParaFunc(cmd['mod'])
            args = [cmd['arg%i'] for i in range(0, cmd['argcnt'])]
            try:
                if do_func and callable(do_func):
                    ret = do_func(args)
                else:
                    ret = do_func if len(args) == 0 else self.SetPara(do_func, args[0])
                print ret
            except Exception as e:
                logger.error("Can't Not Find the Mod%s") % do_func
                cmd['type'] = 'CMD_FAIL_RET'
                pass
        return cmd['type']
    def loop(self):
        while True:
            data, addr = self.sock.recvfrom(2048)
            logger.info('receive %(data)s from %(addr)s', {'data':data, 'addr':addr})
            try:
                data = self.parse_cmd(data)
            except Exception as e:
                logger.error('Exception %(Exception)s', {'Exception':e})
                logger.error(traceback.format_exc())
            finally:
                if data == None:
                    data = 'CMD_FAIL_RET'
                self.sock.sendto(data, addr)
                logger.debug('send %(data)s to %(addr)s', {'data':data, 'addr':addr})
    def run(self):
        self.loop()