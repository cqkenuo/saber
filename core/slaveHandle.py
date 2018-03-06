# -*- coding: utf-8 -*-
__time__ = '2018/3/6 14:29'
__author__ = 'winkyi@163.com'
import json


class SlaveHandle(object):
    def __init__(self):

        pass


    def handle(self,param):
        param_dic = json.loads(param)
        print (" [x] Received %r" % param_dic)
        print ("data type is %s" % type(param_dic))
        print ("master host ip is :%s" %param_dic['hostname'])

        #判断需要执行的参数
        param_keys = param_dic.keys()
        print "param keys: %s" % param_keys
        if 'backup' in param_keys:
            print "backup project %s" %param_dic['backup']
            backupPath = param_dic['backupPath']
            projectName = param_dic['projectName']
            projectPath = param_dic['projectPath']
            print "projectPath:%s,backupPath:%s,projectName:%s" %(projectPath,backupPath,projectName)
        if  'update' in param_keys:
            print "update project %s" %param_dic['update']
        if  'restore' in param_keys:
            print "restore project %s" %param_dic['restore']

