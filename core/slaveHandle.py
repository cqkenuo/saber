# -*- coding: utf-8 -*-
__time__ = '2018/3/6 14:29'
__author__ = 'winkyi@163.com'
import json,sys
from utils.utils import *
from utils import log
from backend.transfer import Transfer
from utils.encrypt import MyCrypt

logger = log.Log()
dc = MyCrypt()


class SlaveHandle(object):
    def __init__(self,param):
        self.param_dic = json.loads(param)
        try:
            if self.param_dic['operate'] in ['backup','update','restore']:
                self.getProjectParam()
            elif self.param_dic['operate'] == 'distribute':
                self.getFileParam()
        except KeyError:
            logger.exception("param_dic has not key!please check!!")
            sys.exit('slave param error,process exit')
        except Exception:
            logger.exception("init slave param fail!!!")
        self.getVersionLibParam()
        self.transfer = Transfer(self.versionLib_ip,self.versionLib_sshPort,self.versionLib_hostname,self.versionLib_password)

    def getProjectParam(self):
        self.project_backupPath = str(getHomePath()+'/'+self.param_dic['project_backupPath'])
        self.project_name = str(self.param_dic['project_name'])
        self.project_path = str(getHomePath()+'/'+self.param_dic['project_path'])
        self.project_versionLib = str(getHomePath()+'/'+self.param_dic['project_versionLib'] +'/' +getCurrentDay())
        self.project_tgzName = str(self.param_dic['project_tgzName'])
        self.versionLib_path = str(self.param_dic['versionLib_path'] +'/' +getCurrentDay())


    def getVersionLibParam(self):
        self.versionLib_ip = str(self.param_dic['versionLib_ip'])
        self.versionLib_sshPort = int(self.param_dic['versionLib_sshPort'])
        self.versionLib_hostname = str(self.param_dic['versionLib_hostname'])
        self.versionLib_password = str(dc.decrypt(self.param_dic['versionLib_password']))


    def getFileParam(self):
        self.remoteFile = self.param_dic['remoteFile']
        self.soureFile = self.param_dic['soureFile']

    def handle(self):
        #备份操作
        if self.param_dic['operate'] == 'backup':
            print "backup project %s" %self.param_dic['backup']
            self.backup(self.project_backupPath,self.project_name,self.project_path)

        #更新操作
        if  self.param_dic['operate'] == 'update':
            print "update project %s" %self.param_dic['update']
            #更新操作前必须要备份
            self.backup(self.project_backupPath,self.project_name,self.project_path)
            #更新操作
            self.update(self.project_versionLib,self.project_name,self.project_path,self.project_backupPath)

        #回退操作
        if  self.param_dic['operate'] == 'restore':
            print "restore project %s" %self.param_dic['restore']

        #文件分发操作
        if self.param_dic['operate'] == 'distribute':
            self.distribute(self.param_dic)


    def backup(self,project_backupPath,project_name,project_path):
        if not isPath(project_path):
            logger.error("project %s is not exist,don't excute backup operate!!!!!" % project_path)
        else:
            if pathIsExists(project_backupPath):
                try:
                    logger.info("start backup project")
                    print "project_path:",project_path
                    print "project_backupPath:",project_backupPath
                    print "project_name:",project_name
                    self.backup_project_name = "%s_%s" %(project_name,getCurrentTime())
                    makeTar(project_path,project_backupPath,self.backup_project_name)
                except:
                    logger.exception("backup fail: tar cmd error!!!")
            else:
                logger.error("backup path is error!!!")


    #更新操作
    #project_name工程包的名称
    #self.project_name备份后工程包的名称，已带上日期
    def update(self,project_versionLib,project_name,project_path,project_backupPath):
        #判断本地版本库路径是否存在,不存在就创建
        if pathIsExists(project_versionLib):
            if pathIsExists(project_path):
                #判断备份是否完成
                if fileIsExist("%s/%s.tar.gz"  %(project_backupPath,self.backup_project_name)) and getFileSize("%s/%s.tar.gz"%(project_backupPath,self.backup_project_name))  > 0:
                    #从版本机获取版本至本地版本放置路径
                    logger.info("start get remote verionLib project!")
                    self.transfer.sftp_down_file('%s/%s' %(self.versionLib_path,self.project_tgzName),'%s/%s' %(project_versionLib,self.project_tgzName))
                    logger.info("success get remote versionLib project!")
                    #删除旧版本目录
                    delDir(self.project_path)
                    #从本地版本解压包至工程目录
                    if isNullDir(self.project_path):
                        unTar(self.project_versionLib,self.project_tgzName,self.project_path)
                    else:
                        logger.info("project path is not null,please empty path!")
                    #配置环境变量,看情况

                    #启动工程
                    """
                    #!/bin/bash
                    JAVA_HOME=/home/xinli/jdk1.8.0_92
                    JAVA=$JAVA_HOME/bin/java
                    nohup $JAVA -jar yunnan-rest-service-0.1.0.jar -Djava.ext.dirs=$JAVA_HOME/lib &
                """

                    #检查启动情况

                else:
                    logger.error("UPDATE:[backupfile is not find ,update operate stop!]")
            else:
                logger.error("UPDATE:[create project path fail!]")
        else:
            logger.error("UPDATE:[create versionLib path fail!]")


    def restore(self):
        pass




    def distribute(self,fileParam):
        soureFile = fileParam['soureFile']
        remoteFile = fileParam['remoteFile']
        remotePath = "/".join(remoteFile.split('/')[0:-1])
        if self.transfer.sftp_exec_command("ls -l %s" %remotePath):
            if fileIsExist(soureFile):
                logger.info("start distribute file")
                self.transfer.sftp_upload_file(remoteFile,soureFile)
                logger.info("success distribute file %s" %remoteFile)
            else:
                logger.error("local file %s is not exist" %soureFile)
        else:
            logger.error("remote path %s is not exist!!" %remotePath)


