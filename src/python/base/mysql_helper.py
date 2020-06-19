# -*- coding: utf-8 -*-

import pymysql

class MySqlHelper():
    def __init__(self, ip, port, db_name, user_name, passwrd):
        self.ip = ip
        self.port = port
        self.db = db_name
        self.user = user_name
        self.passwd = passwrd

    def __get_connected(self):
        self.__db = pymysql.connect(host=self.ip, port=self.port,
                                    user=self.user, passwd=self.passwd,
                                    db=self.db)
        cur = self.__db.cursor()
        if not cur:
            raise(NameError, "connect db fail...")
        else:
            return cur

    def exec_query(self, sql):
        cur = self.__get_connected()
        cur.execute(sql)
        res_list = cur.fetchall()

        #must close connect after query
        self.__db.close()
        return res_list

