#-*-coding:utf-8-*-
import urllib
import urllib2
import time
import json


url = "http://192.168.32.23:8085/api/v0.1/crontrol"
def post(data):
    fullurl = url
    print(fullurl)
    req = urllib2.Request(fullurl,data)
    res = urllib2.urlopen(req)
    rdata = res.read()
    return  rdata

class crontrol(object):
    def __init__(self):
        pass

    def userAuth(self,**kwargs):
        user = kwargs['username']
        try:
            password = kwargs['password']
            data = json.dumps({'type':"userAuth","username":user,"password":password})
            recode = json.loads(post(data=data))
            print({'action': 'login', 'user': '{}'.format(user), 'status': 'ok', 'module': 'userAuth'})
            return recode
        except Exception,msg:
            print(msg)
            print({'action':'login','user':'{}'.format(user),'status':'error','module':'userAuth'})

    def instanceMangnt(self):
        try:
            data = json.dumps({"type":"instanceMangntAll"})
            recode = json.loads(post(data))
            f = []
            for i in recode.keys():
                f.append(recode[i])
            print({'action': 'get instance info', 'user': 'all', 'status': 'ok', 'module': 'instanceMangnt'})
            return f
        except Exception,msg:
            pass

    def diskMangnt(self):
        try:
            data = json.dumps({"type":"diskMangntAll"})
            recode = json.loads(post(data))
            f = []
            for i in recode.keys():
                recode[i]['UUID'] = i
                f.append(recode[i])
            print({'action': 'get disk info', 'user': 'all', 'status': 'ok', 'module': 'diskMangntMangnt'})
            return f
        except Exception,msg:
            pass

    def clusterMangnt(self):
        try:
            data = json.dumps({"type":"clusterMangntAll"})
            recode = json.loads(post(data))
            f = []
            for i in recode.keys():
                recode[i]['UUID'] = i
                f.append(recode[i])
            print({'action': 'get cluster info', 'user': 'all', 'status': 'ok', 'module': 'clusterMangntMangnt'})
            return f
        except Exception,msg:
            pass

    def instanceIscdRom(self):
        try:
            data = json.dumps({"type":"instanceIscdRom"})
            recode = json.loads(post(data))
        except Exception,msg:
            pass
    def userShow(self):
        try:
            value = json.dumps({"type":"UserControl","data":{"type":"show"}})
            m = post(data=value)
            print({'action': 'get user info', 'user': 'all', 'status': 'ok', 'module': 'userShow'})
            return json.loads(m)
        except Exception,msg:
            return {'code' : '451'}

    def getDomianConfig(self):
        try:
            data = json.dumps({"type":"getDomainConfig"})
            m = post(data)
            return json.loads(m)
        except Exception,msg:
            return {'code' : '451'}

    def getCreateDomainInfo(self):
        try:
            data = json.dumps({"type" : "createMachineUse"})
            m = post(data)
            return json.loads(m)
        except Exception,msg:
            return {'code' : '451'}

    def clusterNodeResourceInformation(self):
        try:
            pass
        except Exception,msg:
            pass