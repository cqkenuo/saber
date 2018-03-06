# -*- coding: utf-8 -*-
__time__ = '2018/3/2 11:14'
__author__ = 'winkyi@163.com'

from utils import log
from utils.utils import GetConf,RabbitMQPublish
import json
from utils.encrypt import MyCrypt

ed = MyCrypt()


logger = log.Log()


#目前消息是群发至每个节点，后续版本按节点来区分
def getChannel():
    return 'clond'

def getExchange():
    return 'cloud'

def sendCMDToSlave(param):
    logger.info('prepare send cmd to slave!')
    cf = GetConf("rbq.conf","main")
    ipaddr =  cf.get("host")
    port =  cf.getInt("port")
    username = cf.get('username')
    password = ed.decrypt(cf.get('password'))
    vhost = cf.get('vhost')

    mq = RabbitMQPublish(username,password,ipaddr,port,vhost)
    mq.sendMessage(getExchange(),json.dumps(param))


