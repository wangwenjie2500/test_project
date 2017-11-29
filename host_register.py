# -*- coding:utf-8 -*-
from src import domain_opera as dom
import re
import pexpect
import script
import logging
import dbMgnt
import task_distribution as task

def host_register(*args):
    try:
        host = args[0]
        memory = task.task_distribution({'task':'MemoryUsage','data':{}},host)
        cpu = task.task_distribution({'task':'CpuInfo','data':{}},host)
        operainfo = task.task_distribution({'task':'OperaInfo','data':{}},host)
        memory,cpu,operainfo = memory['value'][0],cpu['value'][0],operainfo['value'][0]
        info = args[1]
        virType = args[2]
        id = script.random_str(36)
        nodeRegInfo = {
            "nodeIP": "'{}'".format(host),
            "nodeSTATUS": "0",
            "nodeMem": "{}".format(int(memory['totalmemory']) / 1024),
            "nodeCpu": "{}".format(cpu['physical']),
            "nodeCpuVersion": "'{}'".format(cpu['type']),
            "nodeKernelVersion": "'{}'".format(operainfo['version']),
            "nodeKenrelJ": "'{}'".format('None'),
            "nodeSysVersion": "'{}'".format(operainfo['name']),
            "UUID": "'{}'".format(id),
            "virtype" : "'{}'".format(virType),
            "hostname":"'{}'".format(operainfo['hostname']),
            "info" : "'{}'".format(info)
        }
        conn = dbMgnt.redisMgnt()
        f = conn.control(type='insert',Dict=nodeRegInfo,table='host_nodeinfo')
        conn.__exit__()
        return f
    except Exception,msg:
        print msg


def hostDelete(host):
    try:
        f = dbMgnt.redisMgnt().control(type='delete',table='host_nodeinfo',Where={'UUID':"{}".format(host)})
        return f
    except Exception,msg:
        print(msg)


def hostNodeRefer():
    try:
        pass
    except Exception,msg:
        pass
