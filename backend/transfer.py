# -*- coding: utf-8 -*-
__time__ = '2018/3/5 17:01'
__author__ = 'winkyi@163.com'

import paramiko


host = "202.5.20.208"
port = 22
timeout = 30
user = "root"
password = "!@cwq8898859"


#Paramiko远程执行linux命令
def sftp_exec_command(command):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, 22, user, password)
        std_in, std_out, std_err = ssh_client.exec_command(command)
        for line in std_out:
            print line.strip("\n")
        ssh_client.close()
    except Exception, e:
        print e


#Paramiko上传文件
def sftp_upload_file(server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
    except Exception, e:
        print e


#Paramiko下载文件
def sftp_down_file(server_path, local_path):
    try:
        t = paramiko.Transport((host, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
    except Exception, e:
        print e


if __name__ == '__main__':
    host = "202.5.20.208"
    port = 22
    timeout = 30
    user = "root"
    password = "!@cwq8898859"

    sftp_exec_command("ls -l")
    sftp_upload_file("/root/tools/data1.txt", "D:/data/data1.txt")
    sftp_down_file("/root/tools/aabbccdd.txt", "D:/data/aabbccdd.txt")

