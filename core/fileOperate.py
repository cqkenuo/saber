# -*- coding: utf-8 -*-
__time__ = '2018/3/12 09:53'
__author__ = 'winkyi@163.com'

from utils.utils import *
from utils import log
import sys,json

logger = log.Log()

class FileOperate(object):

    def __init__(self,fileParam):
        self.param =  fileParam

    def getExchange(self):
        return 'cloud'

    def distribute(self):
        self.param['operate'] = 'distribute'
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
        mq.sendMessage(self.getExchange(),json.dumps(self.param))