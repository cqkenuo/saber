# -*- coding: utf-8 -*-
__time__ = '2018/2/28 14:16'
__author__ = 'winkyi@163.com'
from utils import redisManager
from utils import log
from utils.utils import GetConf
import ConfigParser
import socket
import pika
import sys
from utils.encrypt import MyCrypt
from core.slaveHandle import SlaveHandle
import threading


logger = log.Log()
ed = MyCrypt()

class Slave(object):

    def __init__(self):
        self.redis_cli = redisManager.redis_cli()
        self.saberConf = GetConf('saber.conf')
        self.mqConf = GetConf('rbq.conf')
        self.registerNode()
        self.getMQItem()

    #将node注册到redis,定时器，30秒执行一次
    def registerNode(self):
        try:
            heartbeat =  self.saberConf.getInt("node","heartbeat")
            effect = self.saberConf.getInt("node","effect")
        except ConfigParser.NoSectionError:
            logger.exception("configuration file saber.conf section is not found!!")
            sys.exit("process exit!")
        else:
            logger.info("register node [%s]" %socket.gethostbyname(socket.gethostname()))
            global timer
            self.redis_cli.hset("nodes",socket.gethostname(),socket.gethostbyname(socket.gethostname()))
            #设置key1分钟后失效
            self.redis_cli.expire('nodes',effect)
            timer = threading.Timer(heartbeat,self.registerNode)
            timer.start()

    #获取消息队列信息
    def getMQItem(self):
        try:
            self.ipaddr =  self.mqConf.getStr("main","host")
            self.port =  self.mqConf.getInt("main","port")
            self.username = self.mqConf.getStr("main",'username')
            self.password = ed.decrypt(self.mqConf.getStr("main",'password'))
            self.vhost = self.mqConf.getStr("main",'vhost')
        except ConfigParser.NoSectionError:
            logger.exception("configuration file rbq.conf section is not found!!")
            sys.exit("process exit!")

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
        sh = SlaveHandle(body)
        sh.handle()
        logger.info(" [x] Received %r" % body)

if __name__ == '__main__':
    try:
        s = Slave()
        s.subscribe()
    except KeyboardInterrupt:
        sys.exit("user press Ctrl+C exits process")
