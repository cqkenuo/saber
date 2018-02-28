# -*- coding: utf-8 -*-
__time__ = '2018/2/27 11:03'
__author__ = 'winkyi@163.com'

import sys,os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print base_dir
sys.path.append(base_dir)
reload(sys)

from core import parser


if __name__ == '__main__':
    saber = parser.Saber()
    saber.main()
