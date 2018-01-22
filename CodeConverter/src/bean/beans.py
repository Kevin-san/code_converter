#!/usr/local/jython2.7/bin/jython

# -*- coding: utf-8 -*-

from util.codeutils import code_utils
		
types={-7:"Boolean",
	   -6:"Short",
	   5:"Short",
	   4:"Integer",
	   -5:"Long",
	   6:"Double",
	   7:"Float",
	   8:"Double",
	   2:"java.math.Decimal",
	   3:"java.math.Decimal",
	   1:"String",
	   12:"String",
	   -1:"String",
	   91:"java.sql.Date",
	   92:"java.sql.Time",
	   93:"java.sql.Timestamp",
	   -2:"Byte[]",
	   -3:"Byte[]",
	   -4:"Byte[]",
	   0:"String",
	   1111:"String"}

sTypes={"CHAR":"String",
		"VARCHAR":"String",
		"VARCHAR2":"String",
		"LONGVARCHAR":"String",
		"BINARY":"Byte[]",
		"VARBINARY":"Byte[]",
		"LONGVARBINARY":"Byte[]",
		"TINYINT":"Short",
		"SMALLINT":"Short",
		"INTEGER":"Integer",
		"INT":"Integer",
		"NUMBER":"Integer",
		"BIGINT":"Long",
		"REAL":"Float",
		"FLOAT":"Double",
		"NUMERIC":"java.math.BigDecimal",
		"DECIMAL":"java.math.BigDecimal",
		"BIT":"Boolean",
		"DATE":"java.sql.Date",
		"TIME":"java.sql.Time",
		"DATETIME":"java.sql.Timestamp",
		"TIMESTAMP":"java.sql.Timestamp",
		"UNKNOWN":"String"}

class Property(object):
	def __init__(self,is_static,name,col_type):
		self.is_static=is_static
		self.col_name=name
		self.name=code_utils.convert2property(name)
		self.cap_name=code_utils.to_first_upper_case(self.name)
		n_type=col_type
		if type(n_type) is int:
			self.p_type=types[n_type]
		else:
			if 'identity' in col_type:
				n_type=col_type.replace(' identity','')
			c_type=n_type.upper()
			self.p_type=sTypes[c_type]

	def set_name(self,new_name):
		self.name=new_name
		self.cap_name=code_utils.to_first_upper_case(new_name)
	
class Method(object):
	
	def __init__(self,is_static,ret_type,m_name,m_comment,parameters=[]):
		self.is_static=is_static
		self.ret_type=ret_type
		self.name=m_name
		self.parameters=parameters
		self.comment=m_comment

	
class Configuration(object):
	def __init__(self,project_path,name,suffix):
		self._path=project_path
		self._name=name
		self._suffix=suffix
		
	def set_path(self,new_path):
		self._path=new_path
		
	def get_path(self):
		return self._path
	
	def set_name(self,new_name):
		self._name=new_name
		
	def get_name(self):
		return self._name
	
	def set_suffix(self,new_suffix):
		self._suffix=new_suffix
		
	def get_suffix(self):
		return self._suffix

class Column(object):
	
	def __init__(self, c_type,name):
		self._c_type=c_type
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
	
	def __init__(self,database,name,in_columns=[],out_columns=[]):
		self._database=database
		self._name=name
		self._in_columns=in_columns
		self._out_columns=out_columns
		
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

class SqlObject(object):
	def __init__(self,database,procedure,comment):
		self.database=database
		self.procedure=procedure
		self.comment=comment
		self.sqls=[]
