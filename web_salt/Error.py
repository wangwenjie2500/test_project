# -*- coding:utf-8 -*-
class Error(Exception):
    pass

class FileNotFoundError(Error):
    pass

class SQLKeyError(Error):
    pass

class SQLInsertSQLError(Error):
    pass

class SQLSelectSQLError(Error):
    pass

class SQLUpdateSQLError(Error):
    pass

class SQLDeleteSQLError(Error):
    pass

class UserAddError(Error):
    pass
class UserExitsError(Error):
    pass

class UserAddKeyError(Error):
    pass

class UserDeleteError(Error):
    pass

class UserisExits(Error):
    pass