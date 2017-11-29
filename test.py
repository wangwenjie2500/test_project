# -*- coding:utf-8 -*-
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
    var = line.split(":")[1].rstrip("\n")
    cpuinfo[name] = var
cpuTmp = []
for i in range(len(cpu)):
    for k in cpu[i].keys():
        cpuinfo = {}
        cpuinfo['coreID'] = cpu[i]['core id']
        cpuinfo['cpuCores'] = cpu[i]['cpu cores']
        cpuinfo['mode'] = cpu[i]['model name']
        cpuinfo['cache'] = cpu[i]['cache size']
        cpuinfo['physicalID'] = cpu[i]['physical id']
        cpuTmp.append(cpuinfo)
cpuinfo = {}
cpuinfo['physical'] = len(set([x['physicalID'] for x in cpuTmp]))
cpuinfo['logic'] =  len(list(set([x['coreID'] for x in cpuTmp])))
cpuinfo['cache'] = int(list(set(x['cache'] for x in cpuTmp))[0].lstrip(' ').rstrip(' KB'))
cpuinfo['type'] = list(set(x['mode'] for x in cpuTmp))[0]
print(cpuinfo)