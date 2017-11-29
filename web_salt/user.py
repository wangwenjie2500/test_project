# -*- coding:utf-8 -*-

import hashlib
import dbConnect


class User:
    def __init__(self):
        import Error
        self.Error = Error
        self.dbName = "user_info"
        roleKey = ['role', 'id']
        conn = dbConnect.DBconnect()
        self.roleTable = dict(conn.select(roleKey, table='role_info'))
        conn.__exit__()

    def UserAuth(self, username,password):
        try:
            if self.UserExits(username):
                authPassword = password
                conn = dbConnect.DBconnect()
                passwordAuthList = {"username": username}
                authKey = ['password']
                password = conn.select(authKey,table='user_info',where=passwordAuthList)
                if password:
                    from datetime import datetime
                    loginDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    updateKey = {'last_login':loginDate}
                    whereKey = {'username':username}
                    conn.update(updateKey,table='user_info',where=whereKey)
                    conn.__exit__()
                    return True if hashlib.md5(authPassword).hexdigest() == password[0][0] else False
                else:
                    return False
            else:
                return False
        except Exception,msg:
            print msg

    def UserAdd(self, username, password, role):
        try:
            try:
                if self.UserExits(username):
                    raise self.Error.UserisExits
            except self.Error.UserisExits:
                return "{} is exits".format(username)
            userKey = ['username', 'password', 'role']
            userValue = [username, hashlib.md5(password).hexdigest(), self.roleTable[role]]
            conn = dbConnect.DBconnect()
            conn.insert(dict(zip(userKey, userValue)), table='user_info')
            conn.__exit__()
            return True
        except Exception, msg:
            raise self.Error.UserAddError

    def UserExits(self, username):
        try:
            conn = dbConnect.DBconnect()
            listSelect = ['username']
            valueSelect = {'username': username}
            if conn.select(listSelect, 'user_info', valueSelect):
                conn.__exit__()
                return True
            else:
                conn.__exit__()
                return False
        except Exception, msg:
            raise self.Error.UserExitsError

    def UserDelte(self, username):
        try:
            conn = dbConnect.DBconnect()
            listDelete = {'username' : username}
            conn.delete(table='user_info',where=listDelete)
            conn.__exit__()
        except Exception,msg:
            raise self.Error.UserDeleteError

    def UserChangePassword(self,username,password):
        try:
            conn = dbConnect.DBconnect()
            newPassword = hashlib.md5(password).hexdigest()
            PasswordChangeList = {'password' : newPassword }
            DescChangeList = {'username' : username}
            conn.update(PasswordChangeList,'user_info',DescChangeList)
            conn.__exit__()
        except Exception,msg:
            print msg

    def UserInfoShow(self):
        try:
            conn = dbConnect.DBconnect()
            userKey = ['username','last_login','role']
            userInfo = conn.select(userKey,table='user_info')
            roleInfo = dict(list(conn.select(['id','role'],table='role_info')))
            userList = []
            f = lambda a: {"userName":a[0],"loginDate":a[1],"role":roleInfo[a[2]]}
            for i in userInfo:
                userList.append(f(i))
            return userList
        except Exception,msg:
            pass
