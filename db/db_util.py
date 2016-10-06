#!/usr/bin/python
from __future__ import absolute_import
import MySQLdb

class DbUtil:
    def __init__(self):
        self.krama_db = MySQLdb.connect("localhost", "root", "mysql",
                                      "krama_db")
        self.dict_cursor=self.krama_db.cursor(MySQLdb.cursors.DictCursor)
        self.cursor=self.krama_db.cursor

    def execute(self,statement):
        krama_db = MySQLdb.connect("localhost", "root", "mysql",
                                      "krama_db")
        krama_cursor = krama_db.cursor()
        try:
            krama_cursor.execute(statement)
            krama_cursor.close()
            krama_db.commit()
        except:
            krama_db.rollback()


    def fetch_dict(self,statement):
        krama_db = MySQLdb.connect("localhost", "root", "mysql",
                                      "krama_db")
        krama_cursor = krama_db.cursor(MySQLdb.cursors.DictCursor)
        try:
            krama_cursor.execute(statement)
            results=[row for row in krama_cursor.fetchall()]
            krama_cursor.close()
            krama_db.commit()
            return results
        except:
            krama_db.rollback()
            return []

    def close(self):
        self.krama_db.close()
