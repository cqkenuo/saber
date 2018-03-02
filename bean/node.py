# -*- coding: utf-8 -*-
__time__ = '2018/3/1 14:38'
__author__ = 'winkyi@163.com'


class Node(object):

    def __init__(self,id,nodeName,nodeJoinTime,nodeLastTime,online,st):
        self.id = id
        self.nodeName = nodeName
        self.nodeJoinTime = nodeJoinTime
        self.nodeLastTime = nodeLastTime
        self.online = online
        self.st = st

