# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''

from java.sql import *
from util.codeutils import sqlutil
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
        
    def get_table(self,conn,database,table):
        pst=conn.prepareStatement(sqlutil.get_my_sql(database, table))
        rsmd=pst.getMetaData()
        length=rsmd.getColumnCount()
        columns=[]
        for index in range(0,length):
            name = rsmd.getColumnName(index+1)
            c_type = rsmd.getColumnTypeName(index+1)
            column=Column(c_type,name)
            columns.append(column)
        table=Table(database,table,columns)
        return table
            
        
    def get_tables(self,conn,database):
        meta = conn.getMetaData()
        rs=meta.getTables(None,database,None,["TABLE"])
        tables=[]
        while rs.next():
            table=rs.getString(3)
            tables.append(table)
        return tables
            
        
        
    def get_procedure(self,conn,database,procedure):
        meta=conn.getMetaData()
        rs=meta.getProcedureColumns(None,database,procedure,'%')
        in_columns=[]
        while rs.next():
            name=rs.getString("COLUMN_NAME")
            c_type=rs.getInt("DATA_TYPE")
            column=Column(c_type,name)
            in_columns.append(column)
        proc=Procedure(database, procedure, in_columns, [])
        return proc
        
    def get_procedures(self,conn,database):
        meta=conn.getMetaData()
        rs=meta.getProcedures(None,database,'%')
        procedures=[]
        while rs.next():
            procedure=rs.getString("PROCEDURE_NAME")
            procedures.append(procedure)
        return procedures