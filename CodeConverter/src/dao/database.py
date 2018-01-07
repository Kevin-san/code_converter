# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''

from java.sql import *
from util.sqlUtil import sqlUtil
from bean.database import Column,Table,Procedure
from bean.java_project import Class

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
        for index in range(0,length):
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
    import sys
    print(sys.path)
    from util.connectionUtil import connectionUtil
    from bean.entitys import Property
    from util.beanUtil import beanUtil
    from util.codeUtil import codeUtil
    conn=connectionUtil.getConnection("com.mysql.jdbc.Driver", "jdbc:mysql://localhost:3306/test", "root", "root")
    db=Database()
    proc=db.getProcedure(conn, 'test', 'test_proc')
    table=db.getTable(conn, 'columns', 'pet')
    properties=[]
    classes=set()
    c_name=beanUtil.toFirstUpperCase(beanUtil.convertToProperty(table.get_name()))
    for item in table.get_columns():
        p_name=item.get_name()
        c_type=item.get_cType()
        c_types=c_type.split('.')
        type=c_type
        if len(c_types)>1:
            classes.add(c_type)
            type=c_types[len(c_types)-1]
        prop=Property(False,p_name,type)
        properties.append(prop)
    bean=Class(c_name,'com.entity',classes,'',{},properties)
    data={"classBean":bean}
    str=codeUtil.template("java_bean.html", data)
    print(str)
    
    
    