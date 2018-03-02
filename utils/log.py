# -*- coding: utf-8 -*-
__time__ = '2018/2/28 14:47'
__author__ = 'winkyi@163.com'

import logging
import sys
import os
import utils

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_path = 'logs'
log_name = 'saber.log'
logLevel = 'debug'

class Log(object):
    def __init__(self):

        # 获取logger实例，如果参数为空则返回root logger
        self.logger = logging.getLogger()
        log_level_map = {'debug':logging.DEBUG,'info':logging.INFO,'warning':logging.WARNING,'error':logging.ERROR}
        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')


        if utils.isLinux():
           logfile = "%s/%s/%s" %(base_dir,log_path,log_name)
        else:
           logfile = "%s\\%s\\%s" %(base_dir,log_path,log_name)

        if not self.logger.handlers:
            # 文件日志
            file_handler = logging.FileHandler(logfile)
            file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

            # 控制台日志
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.formatter = formatter  # 也可以直接给formatter赋值

            # 为logger添加的日志处理器
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

            # 指定日志的最低输出级别，默认为WARN级别
            self.logger.setLevel(log_level_map[logLevel])

    def debug(self,message):
      self.logger.debug(message)

    def info(self,message):
      self.logger.info(message)

    def error(self,message):
      self.logger.error(message)

    def warning(self,message):
      self.logger.warning(message)

    def exception(self,message):
      self.logger.exception (message)


if __name__ == '__main__':
     logger = Log()
     logger.error('error~')
     logger.debug('debug')

     try:
          1/0
     except:
          logger.exception('exception')