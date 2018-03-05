# -*- coding: utf-8 -*-
__time__ = '2018/2/27 15:23'
__author__ = 'winkyi@163.com'
import sys
from optparse import OptionParser
from warOperate import *
from utils import redisManager
from utils import log

logger = log.Log()


class Saber(object):

    def __init__(self):
        self.redis_cli = redisManager.redis_cli()
        self.project_set = self.redis_cli.smembers('project')
        self.versionLib_dic = self.redis_cli.hgetall('versionLib')
        self.operParam = {}

    def main(self):
        parser = OptionParser(usage="usage: %prog [options] arg1 arg2")
        parser.add_option("-s","--show",type="choice",choices = ['nodes', 'servers'],dest="show_status",help=u"显示server、node等信息")
        parser.add_option("-b",'--backup',type="choice",choices =list(self.project_set),dest="backup_project",help=u'备份工程')
        parser.add_option("-u",'--update',type="choice",choices =list(self.project_set),dest="update_project",help=u'更新工程')
        parser.add_option("-r",'--restore',type="choice",choices =list(self.project_set),dest="restore_project",help=u'回退工程')
        (options,agrs) = parser.parse_args()

        print "options: %s" %options
        print "args: %s" %agrs

        #如果是show命令
        if options.show_status:
            print options.show_status




        #如果命令是带-c,-b,-u
        #{'backup':'redis','update':'redis','versionPath':'xxxxx','projectPath':'xxxxxx','backupPath':'xxxxx'}
        if options.backup_project:
            self.operParam['backup'] = options.backup_project

        if options.update_project:
            self.operParam['update'] = options.backup_project

        if options.restore_project:
            self.operParam['restore'] = options.backup_project


        #判断备份和更新的工程是否一样，强制要求要一样
        if options.backup_project != options.update_project:
            logger.error("backup project is no same update! process exit")
            sys.exit()

        if self.operParam:
            project_dic = self.redis_cli.hgetall(options.backup_project)
            nodeParam = dict(self.versionLib_dic, **self.operParam)
            paramInof = dict(nodeParam, **project_dic)
            sendCMDToSlave(paramInof)

