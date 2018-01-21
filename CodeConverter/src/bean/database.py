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
    
    def __init__(self, c_type,name):
        if type(c_type) is int:
            self._c_type=types[c_type]
        else:
            self._c_type=sTypes[c_type]
        self._name=name
        
    def set_c_type(self,new_c_type):
        self._c_type=new_c_type
    
    def get_c_type(self):
        return self._c_type
    
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
    
    def __init__(self,database,name,in_columns=[],comment):
        self._database=database
        self._name=name
        self._in_columns=in_columns
        self._comment=comment
        self._out_columns=[]
        
    def set_in_columns(self,new_in_columns):
        self._in_columns=new_in_columns
        
    def get_in_columns(self):
        return self._in_columns
    
    def set_out_columns(self,new_out_columns):
        self._out_columns=new_out_columns
        
    def get_out_columns(self):
        return self._out_columns
    
    def set_database(self,new_database):
        self._database=new_database
        
    def get_database(self):
        return self._database
    
    def set_name(self,new_name):
        self._name=new_name
        
    def get_name(self):
        return self._name