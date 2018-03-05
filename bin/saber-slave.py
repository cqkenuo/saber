# -*- coding: utf-8 -*-
__time__ = '2018/2/28 14:16'
__author__ = 'winkyi@163.com'
from utils import redisManager
from utils import log
from utils.utils import GetConf
import socket
import json,pika


logger = log.Log()

class Slave(object):

    def __init__(self):
        #注册主机信息到redis
        redis_cli = redisManager.redis_cli()
        redis_cli.hset("nodes",'hostname',socket.gethostname())
        redis_cli.hset('nodes','ipaddr',socket.gethostbyname(socket.gethostname()))



    def getChannel(self):
        return 'clond'

    def getMQdata(self):
        cf = GetConf("rbq.conf","main")
        ipaddr =  cf.get("host")
        port =  cf.getInt("port")
        username = cf.get('username')
        password = cf.get('password')
        vhost = cf.get('vhost')
        credentials = pika.PlainCredentials(username,password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(ipaddr,port,vhost,credentials))
        channel = connection.channel()
        channel.queue_declare(self.getChannel())

        channel.basic_consume(self.callback,
                          queue=self.getChannel(),
                          no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

    def callback(self,ch,method,properties,body):
        print (" [x] Received %r" % body)
        logger.info(" [x] Received %r" % body)





if __name__ == '__main__':
    s = Slave()
    s.getMQdata()

