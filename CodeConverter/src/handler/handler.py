#!/usr/local/jython2.7/bin/jython

# -*- coding:UTF-8 -*-

from util.connection import connection,JdbcConf
from bean.beans import Property,Column,Table,Procedure
from bean.java_project import Class
from util.codeutils import code_utils
import log.logger
logger=log.logger.get_log('handler','handler')
temp_maps={"java_bean.html":["classBean"]}

def convert_table2java_bean(pack_name,table):
	c_name='%sBean'%(code_utils.to_first_upper_case(code_utils.convert2property(table.get_name())))
	properties,classes=_convert_columns2properties(table.get_columns())
	bean=Class(c_name,pack_name,classes,'',{},properties)
	return bean

def convert_procedure_in_columns2java_bean(pack_name,procedure,new_name):
	properties,classes=_convert_columns2properties(procedure.get_in_columns())
	bean=Class(new_name,pack_name,classes,'',{},properties)
	return bean

def rander_map(tempfile,datas):
	data={}
	keys=temp_maps[tempfile]
	for index in range(0,len(datas)):
		data[keys[index]]=datas[index]
	str=code_utils.template(tempfile,data)
	return str

def update_bean_property_type(bean,type_conf):
	if type_conf is None:
		return
	map_types=code_utils.load_property(type_conf)
	for prop in bean.get_properties():
		if map_types.get(prop.col_name) is not None:
			prop.p_type=map_types[prop.col_name]

def update_bean_property_name(bean,name_conf):
	if name_conf is None:
		return
	map_names=code_utils.load_property(name_conf)
	for prop in bean.get_properties():
		if map_names.get(prop.col_name) is not None:
			prop.name=map_types[prop.col_name]

def _convert_columns2properties(columns):
	properties=[]
	classes=set()
	for item in columns:
		p_name=item.get_name()
		c_type=item.get_c_type()
		prop=Property(False,p_name,c_type)
		p_types=prop.p_type.split('.')
		if len(p_types)>1:
			classes.add(prop.p_type)
			prop.p_type=p_types[len(p_types)-1]
		properties.append(prop)
	return properties,classes

def build_proc_in_java_bean(map_values,pack_name,entity_name):
	proc=database.get_procedure(conn, map_values['d'],map_values['p'])
	bean=convert_procedure_in_columns2java_bean(pack_name,proc,entity_name)
	update_bean_property_type(bean,map_values.get('f'))
	update_bean_property_name(bean,map_values.get('n'))
	return bean
	
def build_tab_java_bean(map_values,pack_name):
	tab=database.get_table(conn,map_values['d'],map_values['t'])
	bean=convert_table2java_bean(pack_name,tab)
	update_bean_property_type(bean,map_values.get('f'))
	update_bean_property_name(bean,map_values.get('n'))
	return bean


if __name__=="__main__":
	from util.connection import connection,JdbcConf
	from dao.database import database
	from util.codeutils import code_utils
	import sys
	print(sys.path)
	map_options={"c":"--config","t":"--table","p":"--proc","b":"--beans"}
	map_values=code_utils.get_opts(map_options)
	config=map_values['c']
	map_jdbc=code_utils.load_property(config)
	print(map_jdbc['jdbc.password'])
	jdbcConf=JdbcConf(map_jdbc['jdbc.database'],map_jdbc['jdbc.url'],map_jdbc['jdbc.username'],map_jdbc['jdbc.password'],map_jdbc['jdbc.is_encrypted'])
	conn=connection.get_connection(jdbcConf)
	if map_values.get('p'):
		bean=build_proc_in_java_bean(map_values,'com.entity','OptionTrade')
	if map_values.get('t'):
		bean=build_tab_java_bean(map_values,'com.entity')
	else:
		bean=Class('','',{},'',{},[])
	str=rander_map("java_bean.html",[bean])
	logger.debug(str)
	code_utils.write_file('/var/tmp/test/%s.java'%(bean.get_name()),str)

