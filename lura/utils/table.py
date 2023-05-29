import os
import sqlite3
from sqlite3 import connect, Row, IntegrityError

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Table:

    def __init__(self, table, fields, loc='/home/adam/code/lura/lura.db'):
        self.table=table
        self.fields=fields
        self.loc=loc
        self.createTable() 

    def createTable(self):
        sql= "CREATE TABLE IF NOT EXISTS {} ({})".format(
                self.table,
                ','.join(self.fields))
        self.execute(sql)

    def execute(self, sql, values=None):
        con = connect(self.loc)
        con.row_factory = dict_factory 
        cur=con.cursor()
        try:
            if values:
                cur.execute(sql, values)
            else:
                cur.execute(sql)
            con.commit()
        except:
            pass
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
        values=','.join(['"{}"'.format(str(k).replace('"', '\'')) for k in rowDic.values()])
        sql = f'insert into {self.table} ({fields}) values ({values})'

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
        sql = f'delete from {self.table} where {condition}'
        self.execute(sql)

    def getRow(self, criteria):
        condition=self.getCondition(criteria)
        sql = f'select * from {self.table} where {condition}'
        return self.query(sql)

    def getAll(self):
        return self.query(f'select * from {self.table}')

    def query(self, sql):
        cur=self.execute(sql)
        return cur.fetchall()

    def getField(self, fieldName, row_id_name, row_id_value):
        found=self.getRow({'field':row_id_name, 'value':row_id_value})
        if len(found)>0 and fieldName in found[0].keys(): return found[0][fieldName]

    def setField(self, fieldName, fieldValue, row_id_name, row_id_value):
        self.updateRow({'field':row_id_name, 'value':row_id_value}, {fieldName:fieldValue})
