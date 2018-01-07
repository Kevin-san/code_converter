# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''

from java.sql import *
from util.sqlUtil import sqlUtil
from bean.database import Column,Table,Procedure


class Database(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def getTable(self,conn,database,table):
        pst=conn.prepareStatement(sqlUtil.getColumnSql(database, table))
        rsmd=pst.getMetaData()
        length=rsmd.getColumnCount()
        columns=[]
        for index in xrange(0,length):
            name = rsmd.getColumnName(index+1)
            cType = rsmd.getColumnTypeName(index+1)
            column=Column(cType,name)
            columns.append(column)
        table=Table(database,table,columns)
        return table
            
        
    def getTables(self,conn,database):
        meta = conn.getMetaData()
        rs=meta.getTables(None,database,None,["TABLE"])
        tables=[]
        while rs.next():
            table=rs.getString(3)
            tables.append(table)
        return tables
            
        
        
    def getProcedure(self,conn,database,procedure):
        meta=conn.getMetaData()
        rs=meta.getProcedureColumns(None,database,procedure,'%')
        inColumns=[]
        while rs.next():
            name=rs.getString("COLUMN_NAME")
            cType=rs.getInt("DATA_TYPE")
            column=Column(cType,name)
            inColumns.append(column)
        proc=Procedure(database, procedure, inColumns, [])
        return proc
        
    def getProcedures(self,conn,database):
        meta=conn.getMetaData()
        rs=meta.getProcedures(None,database,'%')
        procedures=[]
        while rs.next():
            procedure=rs.getString("PROCEDURE_NAME")
            procedures.append(procedure)
        return procedures

if __name__=="__main__":
    from util.connectionUtil import connectionUtil
    conn=connectionUtil.getConnection("com.mysql.jdbc.Driver", "jdbc:mysql://localhost:3306/test", "root", "root")
    db=Database()
    proc=db.getProcedure(conn, 'test', 'test_proc')
    table=db.getTable(conn, 'columns', 'pet')
    tables=db.getTables(conn, 'columns')
    procs=db.getProcedures(conn, 'test')
    
    
    