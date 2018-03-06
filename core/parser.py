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


        #判断备份和更新的工程是否一样，强制要求要一样
        if options.backup_project and  options.update_project:
            if options.backup_project != options.update_project:
                logger.error("backup project is no same update! process exit")
                sys.exit()

        #回退操作必须单独执行
        if options.restore_project:
            if options.backup_project or  options.update_project:
                logger.error("exist restore operate,not allow backup or update operate! process exit")
                sys.exit()

        #如果命令是带-c,-b,-u
        #{'backup':'redis','update':'redis','versionPath':'xxxxx','projectPath':'xxxxxx','backupPath':'xxxxx'}
        if options.backup_project:
            self.operParam['backup'] = options.backup_project
            project_name = options.backup_project

        if options.update_project:
            self.operParam['update'] = options.update_project
            project_name = options.update_project


        if options.restore_project:
            self.operParam['restore'] = options.restore_project
            project_name = options.restore_project


        if self.operParam:
            project_dic = self.redis_cli.hgetall(project_name)
            nodeParam = dict(self.versionLib_dic, **self.operParam)
            paramInof = dict(nodeParam, **project_dic)
            sendCMDToSlave(paramInof)

