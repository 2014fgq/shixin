#coding:utf-8
'''
Created on 2015-8-18

@author: Haier
'''
import cmd
import string,sys
import logging
import socket
import UShell_json
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class UShell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '>'
        self.remote_address = []
        self.sock = None
        self.parser = UShell_json.json_factory().create_json_parser('pshell_json')
        self.syscmdlist = []
        self.do_bind("0.0.0.0", "31501")
        self.innercmd = [tcmd[3:] for tcmd in dir(self) if tcmd[:3] == "do_"]
        
    def do_bind(self, ip='127.0.0.1', port = '31501'):
        try:
            IP = ip
            Port = int(port)
            self.address = (IP,Port)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(self.address)
            print "[Bind]%s:%d" %(self.address)
        except Exception,e:
            print e
        
    def do_connect(self, arg='127.0.0.1 31500'):
        IP = '127.0.0.1'
        Port = int('31500')
        if len(arg)>0:
        	arg = arg.split(' ')
        if len(arg)>0:
            IP = arg[0]
        if len(arg)>1:
            try:
                Port = int(arg[1])
            except Exception,e:
                print e
                return None
        try:
            self.remote_address = (IP,Port)
        except Exception,e:
            print e
            return None
        self.sock.settimeout(5)
        try:
            self.cmdsend(self.parser.json_init('hello_world'))
            print 'connect %s:%d Success!' % (self.remote_address)
        except:
            print 'connect %s:%d Fail!' % (self.remote_address)
        self.sock.settimeout(0)
    def cmdsend(self, cmd=''):
        data, addr = '',''
        if self.sock is not None and self.remote_address != () and self.remote_address != []:
            try:
                self.sock.sendto(cmd, self.remote_address)
                data, addr = self.sock.recvfrom(2048)
            except Exception,e:
                print e
                raise e
            if data and addr:
                return True
        return False               
    def do_hello(self, arg):
        print "hello again", arg, "!"
        
    def help_hello(self):
        print "syntax: hello [message]"
        print '-- prints a hello message'
    
    def do_disconnect(self, arg):
        if self.remote_address != []:
            print 'disconnect %s ' % self.remote_address
            self.remote_address = []
    
    def do_quit(self, arg):
        sys.exit(1)
        
    def help_quit(self):
        print "syntax: quit"
        print '--terminates the application'
    
       
    def do_UShell(self, arg):
        logger.debug(arg)
        message = self.parser.json_pack(self.syscmdlist, arg)
        if self.remote_address != () and self.remote_address != []:
			try:
				self.cmdsend(message)
			except:
				print "%s send error!" % arg
        return
        #if self.Cmd == 0:
        #    self.Run
    def precmd(self, line):
        """Hook method executed just before the command line is
        interpreted, but after the input prompt is generated and issued.
        """
        if len(line):
            cmd = line.split(" ")
            for innercmd in self.innercmd:
                if cmd[0] == innercmd:
                    return line
            line = 'UShell ' + line
        return line
    do_q = do_quit
    do_c = do_connect
    do_d = do_disconnect
if __name__ == '__main__':
    ushell = UShell()
    ushell.cmdloop()