# -*- coding:utf-8 -*-
# create time : 2017 6 30
#this scripts is self.conn database
import MySQLdb
import ConfigParser
import os
import logging
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='myapp.log',
                filemode='w')
class redisMgnt:
    def __init__(self):
        cf = ConfigParser.ConfigParser()
        path = os.environ.get('VIRT_BASE_PATH')
        cf.read("/git_csdn/kvm/src/global.conf")
        self.host = cf.get('mysql','db_host')
        self.user = cf.get('mysql','db_user')
        self.password = cf.get('mysql','db_password')
        self.db = cf.get('mysql','db_name')
        self.conn =  MySQLdb.connect(self.host, self.user, self.password, self.db, charset="utf8")
        #self.db = 'cloudstack'

    def __exit__(self):
        self.conn.close()


    def control(self,type=None,Dict=None,table=None,Where=None):
        try:
            if type == "update":
                g = lambda x,y: x + "=" + y
                aK = [ x for x in Dict.keys() ]
                aV = [Dict[m] for m in aK ]
                str = ",".join(map(g,aK,aV))
                wK = [ x for x in Where.keys() ]
                wV = [Where[m] for m in wK ]
                str2 = ",".join(map(g,wK,wV))
                cursor = self.conn.cursor()
                #print("update {} set {} where {}".format(table,str,str2))
                cursor.execute("update {} set {} where {}".format(table,str,str2))
                self.conn.commit()
                return 200
            if type == "select":
                if Where:
                    aK = [ x for x in Dict]
                    str = ",".join(map(lambda x: x,aK))
                    wK = [x for x in Where.keys()]
                    wV = [Where[m] for m in wK]
                    str2 = ",".join(map(lambda x,y:x + "=" + y, wK, wV))
                   # print("select {} from {} where {}".format(str,table,str2))
                    cursor = self.conn.cursor()
                    cursor.execute("select {} from {} where {}".format(str,table,str2))
                else:
                    aK = [x for x in Dict]
                    str = ",".join(map(lambda x: x, aK))
                    cursor = self.conn.cursor()
                   # print("select {} from {}".format(str,table))
                    cursor.execute("select {} from {}".format(str,table))
                k = cursor.fetchall()
                return k
            if type == "insert":
                k = ",".join(map(lambda x:x,Dict))
                v = ",".join(map(lambda x:Dict[x],Dict))
                print("insert into {} ({}) values ({})".format(table,k,v))
                self.conn.cursor().execute("insert into {} ({}) values ({}) ".format(table,k,v))
                self.conn.commit()
                return 200
            if type == "delete":
                if Where:
                    g = lambda x, y: x + "=" + y
                    wK = [x for x in Where.keys()]
                    wV = [Where[m] for m in wK]
                    str2 = ",".join(map(g, wK, wV))
                   # print("delete from {} where {}".format(table,str2))
                    self.conn.cursor().execute("delete from {} where {}".format(table,str2))
                    self.conn.commit()
                    return 200
                else:
                    # print("delete from {}".format(table))
                    self.conn.cursor().execute("delete from {}".format(table))
                    self.conn.commit()
                    return 200
        except Exception,msg:
            print(msg)