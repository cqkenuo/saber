# -*- coding: utf-8 -*-
__time__ = '2018/2/27 15:23'
__author__ = 'winkyi@163.com'
import sys
from optparse import OptionParser





class Saber(object):
    def main(self):
        parser = OptionParser(usage="usage: %prog [options] arg1 arg2")
        parser.add_option("-s","--show",action="store",dest="show_status",help=u"显示server、node等信息")
        (options,agrs) = parser.parse_args()

        if parser.has_option('-s'):
            args = options.show_status
            if hasattr(self,args):
                func = getattr(self,args)
                func()
            else:
                self.message(options.show_status)


    def message(self,param):
        print u"错误的参数信息,无此参数 %s,参数列表[nodes,servers]" %param

    def nodes(self):
        print u"显示有几个节点接入"

    def servers(self):
        print u"显示每个服务部署在哪台机器上"




