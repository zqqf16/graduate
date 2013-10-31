#! /usr/bin/env python
"""the wrapper of c functions"""
# -*- coding: UTF-8 -*-

from ctypes import *

class ZsReturn(Structure):
    _fields_ = [('mes', c_char_p),
                ('res', c_int)]

class ZsDataHead(Structure):
	pass

ZsDataHead._fields_ = [('data', POINTER(c_ubyte)),
					   		   ('size', c_int),
					   		   ('next', POINTER(ZsDataHead))
					  		  ]

class Interface:
    def __init__(self):

        dll = CDLL("./libzs.so")
        self.zinit = dll.zs_init
        self.zinit.restype = POINTER(ZsReturn)
        self.zstart = dll.zs_start
        self.zstop = dll.zs_stop            
        self.zclean = dll.zs_clean
        self.zhead = POINTER(ZsDataHead).in_dll(dll, 'head')
		
    def init(self):
        ret = POINTER(ZsReturn)
        ret = self.zinit()
        print ret.contents.res
        
    def start(self):
        self.zstart()
        
    def stop(self):
        self.zstop()
        
    def clean(self):
        self.zclean()
        
if __name__ == '__main__':
    import time
    import os
    print os.getcwd()
    zs = Interface()
    print 'Ready'
    zs.init()
    print 'init'
    zs.start()
    print 'start'
    time.sleep(0.1)
    zs.stop()
    print 'stop'
    eth = zs.zhead.contents.data
    print 'TO:      %02X%02X%02X%02X%02X%02X' % (eth[0], eth[1], eth[2], eth[3], eth[4], eth[5])
    print 'FROM:    %02X%02X%02X%02X%02X%02X' % (eth[6], eth[7], eth[8], eth[9], eth[10], eth[11])
    zs.clean()
    print 'clean'
                        
