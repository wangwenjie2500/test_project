# -*- coding:utf-8 -*-
import socket
import json
import datetime
import sys
import struct
import task_run
import random
import sys
def taskRun(cmd):
    if sys.platform == 'win32':
        t = task_run.windows_ShellCommand()
        setattr(t,"data",cmd['data'])
        fh = getattr(t,cmd['task'])()
        return fh
    elif sys.platform == 'linux2':
        t = task_run.linux_ShellCommand()
        setattr(t,"data",cmd['data'])
        fh = getattr(t,cmd['task'])()
        return fh
if __name__ == "__main__":
    host = ('10.31.29.177',18000)
    sk = socket.socket() #开启一个socket 句柄
    sk.bind(host) #将这个端口和IP进行绑定
    sk.listen(5) #开启监听，最大允许5个连接
    while True:
        try:
            print('server waiting')
            conn,addr = sk.accept()#阻塞这个监听
            print("{} is connection ".format(addr[0]))
            data = json.loads(conn.recv(2048))#将接受的字符串转换成json格式
            now = datetime.datetime.now()
            time = now.strftime("%Y:%m:%d %H:%M:%S")
            print ("start task  {} {}" .format(data,time))
            #.decode('gb2312').encode('utf-8')#执行接受到的命令，并将字符编码从gb2312转换成utf-8
            fh = taskRun(data)
            data = json.dumps({"value":fh}) #将数据封装
            packegeWidth=1200 #定义数据包长度
            packegeId = random.Random().randint(100000,999999)#生成数据包Id
            if sys.getsizeof(data) > packegeWidth: #如果封装的数据包长度大于指定的数据包长度
                dataList = [data[x:x+packegeWidth] for x in range(0,sys.getsizeof(data),packegeWidth)]#将数据包切片
                print ("packge size is {},package number is {},packageId is {} ".format(sys.getsizeof(data),len(dataList),packegeId))
                for i in range(len(dataList)):#循环生成切片数据包
                    header = [packegeId,dataList[i].__len__(),i]#定义数据包头部标签
                    headPack = struct.pack("!3I",*header)#生成二进制流
                    packege = headPack + dataList[i].encode()#将包头和包体拼装
                    print ("send packgeId {} number {} size is {}".format(packegeId,i,sys.getsizeof(packege)))
                    conn.sendall(packege)#发送数据包
            else:
                print ("packge size is {},package number is 1,packageId is {} ".format(sys.getsizeof(data),packegeId))
                header = [packegeId,data.__len__(),0]
                headPack = struct.pack("!3I",*header)
                packege = headPack + data
                conn.sendall(packege)
            # conn.sendall()
            now = datetime.datetime.now()
            time = now.strftime("%Y:%m:%d %H:%M:%S")
            print("run task is finish {}".format(time))
        except Exception,msg:
            pass
        finally:
            conn.close()