# -*- coding: utf-8 -*-
__time__ = '2018/3/9 09:53'
__author__ = 'winkyi@163.com'

from utils import redisManager,log
from utils.utils import *

class ShowOperate(object):

    def __init__(self,param):
        self.redis_cli = redisManager.redis_cli()
        self.param = param

    def getItem(self):
        if hasattr(self,self.param):
            func = getattr(self,self.param)
            func()

    @printFormat('nodes')
    def nodes(self):
        nodes = self.redis_cli.hgetall('nodes')
        for k,v in nodes.items():
            print "%s  %s\n" %(k,v)

    def servers(self):
        pass


