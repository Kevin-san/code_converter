# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''

types={-7:"Boolean",-6:"Short",5:"Short",4:"Integer",
       -5:"Long",6:"Double",7:"Float",8:"Double",
       2:"java.math.Decimal",3:"java.math.Decimal",
       1:"String",12:"String",-1:"String",
       91:"java.sql.Date",92:"java.sql.Time",
       93:"java.sql.Timestamp",-2:"Byte[]",
       -3:"Byte[]",-4:"Byte[]",0:"String",1111:"String"}

sTypes={"CHAR":"String","VARCHAR":"String","VARCHAR2":"String",
        "LONGVARCHAR":"String","BINARY":"Byte[]","VARBINARY":"Byte[]",
        "LONGVARBINARY":"Byte[]","TINYINT":"Short","SMALLINT":"Short",
        "INTEGER":"Integer","NUMBER":"Integer","BIGINT":"Long","REAL":"Float",
        "FLOAT":"Double","NUMERIC":"java.math.BigDecimal",
        "DECIMAL":"java.math.BigDecimal","BIT":"Boolean",
        "DATE":"java.sql.Date","TIME":"java.sql.Time",
        "TIMESTAMP":"java.sql.Timestamp","UNKNOWN":"String"}

class Column(object):
    
    def __init__(self, cType,name):
        if type(cType) is int:
            self._cType=types[cType]
        else:
            self._cType=sTypes[cType]
        self._name=name
        
    def set_cType(self,new_cType):
        self._cType=new_cType
    
    def get_cType(self):
        return self._cType
    
    def set_name(self,new_name):
        self._name=new_name
        
    def get_name(self):
        return self._name
    
class Table(object):
    
    def __init__(self,database,name,columns=[]):
        self._database=database
        self._name=name
        self._columns=columns
        
    def set_columns(self,new_columns):
        self._columns=new_columns
        
    def get_columns(self):
        return self._columns
    
    def set_database(self,new_database):
        self._database=new_database
        
    def get_database(self):
        return self._database
    
    def set_name(self,new_name):
        self._name=new_name
        
    def get_name(self):
        return self._name
        
class Procedure(object):
    
    def __init__(self,database,name,inColumns=[],outColumns=[]):
        self._database=database
        self._name=name
        self._inColumns=inColumns
        self._outColumns=outColumns
        
    def set_inColumns(self,new_inColumns):
        self._inColumns=new_inColumns
        
    def get_inColumns(self):
        return self._inColumns
    
    def set_outColumns(self,new_outColumns):
        self._outColumns=new_outColumns
        
    def get_outColumns(self):
        return self._outColumns
    
    def set_database(self,new_database):
        self._database=new_database
        
    def get_database(self):
        return self._database
    
    def set_name(self,new_name):
        self._name=new_name
        
    def get_name(self):
        return self._name

           