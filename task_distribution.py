# -*- coding:utf-8 -*-
import socket
import json
import struct
def task(cmd,ip):
    try:
        dataBuffer = []
        headerSize = 12
        host = (ip, 18000)
        conn = socket.socket()
        conn.settimeout(40)
        try:
            conn.connect(host)
        except Exception,msg:
            return 450
        conn.sendall(cmd)
        f = True
        while f:
            fh = conn.recv(2048)
            if fh:
                dataBuffer.append(fh)
            else:
                f = False
        conn.close()
        str = ""
        for i in dataBuffer:
            headPack = struct.unpack('!3I', i[:headerSize])
            id = headPack[0]
            packageWidth = headPack[1]
            packageOrder = headPack[2]
            str += i[headerSize:headerSize + packageWidth]
        return str
    except Exception, msg:
        print msg

def task_distribution(Task,ip):
    cmd = json.dumps(Task)
    rd = task(cmd=cmd,ip=ip)
    if rd != 450:
        return json.loads(rd)
    else:
        return 450