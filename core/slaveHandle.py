# -*- coding: utf-8 -*-
__time__ = '2018/3/6 14:29'
__author__ = 'winkyi@163.com'
import json
from utils.utils import *
from utils import log


logger = log.Log()

class SlaveHandle(object):
    def __init__(self):

        pass


    def handle(self,param):
        param_dic = json.loads(param)
        print (" [x] Received %r" % param_dic)

        #判断需要执行的参数
        param_keys = param_dic.keys()
        print "param keys: %s" % param_keys

        project_backupPath = getHomePath()+'/'+param_dic['project_backupPath']
        project_name = param_dic['project_name']
        project_path = getHomePath()+'/'+param_dic['project_path']
        project_versionLib = getHomePath()+'/'+param_dic['project_versionLib']

        #备份操作
        if 'backup' in param_keys:
            print "backup project %s" %param_dic['backup']
            self.backup(project_backupPath,project_name,project_path)

        #更新操作
        if  'update' in param_keys:
            print "update project %s" %param_dic['update']
            #判断本地版本库路径是否存在,不存在就创建
            if pathIsExists(project_versionLib):
                if pathIsExists(project_path):
                    pass
                    #解压tar包

                    #配置环境变量

                else:
                    logger.error("UPDATE:[create project path fail!]")
            else:
                logger.error("UPDATE:[create versionLib path fail!]")



        if  'restore' in param_keys:
            print "restore project %s" %param_dic['restore']



    def backup(self,project_backupPath,project_name,project_path):
        if not isPath(project_path):
            logger.error("project %s is not exist,don't excute backup operate!!!!!" % project_path)
        else:
            if pathIsExists(project_backupPath):
                try:
                    logger.info("start backup project")
                    print "project_path:",project_path
                    print "project_backupPath:",project_backupPath
                    print "project_name:",project_name.replace('.war','')
                    makeTar(project_path,project_backupPath,project_name.replace('.war',''))
                except:
                    logger.exception("backup fail: tar cmd error!!!")
            else:
                logger.error("backup path is error!!!")


    def update(self):
        pass


    def restore(self):
        pass



