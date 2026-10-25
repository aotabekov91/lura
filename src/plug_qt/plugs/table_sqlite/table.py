import os
import sqlite3

class Table:

    def __init__(
            self,
            uniq={}, 
            loc=None, 
            fields=[], 
            foreign={}, 
            idField='id', 
            table_name=None, 
            folder='~/.tables',
            database_name='table', 
            ):
        self.loc=loc
        self.fields=fields
        self.idField=idField
        self.uniq=uniq.copy()
        self.table_name=table_name
        self.database_name=database_name
        self.foreign=foreign.copy()
        self.folder=os.path.expanduser(folder)
        self.setup()

    def setup(self):
        self.addUniq()
        self.setName()
        self.setLoc()
        self.setFields()
        self.createTable() 

    def activate(self, action=None, **kwargs):
        if action:
            functor=getattr(self, action, None)
            if functor:
                return functor(**kwargs)

    def addUniq(self):
        for name, cons in self.uniq.items():
            cons=tuple(cons)
            self.fields+=[f'constraint {name} unique {str(cons)}']

    def setName(self):
        if not self.table_name: 
            self.table_name=self.__class__.__name__
        if not self.database_name: 
            self.database_name=self.table_name

    def setLoc(self):
        if not self.loc:
            if not os.path.exists(self.folder): 
                os.mkdir(self.folder)
            d, f =self.database_name, self.folder
            self.loc=f'{f}/{d}.db'
        if not os.path.exists(self.loc):
            os.popen(f'sqlite3 {self.loc}')

    def setFields(self):
        exc=['constraint', 'foreign']
        cfields=[]
        for f in self.fields:
            fname=f.split(' ')[0]
            if not fname in exc:
                cfields+=[f.split(' ')]
        self.fdict={}
        for f in cfields:
            self.fdict[f[0]]=f[1]
        cfields=list(self.fdict.keys())
        self.cfields=cfields

    def createTable(self):
        flds=','.join(self.fields)
        sql="CREATE TABLE IF NOT EXISTS {} ({})"
        sql= sql.format(self.table_name, flds) 
        self.exec(sql)

    def updateRow(self, criteria, data):
        udict=self.filterDict(data)
        upd=[]
        sql='update {} set {} where {}'
        for k, v in udict.items():
            if k==self.idField: continue
            v=str(v).replace('"',  '\'')
            upd+=['{} = "{}"'.format(k, v)]
        sql=sql.format(
                self.table_name, 
                ', '.join(upd),
                self.getCond(criteria))
        self.exec(sql)

    def filterDict(self, data):
        adata={}
        for key, value in data.items():
            if key in self.cfields:
                adata[key]=value
        return adata

    def writeRow(self, data=None, uid=None):
        cond={}
        rowDic=self.filterDict(data)
        for key, name in self.uniq.items():
            cond={}
            for i in name:
                if not i in rowDic: break
                cond[i]=rowDic[i]
        rows=self.getRow(cond)
        if rows:
            row_data=rows[0]
            uid = uid or self.idField
            rc=rowDic.copy()
            rc.pop(uid, None)
            idx=row_data.get(uid, None)
            self.updateRow({uid: idx}, rc)
            return idx
        field=[]
        for key in rowDic.keys():
            if key in self.cfields:
                field+=['"{}"'.format(key)]
        value=[]
        for j, key in rowDic.items(): 
            if j in self.cfields:
                key=str(key).replace('"', '\'')
                value+=['"{}"'.format(key)]
        sql = 'insert into {} ({}) values ({})'
        value, field=','.join(value), ','.join(field)
        sql = sql.format(self.table_name, field, value)
        return self.exec(sql)

    def removeRow(self, criteria):
        c=self.getCond(criteria)
        sql = 'delete from {} where {}'
        sql = sql.format(self.table_name, c)
        self.exec(sql)

    def exec(self, sql, fetch=False):
        def dict_factory(column, row):
            data = {}
            for idx, col in enumerate(column.description):
                data[col[0]] = row[idx]
            return data

        result=None
        with sqlite3.connect(self.loc) as c:
            c.row_factory = dict_factory 
            cur=c.cursor()
            try:
                cur.execute(sql)
                result=cur.lastrowid
                if fetch:
                    result=cur.fetchall()
            except:
                pass
            finally:
                c.commit()
        return result

    def getCond(self, cond):
        if type(cond)!=list: 
            cond=[cond]
        ctr=[]
        for i in cond:
            for f, v in i.items():
                if type(v)==str and "'" in v: 
                    v=v.replace('"', "'")
                    ctr+=[f'{f}="{v}"']
                else:
                    ctr+=[f"{f}='{v}'"]
        return ' and '.join(ctr)

    def getRow(self, criteria={}):
        acriteria={}
        for key, value in criteria.items():
            if key in self.cfields:
                acriteria[key]=value
        condition=self.getCond(acriteria)
        sql = 'select * from {} where {}'
        sql = sql.format(
                self.table_name, condition)
        return self.exec(sql, fetch=True)

    def getRows(self):
        sql='select * from {}'
        sql=sql.format(self.table_name)
        return self.exec(sql, fetch=True)

    def getField(self, field, key, value):
        data={'field':key, 'value':value}
        row=self.getRow(data)
        if row and field in row[0].keys(): 
            return row[0][field]

    def setField(self, fkey, fvalue, key, value):
        data={'field':key, 'value':value}
        self.updateRow(data, {fkey:fvalue})
