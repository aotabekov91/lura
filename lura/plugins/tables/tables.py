import os
import sqlite3
from collections import OrderedDict

from sqlite3 import connect, Row, IntegrityError

class Tables(OrderedDict):
    def __init__(self, parent, configuration):
        super().__init__()
        self.window=parent
        self.name='tables'

    def addTable(self, tableClass, tableName=None): 
        table=tableClass()
        if tableName is None: 
            tableName=table.__class__.__name__.lower().replace('table', '') 
        setattr(self, tableName, table)


class Table:

    def __init__(self, table, fields, loc='/home/adam/code/lura/lura.db'):
        self.table=table
        self.fields
        self.loc=loc
        self.createTable() 

    def createTable(self):
        sql= "CREATE TABLE IF NOT EXISTS {} ({})".format(
                self.table,
                ','.join(self.fields))
        self.execute(sql)

    def execute(self, sql):
        con = connect(self.loc)
        con.row_factory = Row
        cur=con.cursor()
        cur.execute(sql)
        con.commit()
        return cur

    def getCondition(self, criteria):
        ctr=[]
        if type(criteria)!=list: criteria=[criteria]
        for c in criteria:
            ctr+=['{field}="{value}"'.format(**c)]
        return ' and '.join(ctr)

    def updateRow(self, criteria, updateDict):
        condition=self.getCondition(criteria)
        sql='update {} set {} where {}'
        updates=['{} = "{}"'.format(k, v.replace('"', '\'')) for k, v in updateDict.items()]
        update=', '.join(updates)
        sql=sql.format(self.table, update, condition)
        self.execute(sql)

    def writeRow(self, rowDic=None, update=True):
        fields=','.join(['"{}"'.format(k) for k in rowDic.keys()])
        values=','.join(['"{}"'.format(k) for k in rowDic.values()])
        sql = 'insert into {}' '({})' 'values ({})'.format(
                self.table, fields, values) 
        try:
            self.execute(sql)
        except sqlite3.IntegrityError:
            if update:
                if rowDic.get('id', None) is None: return 
                criteria={'field':'id', 'value':rowDic['id']}
                rowDic=rowDic.copy()
                rowDic.pop('id')
                self.updateRow(criteria, rowDic)

    def removeRow(self, criteria):
        condition=self.getCondition(criteria)
        sql = 'delete from {} where {}'.format(
                self.table, condition) 
        self.execute(sql)

    def getRow(self, criteria):
        condition=self.getCondition(criteria)
        sql = 'select * from {} where {}'.format(
                self.table, condition)
        return self.query(sql)

    def getAll(self):
        return self.query(f'select * from {self.table}')

    def query(self, sql):
        cur=self.execute(sql)
        return cur.fetchall()

