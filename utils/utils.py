# -*- coding: utf-8 -*-
__time__ = '2018/2/28 15:16'
__author__ = 'winkyi@163.com'

import ConfigParser
import os
import platform
import pika
import socket
from encrypt import MyCrypt

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

if __name__ == '__main__':
    #conf配置文件的相关
    cf = GetConf("rbq.conf","main")
    ipaddr =  cf.get("host")
    port =  cf.getInt("port")
    username = cf.get('username')
    password = cf.get('password')
    vhost = cf.get('vhost')

    # mq = RabbitMQ(username,password,ipaddr,port,vhost)
    # mq.sendMessage('test','okokok')

    mq = RabbitMQPublish(username,ed.decrypt(password),ipaddr,port,vhost)
    mq.sendMessage('cloud','okokok666')
