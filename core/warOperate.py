# -*- coding: utf-8 -*-
__time__ = '2018/3/2 11:14'
__author__ = 'winkyi@163.com'

from utils import log
from utils.utils import GetConf,RabbitMQPublish
import json
from utils.encrypt import MyCrypt
import ConfigParser,sys


ed = MyCrypt()
logger = log.Log()


#目前消息是群发至每个节点，后续版本按节点来区分
def getChannel():
    return 'clond'

def getExchange():
    return 'cloud'

def sendCMDToSlave(param):
    logger.info('prepare send cmd to slave!')
    try:
        cf = GetConf("rbq.conf")
        ipaddr =  cf.getStr("main","host")
        port =  cf.getInt("main","port")
        username = cf.getStr("main",'username')
        password = ed.decrypt(cf.getStr("main",'password'))
        vhost = cf.getStr("main",'vhost')
    except ConfigParser.NoSectionError:
            logger.exception("configuration file saber.conf section is not found!!")
            sys.exit("process exit!")

    mq = RabbitMQPublish(username,password,ipaddr,port,vhost)
    mq.sendMessage(getExchange(),json.dumps(param))


