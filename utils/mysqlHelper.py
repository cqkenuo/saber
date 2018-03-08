# -*- coding: utf-8 -*-
__time__ = '2018/3/2 10:19'
__author__ = 'winkyi@163.com'

import MySQLdb
from log import Log
import utils
import sys

logger = Log()


"""
mysql数据库相关
"""
class MysqlBase(object):

    def __init__(self,ipaddr,username,password,dbname,port):
        try:
            self.db = MySQLdb.connect(ipaddr,username,password,dbname,port)
            self.cursor = self.db.cursor()
        except:
            logger.exception("Can't connect to MySQL server on %s" %ipaddr)

    def __del__(self):
        self.cursor.close()
        self.db.close()

    #数据库查询操作
    def query_data(self,sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
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



class MysqlHelper(object):

    def __init__(self):
        cf = utils.GetConf("mysql.conf")
        host = cf.getStr('db','host')
        port = cf.getInt('db','port')
        username = cf.getStr('db','username')
        password = cf.getStr('db','password')
        dbname = cf.getStr('db','dbname')
        self.obj = MysqlBase(host,username,password,dbname,port)


    #查询nodes节点的信息
    #remark 0 slave节点，1 master节点 2 所有节点
    def findNodeInfo(self,mark):
        nodes = {}
        if mark == 2:
            sql = 'select nHostname,nIP from node_info'
        elif mark == 0:
            sql = 'select nHostname,nIP from node_info where isMaster=0'
        elif mark == 1:
            sql = 'select nHostname,nIP from node_info where isMaster=1'
        for node in self.obj.query_data(sql):
            if node is not None:
                nodes[node[0]] = node[1]
        return nodes


    #查询所有node节点
    def getAllNodeInfo(self):
        return self.findNodeInfo(2)
    #查询master节点
    def getMasterNode(self):
        return self.findNodeInfo(1)
    #查询slave节点
    def getSlaveNode(self):
        return self.findNodeInfo(0)


    #查询参数表内容
    def getParam(self):
        params = {}
        sql = 'select pKey,pValue,pRemark from param'
        for param in self.obj.query_data(sql):
            if param is not None:
                params[param[0]] = param[1]

        return params



if __name__ == '__main__':
    ms = MysqlHelper()
    print ms.getAllNodeInfo()
    print ms.getMasterNode()
    print ms.getSlaveNode()
    print ms.getParam()
    print ms.getParam()['uassPath']