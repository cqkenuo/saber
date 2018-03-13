# -*- coding: utf-8 -*-
__time__ = '2018/3/13 14:26'
__author__ = 'winkyi@163.com'
import sys

class CommonException(Exception):

    def __init__(self,code="",msg=""):
        self.code = code
        self.msg = msg
        sys.stderr.write('commonException:%s (%s)\n' %(code,msg))

    def __repr__(self):
        return 'commonException:%s (%s)\n' %(self.code,self.msg)

    def __str__(self):
        return 'commonException:%s (%s)\n' %(self.code,self.msg)