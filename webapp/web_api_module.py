#-*- coding:utf-8 -*-
import os
os.chdir('/git_csdn/kvm/src/')
import sys
sys.path.append("..")
import re
from src.dbMgnt import redisMgnt
import json
from src import domain_control
from src import script
from src import disk_control
from src import host_register
import hashlib
from src import task_distribution
import datetime


def checkJsonFormat(raw_msg):
    if isinstance(raw_msg, str):
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False

class host:
    #host register function
    def hostRegister(self,tuple):
        try:
            str = tuple
            type = re.findall("(?<=\&)(.+?)(?=\&)", str)[0].split('=')[1]
            if type == 'register':
                bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
                key = {}
                for i in bd:
                    ti = i.split('=')
                    key[ti[0]] = "'{}'".format(ti[1])
                rcode = host_register.hostRegister(key['client'])
                if rcode == 200:
                    return {'code' : 200}
            if type == 'delete':
                bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
                key = {}
                for i in bd:
                    ti = i.split('=')
                    key[ti[0]] = "'{}'".format(ti[1])
                rcode = host_register.hostDelete(key['UUID'])
                if rcode == 200:
                    return {'code':200}
        except Exception,msg:
            print(msg)
            return {"error": 452}

    #host list
    def hostSelect(self,tuple):
        try:
            str = tuple
            type = re.findall("(?<=\&)(.+?)(?=\&)", str)[0].split('=')[1]
            if type == 'all':
                cod = re.findall("(?<=\%)(.+?)(?=\%)", str)
                k = redisMgnt().control(type='select', Dict=cod, table='host_nodeinfo')
                fk = []
                for i in k:
                    tmp = []
                    for m in range(len(i)):
                        if checkJsonFormat(i[m]):
                            g = json.loads(i[m])
                            tmp.append(g)
                        else:
                            tmp.append(i[m])
                    fd = dict(zip(cod, tmp))
                    fk.append(fd)
                return fk
            if type == 'only':
                cod = re.findall("(?<=\%)(.+?)(?=\%)", str)
                bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
                key = {}
                # sheng cheng where zi duan
                for i in bd:
                    ti = i.split('=')
                    key[ti[0]] = "'{}'".format(ti[1])
                k = redisMgnt().control(type='select', Dict=cod, table='host_nodeinfo', Where=key)[0]
                tmp = []
                for m in range(len(k)):
                    if checkJsonFormat(k[m].encode('utf-8')):
                        g = json.loads(k[m])
                        tmp.append(g)
                    else:
                        tmp.append(k[m])
                fd = dict(zip(cod, tmp))
                return fd
        except Exception,msg:
            print(msg)
            return {"error":452}



class domain:
    def domainControl(self,tuple):
        try:
            str = tuple
            #get num zi duan de zhi
            type = re.findall("(?<=\&)(.+?)(?=\&)", str)[0].split('=')[1]
            if type == 'all':
                cod = re.findall("(?<=\%)(.+?)(?=\%)", str)
                k = redisMgnt().control(type='select', Dict=cod, table='domain_machineinfo')
                fk = []
                for i in k:
                    tmp = []
                    for m in range(len(i)):
                        if checkJsonFormat(i[m]):
                            g = json.loads(i[m])
                            tmp.append(g)
                        else:
                            tmp.append(i[m])
                    fd = dict(zip(cod, tmp))
                    fk.append(fd)
                return fk
            if type == 'only':
                cod = re.findall("(?<=\%)(.+?)(?=\%)", str)
                bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
                key = {}
                # sheng cheng where zi duan
                for i in bd:
                    ti = i.split('=')
                    key[ti[0]] = "'{}'".format(ti[1])
                k = redisMgnt().control(type='select', Dict=cod, table='domain_machineinfo', Where=key)[0]
                tmp = []
                for m in range(len(k)):
                    if checkJsonFormat(k[m].encode('utf-8')):
                        g = json.loads(k[m])
                        tmp.append(g)
                    else:
                        tmp.append(k[m])
                fd = dict(zip(cod, tmp))
                return fd


        except Exception,msg:
            pass
    def domainCrontolInfo(self,tuple):
        try:
            str = tuple
            # get num zi duan de zhi
            type = re.findall("(?<=\&)(.+?)(?=\&)", str)[0].split('=')[1]
            bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
            key = {}
            for i in bd:
                key[i.split("=")[0].encode('utf-8')] = i.split("=")[1].encode('utf-8')
            if type == 'createMachine':
                f = domain_control.createMachine(data=key)
                return f
            else:
                f = domain_control.domain_crontrol_function(ACTION=type,UUID=key['UUID'])
                return f
        except Exception,msg:
            print(msg)


    def domainFlush(self,tuple):
        try:
            str = tuple
            type = re.findall("(?<=\&)(.+?)(?=\&)", str)[0].split('=')[1]
            if type == 'allDomain':
                return  domain_control.domain_control_refer(num='all')
            elif type == 'onlyDomain':
                cod = re.findall("(?<=\$)(.+?)(?=\$)", str)[0]
                UID = cod.split("=")[1]
                return domain_control.domain_control_refer(num='only',UUID=UID)
            elif type == 'onlyHost':
                cod = re.findall("(?<=\$)(.+?)(?=\$)", str)[0]
                UID = cod.split("=")[1]
                return domain_control.domain_control_refer(num='onlyHost', UUID=UID)
            elif type == 'allCheck':
                return domain_control.domain_control_monitor(num='all')
            elif type == 'onlyCheck':
                cod = re.findall("(?<=\$)(.+?)(?=\$)", str)[0]
                UID = cod.split("=")[1]
                return domain_control.domain_control_monitor(num='only',UUID=UID)
            elif type == 'vncinfo':
                return script.nodeVncPort()
            elif type == 'vncToken':
                return script.vncConfig()
            elif type == 'networkTarget':
                return script.networkTargetUseCheck()
        except Exception,msg:
            print(msg)
            return {"error": 452}



class disk:
    def __init__(self):
        pass
    def diskControl(self,tuple):
        try:
            str = tuple
            type = re.findall("(?<=\&)(.+?)(?=\&)", str)[0].split('=')[1]
            if type == 'all':
                cod = re.findall("(?<=\%)(.+?)(?=\%)", str)
                k = redisMgnt().control(type='select', Dict=cod, table='disk_diskregister')
                fk = []
                for i in k:
                    tmp = []
                    for m in range(len(i)):
                        if checkJsonFormat(i[m]):
                            g = json.loads(i[m])
                            tmp.append(g)
                        else:
                            tmp.append(i[m])
                    fd = dict(zip(cod, tmp))
                    fk.append(fd)
                return fk
            elif type == 'only':
                cod = re.findall("(?<=\%)(.+?)(?=\%)", str)
                bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
                key = {}
                # sheng cheng where zi duan
                for i in bd:
                    ti = i.split('=')
                    key[ti[0]] = "'{}'".format(ti[1])
                k = redisMgnt().control(type='select', Dict=cod, table='disk_diskregister', Where=key)[0]
                tmp = []
                for m in range(len(k)):
                    if checkJsonFormat(k[m].encode('utf-8')):
                        g = json.loads(k[m])
                        tmp.append(g)
                    else:
                        tmp.append(k[m])
                fd = dict(zip(cod, tmp))
                return fd
            if type == 'create':
                bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
                key = {}
                # sheng cheng where zi duan
                for i in bd:
                    ti = i.split('=')
                    key[ti[0]] = "{}".format(ti[1])
                rcode = disk_control.diskCreate(name=key['name'],size=key['size'])
                if rcode == 200:
                    return {'code' : 200}
            if type == 'delete':
                bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
                key = {}
                # sheng cheng where zi duan
                for i in bd:
                    ti = i.split('=')
                    key[ti[0]] = "{}".format(ti[1])
                rcode = disk_control.diskDelete(UUID=key['UUID'])
                if rcode == 200:
                    return {'code' : 200}
                else:
                    return {'error' : 452}
            if type == 'resize':
                bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
                key = {}
                # sheng cheng where zi duan
                for i in bd:
                    ti = i.split('=')
                    key[ti[0]] = "{}".format(ti[1])
                rcode = disk_control.diskResize(UUID=key['UUID'],size=key['size'])
                if rcode == 200:
                    return {'code' : 200}
                else:
                    return rcode
        except Exception,msg:
            return {"error": 452}

class image:
    def __init__(self):
        pass

    def imageControl(self,tuple):
        try:
            str = tuple
            type = re.findall("(?<=\&)(.+?)(?=\&)", str)[0].split('=')[1]
            if type == 'all':
                cod = re.findall("(?<=\%)(.+?)(?=\%)", str)
                k = redisMgnt().control(type='select', Dict=cod, table='imageregister')
                fk = []
                for i in k:
                    tmp = []
                    for m in range(len(i)):
                        if checkJsonFormat(i[m]):
                            g = json.loads(i[m])
                            tmp.append(g)
                        else:
                            tmp.append(i[m])
                    fd = dict(zip(cod, tmp))
                    fk.append(fd)
                return fk
            elif type == 'only':
                cod = re.findall("(?<=\%)(.+?)(?=\%)", str)
                bd = re.findall("(?<=\$)(.+?)(?=\$)", str)
                key = {}
                # sheng cheng where zi duan
                for i in bd:
                    ti = i.split('=')
                    key[ti[0]] = "'{}'".format(ti[1])
                k = redisMgnt().control(type='select', Dict=cod, table='imageregister', Where=key)[0]
                tmp = []
                for m in range(len(k)):
                    if checkJsonFormat(k[m].encode('utf-8')):
                        g = json.loads(k[m])
                        tmp.append(g)
                    else:
                        tmp.append(k[m])
                fd = dict(zip(cod, tmp))
                return fd
        except Exception,msg:
            print(msg)
class auth:
    def __init__(self):
        pass

    def user_auth(self,kwargs):
        try:
            user = kwargs['username']
            password = hashlib.md5(kwargs['password']).hexdigest()
            conn = redisMgnt()
            alist = conn.control(type='select', Dict=['password'], table='userinfo',
                                        Where={'user': "'{}'".format(user)})[0][0]
            alist = alist.encode('utf-8')
            if alist:
                if password == alist:
                    now = datetime.datetime.now()
                    time = now.strftime('%Y-%m-%d %H:%M:%S')
                    conn.control(type='update',Dict={"lastlogin":"'{}'".format(time)},table='userinfo',Where={'user':"'{}'".format(user)})
                    conn.__exit__()
                    print {'type': 'user-Auth', 'status': 'ok', 'user': user, 'des': 'login ok'}
                    return {'code': 200}
                else:
                    print {'type': 'user-Auth', 'status': 'faild', 'user': user, 'des': 'user password is error'}
                    return {'code':201}
            else:
                print {'type':'user-Auth','status':'faild','user': user,'des':'user is not found'}
                return {'code': 201}
        except Exception,msg:
            print {'type': 'user-Auth', 'status': 'faild', 'des': 'error wei zhi'}
            return {'error':451}

class crontrol(object):
    def __init__(self):
        self.data = None
    def userAdd(self):
        user = self.data['username']
        try:
            password = self.data['password']
            rcode = script.userRegister(type='add',user=user,password=password)
            print {'type': 'user-Add', 'status': 'ok', 'user': user, 'des': 'add ok',
                   'module': 'api-crontrol-userAdd'}
            return rcode
        except Exception:
            print {'type': 'user-Add', 'status': 'ok', 'user': user, 'des': 'add faild',
                   'module': 'api-crontrol-userAdd'}
            return {'code' : 451}
    def userDel(self):
        try:
            user = self.data['username']
            rcode = script
        except Exception:
            return {'code' : 451}

    def userAuth(self):
        user = self.data['username']
        try:
            print user
            conn = redisMgnt()
            password = hashlib.md5(self.data['password']).hexdigest()
            alist = conn.control(type='select', Dict=['password'], table='userinfo',
                                        Where={'user': "'{}'".format(user)})[0][0]
            alist = alist.encode('utf-8')
            if alist:
                if password == alist:
                    now = datetime.datetime.now()
                    time = now.strftime('%Y-%m-%d %H:%M:%S')
                    conn.control(type='update', Dict={"lastlogin": "'{}'".format(time)}, table='userinfo',
                                 Where={'user': "'{}'".format(user)})
                    conn.__exit__()
                    print {'type': 'user-Auth', 'status': 'ok', 'user': user, 'des': 'login ok','module':'api-crontrol-userAuth'}
                    return {'code': 200}
                else:
                    print {'type': 'user-Auth', 'status': 'faild', 'user': user, 'des': 'user password is error','module':'api-crontrol-userAuth'}
                    return {'code':201}
            else:
                print {'type':'user-Auth','status':'faild','user': user,'des':'user is not found','module':'api-crontrol-userAuth'}
                return {'code': 201}
        except Exception,msg:
            print {'type': 'user-Auth', 'status': 'faild', 'user': user, 'des': 'user is not found','module':'api-crontrol-userAuth'}
            return {'error':451}


    def instanceMangntAll(self):
        try:

            DomainInfo = {}
            DomainList = [ x[0] for x in redisMgnt().control(type='select',Dict=['UUID'],table='domain_machineinfo')]
            for i in DomainList:
                DomainInfo[i] = domain_control.domainInfo(UUID=i)
            print({'status':'ok','des':'get ok','type':'domaininfo','module':'api-web_api_module-instanceMangntAll'})
            return DomainInfo
        except Exception:
            pass
    def diskMangntAll(self):
        try:
            DiskInfo = {}
            DomainList = [ x[0] for x in redisMgnt().control(type='select',Dict=['UUID'],table='disk_diskregister')]
            for i in DomainList:
                DiskInfo[i] = disk_control.diskInfo(UUID=i)
            return DiskInfo
        except Exception,msg:
            print(msg)
            pass

    def selectDomainAll(self):
        try:
            data = self.data['data']
            k = redisMgnt().control(type='select', Dict=data, table='domain_machineinfo')
            fk = []
            for i in k:
                tmp = []
                for m in range(len(i)):
                    if checkJsonFormat(i[m]):
                        g = json.loads(i[m])
                        tmp.append(g)
                    else:
                        tmp.append(i[m])
                fd = dict(zip(data, tmp))
                fk.append(fd)
            print {'type': 'SeletDomainAll', 'status': 'ok','user':'all' ,'des': 'get ok',
                   'module': 'api-crontrol-DomainDetailViews'}
            return fk
        except Exception,msg:
            return {'error' : 451}

    def instanceCrontrol(self):
        try:
            data = self.data['data']
            rcode = domain_control.domain_crontrol_function(UUID=data['UUID'],ACTION=data['action'])
            return rcode
        except Exception,msg:
            return {'error' : 451}

    def infoRefer(self):
        try:
            data = self.data['data']
            if data['type'] == 'diskAllRefer':
                recode = disk_control.diskUseCheck()
                print(recode)
                print({'status': 'ok', 'des': 'get ok', 'type': 'diskinfo', 'module': 'api-web_api_module-infoRefer'})
                return recode
        except Exception,msg:
            return {'error' : 451}


    def clusterMangntAll(self):
        try:
            _tmp = {}
            for i in  [x for x in redisMgnt().control(type='select',Dict=['UUID','nodeSTATUS','nodeMem','nodeSysVersion','nodeCpu','nodeIP','nodeCpuVersion','hostname'],table='host_nodeinfo')]:
                _tmp[i[0]] = {
                    "status" : int(i[1]),
                    "memory" : int(i[2]),
                    "systemOS" : i[3],
                    "cpu" : int(i[4]),
                    "ip" : i[5],
                    "cpuVersion" : i[6],
                    "hostname" : i[7],
                    "uuid" : i[0]
                }
            return _tmp
        except Exception,msg:
            return {'error' : 451}

    def getInstanceCreateInfo(self):
        try:
            _tmp = {}
            _a = {}
            conn = redisMgnt()
            aliveHost = conn.control(type="select",Dict=['UUID','nodeIP'],table='host_nodeinfo',Where={'nodeSTATUS':"'0'"})
            for i in aliveHost:
                _a[i[0]] = i[1]
            _tmp['inHost'] = _a
            aliveDisk = conn.control(type="select",Dict=['UUID','image'],table='disk_diskregister',Where={'st':"'N'"})
            for i in aliveDisk:
                _a[i[0]] = i[1]
            _tmp['Disk'] = _a

        except Exception,msg:
            print(msg)
            return {'error' : 451}

    def getResourceNumber(self):
        try:
            conn = redisMgnt()
            instanceNumberAlive = int(conn.control(type="select",Dict=['count(*)'],table='domain_machineinfo',Where={'rStatus':"'1'"})[0][0])
            instanceNumberFaild = int(conn.control(type="select",Dict=['count(*)'],table='domain_machineinfo',Where={'rStatus':"'0'"})[0][0])
            nodeNumberAlive = int(conn.control(type="select",Dict=['count(*)'],table='host_nodeinfo',Where={'nodeSTATUS':"'0'"})[0][0])
            nodeNumberFaild = int(conn.control(type="select",Dict=['count(*)'],table='host_nodeinfo',Where={'nodeSTATUS':"'1'"})[0][0])
            return {'instanceAlive' : instanceNumberAlive,'instanceFaild':instanceNumberFaild,'nodeAlive':nodeNumberAlive,'nodeFaild':nodeNumberFaild}
        except Exception,msg:
            print(msg)
            return {'error' : 451}

    def getResourceImage(self):
        try:
            conn = redisMgnt()
            imageList = conn.control(type="select",Dict=['UUID','image'],table='imageregister')
            conn.__exit__()
            _tmp = {}
            for i in imageList:
                _tmp[i[0]] = i[1]
            return _tmp
        except Exception,msg:
            return {'error' : 451}

    def ejectInstanceCdrom(self):
        try:
            data =self.data['data']
            UUID = data['UUID']
            return domain_control.domainEjectCdrom(UUID=UUID,ACTION='eject')
        except Exception,msg:
            return {'error' : 451}

    def mountInstanceCdrom(self):
        try:
            data = self.data['data']
            UUID = data['UUID']
            CDUUID = data['CDUUID']
            recode = domain_control.domainEjectCdrom(UUID=UUID, ACTION='mount', CDUUID=CDUUID)
            if recode['code'] == '200':
                domain_control.domain_control_refer(num='only',UUID=UUID)
            return recode
        except Exception,msg:
            return {'error':451}

    def UserControl(self):
        try:
            data = self.data['data']
            if data['type'] == 'show':
                rcode = script.userRegister(type='show')
                return rcode
        except Exception,msg:
            return {'error':451}


    def createMachineUse(self):
        try:
            _tmp = {}
            conn = redisMgnt()
            AliveHost =  conn.control(type="select",Dict=['UUID','nodeIP'],table='host_nodeinfo',Where={'nodeSTATUS':"0"})
            a,b = [ x[0] for x in AliveHost ],[ x[1] for x in AliveHost ]
            _tmp['host'] = dict(zip(a,b))
            AliveDisk = conn.control(type="select",Dict=['UUID','image'],table='disk_diskregister',Where={'st':"'N'"})
            a,b = [ x[0] for x in AliveDisk],[ x[1] for x in AliveDisk]
            _tmp['disk'] = dict(zip(a,b))
            AliveImage = conn.control(type="select",Dict=['UUID','image'],table='imageregister')
            a,b = [ x[0] for x in AliveImage],[ x[1] for x in AliveImage]
            _tmp['image'] = dict(zip(a,b))
            AliveNetwork = conn.control(type="select",Dict=['UUID','network'],table='network')
            _tmp['network'] = {k[0] : k[1] for k in AliveNetwork }
            conn.__exit__()
            return _tmp
        except Exception,msg:
            return {'error' : 451}

    def isIntanceExits(self):
        try:
            data = self.data['data']
            conn = redisMgnt()
            return {'code': "Y" if data['name'] in [ x[0] for x in conn.control(type='select',Dict=['vName'],table='domain_machineinfo')] else "N" }
        except Exception,msg:
            return {'error' : 451}
        finally:
            conn.__exit__()

    def createMachine(self):
        try:
            data = self.data['data']
            print data
            return {'code': 200}
        except Exception,msg:
            return {'error':451}

    def NodeConnectTest(self):
        try:
            data = self.data['data']
            fh = task_distribution.task_distribution(Task={"task":"isAlive","data":{}},ip=data['address'])
            if fh != 450:
                if fh['value'][0]['status'] == 0:
                    return {'code' : 200}
            else:
                return {'code' : 451}
        except Exception,msg:
            print msg
            return {'code':451}

    def NodeAdd(self):
        try:
            data = self.data['data']
            fh = task_distribution.task_distribution({'task':'isAlive','data':{}}, data['ip'])
            if fh != 450 and  fh['value'][0]['status'] == 0:
                return {'code': host_register.host_register(data['ip'],data['info'],data['type'])}
        except Exception,msg:
            return {'code' : 451}