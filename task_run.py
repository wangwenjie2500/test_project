# -*- coding:utf-8 -*-
import subprocess
import json
import re


def powerShellCommand(cmd):
    try:
        args = [r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe',"-ExecutionPolicy","Unrestricted",r"{}".format(cmd)]
        dt = subprocess.Popen(args,stdout=subprocess.PIPE)
        return dt.stdout.read().decode('gb2312').encode('utf-8')
    except Exception,msg:
        print msg

class windows_ShellCommand(object):
    def __init__(self):
        self.data = None

    def CpuInfo(self):
        try:
            cmd = "Get-WmiObject -class win32_processor | Select-Object -Property name,numberofcores,numberoflogicalprocessors,virtualizationfirmwareenabled| ConvertTo-json"
            fh = json.loads(powerShellCommand(cmd))
            if isinstance(fh,dict):
                return [{'physical': 1,'logic':fh['numberofcores'],'type':fh['name']}]
            if isinstance(fh,list):
                cpuinfo = {}
                cpuinfo['physical'] = len(fh)
                cpuinfo['logic'] =  min(list(set([x['numberofcores'] for x in fh])))
                cpuinfo['type'] = list(set(x['name'] for x in fh))[0]
                return [cpuinfo]
        except Exception,msg:
            pass

    def MemoryInfo(self):
        try:
            cmd = "Get-WmiObject -class win32_physicalmemory  | Select-Object -Property  speed,serialnumber,capacity | ConvertTo-json"
            fh = json.loads(powerShellCommand(cmd))
            if isinstance(fh,list):
                return fh
            if isinstance(fh,dict):
                return [fh]
        except Exception,msg:
            print msg

    def OperaInfo(self):
        try:
            cmd = "Get-WmiObject -Class win32_operatingsystem | Select-Object -Property name,serialnumber,numberofusers,version| ConvertTo-json"
            fh = json.loads(powerShellCommand(cmd))
            fh['name'] = fh['name'].split('|')[0]
            cmd = "Get-WmiObject -Class win32_computersystem | Select-Object -Property name | ConvertTo-json"
            p = json.loads(powerShellCommand(cmd))
            fh['hostname'] = p['name']
            return  [fh]
        except Exception,msg:
            print msg

    def MemoryUsage(self):
        try:
            cmd = "Get-WmiObject -Class win32_operatingsystem | Select-Object -Property totalvisiblememorysize,freephysicalmemory| ConvertTo-json"
            fh = json.loads(powerShellCommand(cmd))
            return [{'totalmemory':fh['totalvisiblememorysize'],'freememory':fh['freephysicalmemory']}]
        except Exception,msg:
            pass

    def isAlive(self):
        try:
            return [{'status':0}]
        except Exception,msg:
            pass


class linux_ShellCommand(object):
    def __init__(self):
        self.data = ""

     #获取该节点的CPU情况
    def MemoryUsage(self):
        try:
            mem = []
            meminfo = {}
            with open('/proc/meminfo') as f:
                k = f.readlines()
            for line in k:
                if line == '\n':
                    continue
                if len(line) < 2:
                    continue
                name = line.split(":")[0].rstrip()
                var = line.split(":")[1].rstrip("\n").lstrip(" ")
                meminfo[name] = var
            return [{"totalmemory":meminfo['MemTotal'].rstrip(" kB"),"freememory":meminfo['MemFree'].rstrip(" kB")}]
        except Exception,msg:
            print msg

    def CpuInfo(self):
        try:
            cpu = []
            cpuinfo = {}
            with open('/proc/cpuinfo') as f:
                k = f.readlines()
            for line in k:
                if line == '\n':
                    cpu.append(cpuinfo)
                    cpuinfo = {}
                if len(line) < 2:
                    continue
                name = line.split(":")[0].rstrip()
                var = line.split(":")[1].rstrip("\n").lstrip(" ")
                cpuinfo[name] = var
            cpuTmp = []
            for i in range(len(cpu)):
                cpuinfo = {}
                cpuinfo['coreID'] = cpu[i]['core id']
                cpuinfo['cpuCores'] = cpu[i]['cpu cores']
                cpuinfo['name'] = cpu[i]['model name']
                cpuinfo['physicalID'] = cpu[i]['physical id']
                cpuTmp.append(cpuinfo)
            cpuinfo = {}
            cpuinfo['physical'] = len(set([x['physicalID'] for x in cpuTmp]))
            cpuinfo['logic'] =  len(list(set([x['coreID'] for x in cpuTmp])))
            cpuinfo['type'] = list(set(x['name'] for x in cpuTmp))[0]
            return [cpuinfo]
        except Exception,msg:
            print msg

    def CpuLoadAvg(self):
        try:
            with open('/proc/stat') as f:
                k = f.readline()
            time = 0
            for i in range(2,9):
                time += int(k.split(" ")[i])
            idel = int(k.split(" ")[5])
            iowait = int(k.split(" ")[6])
            return {'idel':idel,'iowait':iowait,'total':time }
        except Exception,msg:
            pass

    def OperaInfo(self):
        try:
            data = self.data
            with open('/etc/redhat-release') as f:
                name = f.read()
            name = name.rstrip(" \n")
            # else:
            #     with open('/etc/issue') as f:
            #         ver = f.read()
            #     name = re.findall('(?<=Welcome to )(.+?)(?= \- Kernel)',ver)
            with open('/proc/version') as f:
                ver = f.read()
            version = re.findall('(?<=Linux version )(.+?)(?= \()',ver)
            with open('/proc/sys/kernel/hostname') as f:
                host = f.read()
            return [{'name':name,'version':version[0],'hostname':host}]
        except Exception,msg:
            pass



    def isAlive(self):
        try:
            return [{'status':0}]
        except Exception,msg:
            pass
