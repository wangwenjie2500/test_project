# -*- coding:utf-8 -*-
import MySQLdb
import os
import yaml
import Error


class DBconnect:
    def __init__(self):
        #path = os.environ['saltpath']
        path = '/git_csdn/kvm/src/web_salt/conf/salt.conf'
        if os.path.exists(path):
            with open(path) as file:
                k = file.read()
            config = yaml.load(k)['mysql']
            self.conn = MySQLdb.connect(config['ip'], config['user'], config['password'], config['database'],
                                        charset="utf8")
        else:
            raise Error.FileNotFoundError

    def __exit__(self):
        self.conn.close()

    def insert(self,Dict=None,table=None):
        try:
            if not Dict or not table:
                raise Error.SQLKeyError
            k = ",".join(map(lambda x: x, Dict))
            v = ",".join(map(lambda x: "'" + Dict[x] + "'", Dict))
            self.conn.cursor().execute("insert into {} ({}) values ({}) ".format(table, k, v))
            self.conn.commit()
        except Exception,msg:
            raise Error.SQLInsertSQLError

    def select(self,Dict=None,table=None,where=None):
        try:
            if not Dict or not table:
                raise Error.SQLKeyError
            if where:
                aK = [x for x in Dict]
                str = ",".join(map(lambda x: x, aK))
                wK = [x for x in where.keys()]
                wV = [where[m] for m in wK]
                str2 = ",".join(map(lambda x, y: x + "=" + "'" + y + "'", wK, wV))
                cursor = self.conn.cursor()
                #print("select {} from {} where {}".format(str, table, str2))
                cursor.execute("select {} from {} where {}".format(str, table, str2))
            else:
                aK = [x for x in Dict]
                str = ",".join(map(lambda x: x, aK))
                cursor = self.conn.cursor()
                cursor.execute("select {} from {}".format(str, table))
            data = cursor.fetchall()
            return data
        except Exception,msg:
            raise  Error.SQLSelectSQLError

    def update(self,Dict=None,table=None,where=None):
        try:
            if not Dict or not table or not where:
                raise Error.SQLKeyError
            g = lambda x, y: x + "=" + "'" + y + "'"
            aK = [x for x in Dict.keys()]
            aV = [Dict[m] for m in aK]
            str = ",".join(map(g, aK, aV))
            wK = [x for x in where.keys()]
            wV = [where[m] for m in wK]
            str2 = ",".join(map(g,wK,wV))
            cursor = self.conn.cursor()
            cursor.execute("update {} set {} where {}".format(table, str, str2))
            self.conn.commit()
        except Exception,msg:
            raise Error.SQLUpdateSQLError

    def delete(self,table=None,where=None):
        try:
            if not table:
                raise Error.SQLKeyError
            if not where:
                self.conn.cursor().execute("delete from {}".format(table))
                self.conn.commit()
            else:
                g = lambda x, y: x + "=" + "'" + y + "'"
                wK = [x for x in where.keys()]
                wV = [where[m] for m in wK]
                str2 = ",".join(map(g, wK, wV))
                #print("delete from {} where {}".format(table,str2))
                self.conn.cursor().execute("delete from {} where {}".format(table, str2))
                self.conn.commit()
        except Exception,msg:
          raise Error.SQLDeleteSQLError

