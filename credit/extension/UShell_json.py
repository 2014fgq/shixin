#coding:utf-8
'''
Created on 2015-8-30

@author: Haier
'''

import json
import re
class pshell_json():
    def __init__(self):
        self.mod = None
        self.arg = None
    
    def para_arg(self, arg):
        try:
            mod = arg.split(' ')[0]
            arg = ' '.join(arg.split( )[1:])
            return mod, arg
        except Exception,e:
            print e
        return None, None

    def json_pack(self, syscmd, arg):
        Issyscmd = False
        mod, args = self.para_arg(arg)
        cmd = {}
        cmd['argcnt'] = 0
        for i in range(0, len(syscmd)):
            if mod == syscmd[i]:
                Issyscmd = True
                break
        if Issyscmd == True:
            cmd['type'] = 'CMD_SYS_CALL'
        else:
            cmd['type'] = 'CMD_FUNC_CALL'
        cmd['mod'] = mod
        if arg:
            if len(args) > 0:args=args.split(',')
            string_to_int = re.match(r'[+-]?\d+$', arg.strip()) and (lambda arg:int(arg)) or (lambda arg:arg)
            args = map(string_to_int, args)
        for i in range(0, len(args)):
            cmd['arg%d'%i] = args[i]
        cmd['argcnt'] = int(len(args))
        
        return json.dumps([cmd])
    
    def json_init(self, string):
        cmd = {}
        cmd['type'] = 'CMD_INIT_CALL'
        cmd['mode'] = string
        cmd['argcnt'] = 0
        return json.dumps([cmd])
     
    def json_parse(self, arg):
        return json.loads(arg)
    
class json_factory():
    def __init__(self):
        pass
    def create_json_parser(self, string=''):
        if string == 'pshell_json' :
            return pshell_json();
        return None
    
if __name__ == '__main__':
    pass
    
    