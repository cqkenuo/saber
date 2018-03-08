# -*- coding: utf-8 -*-
__time__ = '2018/2/28 15:16'
__author__ = 'winkyi@163.com'

import ConfigParser
import os
import platform
import pika
import socket
from encrypt import MyCrypt
import tarfile
import datetime
import shutil


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#conf文件夹在工程相对路径下的名字
conf_path = "conf"
ed = MyCrypt()

#判断系统是否为linux
def isLinux():
     if platform.system() == 'Linux':
          return True
     else:
          return False


"""
获取配置文件信息
"""



#定义MyConf类，重写optionxform方法，来解决值的大小写问题
class MyConf(ConfigParser.ConfigParser):
    def __init__(self,defaults=None):
        ConfigParser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr


class GetConf(object):
    def __init__(self, filename):
        if isLinux():
            confFile = "%s/%s/%s" %(base_dir,conf_path,filename)
        else:
            confFile = "%s\\%s\\%s" %(base_dir,conf_path,filename)
        self.cf=MyConf()
        self.cf.read(confFile)
        self.secDic = {}

    # 这里重写了optionxform方法，直接返回选项名
    def optionxform(self, optionstr):
        return optionstr

    def getStr(self,section,option):
        return self.cf.get(section,option)

    def getInt(self,section,option):
        return self.cf.getint(section,option)

    #返回一个section内的键值对，以字典格式输出
    def getOptions(self,section):
        secs = self.cf.items(section)
        for sec in secs:
            self.secDic[sec[0]] = sec[1]
        return self.secDic

    #获取所有章节名
    def getSecs(self):
        return self.cf.sections()



"""
消息队列生产者相关,一对一发送
"""
class RabbitMQ(object):
    def __init__(self,username,password,ipaddr,port,vhost):
        credentials = pika.PlainCredentials(username,password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(ipaddr,port,vhost,credentials))
        self.channel = self.connection.channel()

    def __del__(self):
        self.connection.close()

    def sendMessage(self,queue_name,message):
        self.channel.queue_declare(queue_name)
        self.channel.basic_publish(
            exchange = '',
            routing_key=queue_name,  #queue名字
            body = message #消息内容
        )


"""
消息队列发布、订阅
"""
class RabbitMQPublish(object):

    def __init__(self,username,password,ipaddr,port,vhost):
        credentials = pika.PlainCredentials(username,password)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(ipaddr,port,vhost,credentials))
        self.channel = self.connection.channel()



    def __del__(self):
        self.connection.close()

    def sendMessage(self,exchangeName,message):
        #发布方不需要声明queue 只需要有个exchange就可以了 ， exchange_type 类型是 fanout
        self.channel.exchange_declare(exchange=exchangeName,exchange_type='fanout')
        self.channel.basic_publish(exchange=exchangeName,  # 发布广播的时候 exchange定义要一致
                      routing_key='',   #必须要写成空
                      body=message)     #发送的消息主体

def getHostName():
    return socket.gethostname()


def getIPAddr():
    return socket.gethostbyname(getHostName())


#获取当前时间格式为yyyymmddhh24miss
def getCurrentTime():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")



#获取当天日期
def getCurrentDay():
    return datetime.datetime.now().strftime("%Y%m%d")


#压缩文件
def makeTar(sourcePath,targetPath,tarName):
    tar = tarfile.open('%s/%s.tar.gz' %(targetPath,tarName),'w:gz')
    for root ,dir,files in os.walk(sourcePath):
        root_ = os.path.relpath(root,start=sourcePath)
        for file in files:
            fullpath = os.path.join(root,file)
            tar.add(fullpath,arcname=os.path.join(root_,file))
    tar.close()

#解压文件
def unTar(sourcePath,tarName,unzipPath):
    t = tarfile.open("%s/%s" %(sourcePath,tarName))
    t.extractall(path=unzipPath)



#判断路径是否存在，如果不存在，创建
def pathIsExists(path):
    try:
        # 去除首位空格
        path=path.strip()
        # 去除尾部 \ 符号
        path=path.rstrip("\\")
        isExists=os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        return True
    except:
        return False

#判断路径是否存在
def isPath(path):
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    isExists=os.path.exists(path)
    if isExists:
        return True
    else:
        return False


#判断文件是否存在
def fileIsExist(fileName):
    if os.access(fileName, os.F_OK):
        return True
    else:
        return False



#获取文件大小
def getFileSize(fileName):
    fsize = os.path.getsize(fileName)
    return fsize



#获取家目录
def getHomePath():
    return os.environ['HOME']


#删除文件夹
def delDir(delDir):
    delList = os.listdir(delDir)
    for f in delList:
        filePath = os.path.join(delDir, f )
        if os.path.isfile(filePath):
            os.remove(filePath)
            print filePath + " was removed!"
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath,True)
            print "Directory: " + filePath +" was removed!"


#判断文件夹是否为空
def isNullDir(work_path):
    if not os.listdir(work_path):
        return True
    else:
        return False

if __name__ == '__main__':
    #conf配置文件的相关
    cf = GetConf("rbq.conf")
    # ipaddr =  cf.getStr("main","host")
    # port =  cf.getInt("main","port")
    # username = cf.getStr("main",'username')
    # password = cf.getStr("main",'password')
    # vhost = cf.getStr("main",'vhost')

    # mq = RabbitMQPublish(username,ed.decrypt(password),ipaddr,port,vhost)
    # mq.sendMessage('cloud','okokok666')
    print cf.getOptions('main')

    ##测试解压压缩
    # makeTar('/home/ap/ldap/software/git-2.9.5','/home/ap/ldap/tools/backup','git')
    # unTar('/home/ap/ldap/tools/backup','git_20180307092718.tar.gz','/home/ap/ldap/tools/git')

    #判断路径是否存在，不存在就创建
    aa = pathIsExists("%s/chenwq222" %getHomePath())
    print aa

    bb = isPath("tools/apache-tomcat-8.5.24")
    print bb

    #判断文件是否存在
    cc = fileIsExist("/home/ap/ldap/1.log")
    print cc


    #获取文件大小
    print getFileSize("/home/ap/ldap/tools/backup/test_20180307150838.tar.gz")

    #删除文件夹
    # delDir("/home/ap/ldap/tools/apache-tomcat-8.5.24")

    #文件夹是否为空
    print isNullDir("/home/ap/ldap/tools/apache-tomcat-8.5.24")

