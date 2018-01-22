#!/usr/local/jython2.7/bin/jython

# -*- coding:UTF-8 -*-

from java.sql import *
from util.codeutils import code_utils
from bean.beans import Column,Table,Procedure
from bean.java_project import Class
import log.logger
logger=log.logger.get_log('dao','database')

class Database(object):
	def get_table(self,conn,database,table):
		pst=conn.prepareStatement(code_utils.get_column(database, table))
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
	
	def get_procedure_comment(self,conn,database,procedure):
		st=conn.createStatement()
		sql=code_utils.get_procedure_comment_sql(database,procedure)
		rs=st.executeQuery(sql)
		str=""
		while rs.next():
			text=rs.getString("text")
			str+=text
		return str
		
	def get_procedure(self,conn,database,procedure):
		meta=conn.getMetaData()
		rs=meta.getProcedureColumns(database,'dbo',procedure,'%')
		in_columns=[]
		while rs.next():
			name=rs.getString("COLUMN_NAME")
			if 'RETURN_VALUE' == name:
				continue
			name=name.replace('@','')
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

database=Database()

