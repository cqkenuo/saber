# -*- coding: utf-8 -*-
__time__ = '2018/2/28 15:16'
__author__ = 'winkyi@163.com'

import ConfigParser
import os
import platform
import pika
import MySQLdb

from log import Log
logger = Log()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#conf文件夹在工程相对路径下的名字
conf_path = "conf"


#判断系统是否为linux
def isLinux():
     if platform.system() == 'Linux':
          return True
     else:
          return False


"""
获取配置文件信息
"""
class GetConf(object):

    def __init__(self,filename,section):
        if isLinux():
            confFile = "%s/%s/%s" %(base_dir,conf_path,filename)
        else:
            confFile = "%s\\%s\\%s" %(base_dir,conf_path,filename)
        self.cf =  ConfigParser.ConfigParser()
        self.cf.read(confFile)
        self.section = section

    def get(self,option):
        return self.cf.get(self.section,option)

    def getInt(self,option):
        return self.cf.getint(self.section,option)



"""
消息队列相关
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
mysql数据库相关
"""
class MysqlHelper(object):

    def __init__(self,ipaddr,username,password,dbname,port):
        self.db = MySQLdb.connect(ipaddr,username,password,dbname,port)
        self.cursor = self.db.cursor()

    def __del__(self):
        self.cursor.close()
        self.db.close()

    #数据库查询操作
    def query_data(self,sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fectchall()
            for row in result:
                print row
        except:
            logger.exception("Error: unable to fetch data")

    #数据库插入操作
    #sql的格式：
    #insert into table_name(xxxx) values ('%s') %("xxxxx")
    def insert_data(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logger.info("insert [%s] sql success!" % sql)
        except:
            logger.exception("Error: insert [%sql] fail!" %sql)
            self.db.rollback()

    def update_data(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
            logger.info("update [%s] sql success!" % sql)
        except:
            logger.exception("Error: update [%sql] fail!" %sql)
            self.db.rollback()



if __name__ == '__main__':
    #conf配置文件的相关
    cf = GetConf("rbq.conf","main")
    ipaddr =  cf.get("host")
    port =  cf.getInt("port")
    username = cf.get('username')
    password = cf.get('password')
    vhost = cf.get('vhost')

    mq = RabbitMQ(username,password,ipaddr,port,vhost)
    mq.sendMessage('test','okokok')

