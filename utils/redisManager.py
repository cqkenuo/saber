# -*- coding: utf-8 -*-
__time__ = '2018/3/2 15:41'
__author__ = 'winkyi@163.com'

from utils import GetConf
import redis


"""
这种方法居然不行，一直报TypeError: 'Redis' object is not callable，后续再看看
class RedisManager(object):

    def __init__(self,host,port,db):
        self.redis_client = redis.Redis(host=host,port=port,db=db)

    def get(self,key):
        return self.redis_client(key)

    def set(self,key,value):
        return self.redis_client(key,value)

"""
def redis_cli():
    cf = GetConf("redis.conf","redis")
    ipaddr =  cf.get("host")
    port =  cf.getInt("port")
    return redis.Redis(host=ipaddr,port=port,db=0)

if __name__ == '__main__':
    r = redis_cli()
    # r.set('name','chenwq1')
    # print r.get('name')
    #
    # #使用hash类型存储对象
    # r.hset("user",'name','chenwq')
    # r.hset('user','age','32')
    # r.hset('user','handset','11111111')
    # r.hincrby('user','visits',1)  #每次加1
    # r.save()
    # user_dic = r.hgetall('user')
    # print user_dic,type(user_dic)
    # user_key = r.hkeys('user')
    # print user_key,type(user_key)


    # project = ['redis','mysql','mangodb']
    # #使用list存储对象
    # #入队
    # for key in project:
    #     r.lpush('project',key)
    #
    # proLen = r.llen('project')
    # print "project param len: %s" %proLen
    # #获取list内数值
    # pro_list = r.lrange('project',0,proLen)
    # print "project param data: %s" % pro_list

    # #使用set存储数据
    # for key in project:
    #     print key
    #     r.sadd('project',key)
    #
    # #获取name对应的集合的所有成员
    # pro_set = r.smembers('project')
    # for aa in pro_set:
    #     print aa
    # print pro_set
    # r.save()


    #以下为初始化
    #1、初始化应用类型
    project = ['redis','mysql','mangodb']
    for key in project:
        print key
        r.sadd('project',key)
    pro_set = r.smembers('project')
    print pro_set

    #初始化版本库信息
    r.hset("versionLib",'ip','202.5.20.208')
    r.hset('versionLib','hostname','root')
    r.hset('versionLib','path','tools')
    versionLib_dic = r.hgetall('versionLib')
    print versionLib_dic

    #初始化一个应用的基本信息
    r.hset("mysql",'projectPath','tools')
    r.hset('mysql','backupPath','tools/backup')
    r.hset('mysql','projectName','test.war')
    mysql_dic = r.hgetall('mysql')

    #保存
    r.save()