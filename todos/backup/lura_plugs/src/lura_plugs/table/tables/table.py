import sqlite3
from os.path import expanduser
from os import mkdir, popen, path

from .utils import dict_factory

class Table:

    uniq={}
    loc=None 
    name=None
    fields=[]
    foreign={}
    idField='id' 
    dname='table'
    folder='~/.tables'

    def __init__(self):
        self.setup()

    def setup(self):

        self.folder=expanduser(self.folder)
        self.addUniq()
        self.setName()
        self.setLoc()
        self.setFields()
        self.createTable() 

    def addUniq(self):

        for n, c in self.uniq.items():
            f=f'constraint {n} unique {str(c)}'
            self.fields+=[f]

    def setName(self):

        if not self.name: 
            self.name=self.__class__.__name__
        if not self.dname: 
            self.dname=self.name

    def setLoc(self):

        if not self.loc:
            if not path.exists(self.folder): 
                mkdir(self.folder)
            d, f =self.dname, self.folder
            self.loc=f'{f}/{d}.db'
        if not path.exists(self.loc):
            popen(f'sqlite3 {self.loc}')

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
        sql= sql.format(self.name, flds) 
        self.exec(sql)

    def updateRow(
            self, cond, udict):

        udict=self.filterDict(udict)
        upd=[]
        sql='update {} set {} where {}'
        for k, v in udict.items():
            if k==self.idField: continue
            v=str(v).replace('"',  '\'')
            upd+=['{} = "{}"'.format(k, v)]
        sql=sql.format(
                self.name, 
                ', '.join(upd),
                self.getCond(cond))
        self.exec(sql)

    def filterDict(self, adict):

        d={}
        for k, v in adict.items():
            if k in self.cfields:
                d[k]=v
        return d

    def writeRow(
            self, 
            rowDic=None, 
            uid=None
            ):

        rowDic=self.filterDict(rowDic)
        cond={}
        for k, c in self.uniq.items():
            cond={}
            for i in c:
                if not i in rowDic: break
                cond[i]=rowDic[i]
        rs=self.getRow(cond)
        if rs:
            d=rs[0]
            uid = uid or self.idField
            rc=rowDic.copy()
            rc.pop(uid, None)
            idx=d.get(uid, None)
            self.updateRow({uid: idx}, rc)
            return idx
        f=[]
        for k in rowDic.keys():
            if k in self.cfields:
                f+=['"{}"'.format(k)]
        v=[]
        for j, k in rowDic.items(): 
            if j in self.cfields:
                k=str(k).replace('"', '\'')
                v+=['"{}"'.format(k)]
        sql = 'insert into {} ({}) values ({})'
        v, f=','.join(v), ','.join(f)
        sql = sql.format(self.name, f, v)
        return self.exec(sql)

    def removeRow(
            self, 
            criteria
            ):

        c=self.getCond(criteria)
        sql = 'delete from {} where {}'
        sql = sql.format(self.name, c)
        self.exec(sql)

    def exec(self, sql, fetch=False):

        f=None
        with sqlite3.connect(self.loc) as c:
            c.row_factory = dict_factory 
            cur=c.cursor()
            try:
                cur.execute(sql)
                f=cur.lastrowid
                if fetch:
                    f=cur.fetchall()
            except:
                pass
            finally:
                c.commit()
        return f

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

    def getRow(self, cond):

        cri={}
        for k, v in cond.items():
            if k in self.cfields:
                cri[k]=v
        c=self.getCond(cri)
        sql = 'select * from {} where {}'
        sql = sql.format(self.name, c)
        return self.exec(sql, fetch=True)

    def getRows(self):

        sql='select * from {}'
        sql=sql.format(self.name)
        return self.exec(sql, fetch=True)

    def getField(
            self, field, name, value):

        d={'field':name, 'value':value}
        r=self.getRow(d)
        if r and field in r[0].keys(): 
            return r[0][field]

    def setField(
            self, 
            fname, 
            fvalue, 
            name, 
            value
            ):

        d={'field':name, 'value':value}
        self.updateRow(d, {fname:fvalue})
