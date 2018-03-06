# -*- coding: utf-8 -*-
__time__ = '2018/2/28 14:16'
__author__ = 'winkyi@163.com'
from utils import redisManager
from utils import log
from utils.utils import GetConf
import socket
import json,pika
from utils.encrypt import MyCrypt


logger = log.Log()
ed = MyCrypt()

class Slave(object):

    def __init__(self):
        #注册主机信息到redis
        redis_cli = redisManager.redis_cli()
        redis_cli.hset("nodes",'hostname',socket.gethostname())
        redis_cli.hset('nodes','ipaddr',socket.gethostbyname(socket.gethostname()))
        cf = GetConf("rbq.conf","main")
        self.ipaddr =  cf.get("host")
        self.port =  cf.getInt("port")
        self.username = cf.get('username')
        self.password = ed.decrypt(cf.get('password'))
        self.vhost = cf.get('vhost')



    def getChannel(self):
        return 'clond'

    def getExchange(self):
        return 'cloud'

    #消息队列消费者，单一收取，靠渠道
    def getMQdata(self):
        credentials = pika.PlainCredentials(self.username,self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.ipaddr,self.port,self.vhost,credentials))
        channel = connection.channel()
        channel.queue_declare(self.getChannel())

        channel.basic_consume(self.callback,
                          queue=self.getChannel(),
                          no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


    #消息队列订阅者
    def subscribe(self):
        credentials = pika.PlainCredentials(self.username,self.password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.ipaddr,self.port,self.vhost,credentials))
        channel = connection.channel()
        #exchange 转发器，exchange_type=fanout 绑定到这个转发器上的消费者都能接收到消息
        channel.exchange_declare(exchange=self.getExchange(), exchange_type='fanout')
        # 随机queue 不指定queue名字,rabbit会随机分配一个名字,exclusive=True会在使用此queue的消费者断开后,自动将queue删除
        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue #获取queueu的名字
        channel.queue_bind(exchange=self.getExchange(),  #绑定到这个转发器上，只能从这个转发器上接收
                   queue=queue_name)  #指定queue的名字 转发器把消息发送到这个queue上，消费者从这个queue上接收消息

        channel.basic_consume(self.callback,
                      queue=queue_name,
                      no_ack=True)
        print(' [*] Waiting for logs. To exit press CTRL+C')
        channel.start_consuming()


    def callback(self,ch,method,properties,body):
        print (" [x] Received %r" % body)
        logger.info(" [x] Received %r" % body)





if __name__ == '__main__':
    s = Slave()
    # s.getMQdata()
    s.subscribe()
