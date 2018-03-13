# -*- coding: utf-8 -*-
__time__ = '2018/3/5 17:11'
__author__ = 'winkyi@163.com'

import sys
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class MyCrypt():
    def __init__(self):
        #密钥秘钥信息
        self.key = '0000000000000000'
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        length = 16
        count = len(text)
        if count < length:
            add = length - count
            text= text + ('\0' * add)

        elif count > length:
            add = (length -(count % length))
            text= text + ('\0' * add)

        # print len(text)
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        self.ciphertext = cryptor.encrypt(text)
        return b2a_hex(self.ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'0000000000000000')
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

if __name__ == '__main__':
    mycrypt = MyCrypt()
    e = mycrypt.encrypt('xm123456')
    d = mycrypt.decrypt(e)
    print e
    print d