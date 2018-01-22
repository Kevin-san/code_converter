#!/usr/local/jython2.7/bin/jython

# -*- coding: utf-8 -*-

import os
import sys,getopt
import zipfile
import jinja2
import log.logger
import re
import json

default=u"/var/tmp/code"
logger=log.logger.get_log('util','util.codeutils')
pattern=re.compile(r'[\s_+]+')
wordPattern = re.compile(r'[a-z]+')
word_num_pattern=re.compile(r'[a-z0-9]+')
table_columns={"Brch":"Branch",
				"Acct":"Account",
				"Cd":"Code",
				"Addr":"Address",
				"U":"User",
				"Dte":"Date",
				"Upd":"Update",
				"Cntct":"Contact",
				"Tel":"Telephone",
				"BL":"BorrowLoan",
				"Flg":"Flag",
				"Amt":"Amount",
				"Grp":"Group",
				"Opn":"Open",
				"Mnc":"Mnemonic",
				"YMD":"Date",
				"CAN":"Cancel",
				"CUST":"Customer",
				"Cust":"Customer",
				"ACCT":"Account"
				}


class CodeUtils(object):
	def convert2property(self,str):
		list=pattern.split(str)
		if len(list)==1:
			hump_list=self.split_humpstr2list(str)
			list=hump_list if len(hump_list)>1 else list
		first=list[0] if table_columns.get(list[0]) is None else table_columns[list[0]]
		m=wordPattern.search(first)
		if m:
			property=first[:1].lower()+first[1:]
		else:
			property=first.lower()
		if len(list)==1:
			logger.debug(property)
			return property
		for index in range(1,len(list)):
			val=table_columns.get(list[index]) if table_columns.get(list[index]) else list[index]
			str=val.lower()
			property+=(self.to_first_upper_case(str))
		logger.debug(property)
		return property

	def to_first_upper_case(self,str):
		return (str[:1].upper()+str[1:])
		
	def split_humpstr2list(self,str):
		chars=list(str)
		result=""
		results=[]
		for char in chars:
			match=word_num_pattern.search(char)
			if match:
				result+=char
			else:
				results.append(result)
				result=char
		results.append(result)
		if results[0] == "":results.pop(0)
		return results
				
	def get_column_sql(self,database,table):
		return u'select * from %s.%s'%(database,table)

	def get_column(self,database,table):
		return u'select * from %s..%s'%(database,table)
	
	def get_procedure_comment_sql(self,database,procedure):
		return u"select text from %s.dbo.syscomments where id=(select id from %s.dbo.sysobjects where name='%s')"%(database,database,procedure)
	
	def get_my_procedure_comment(self,database,procedure):
		return u"select body from mysql.proc where db='%s' and name='%s' and type='PROCEDURE'"%(database,procedure)
	
	def create_where_sql(self,params):
		str=' where 1=1'
		for param in params:
			str+=(' and %s =?'%(param))
		return str
	
	def create_insert_sql(self,database,table,columns):
		str='insert into %s..%s('%(database,table)
		for col_name in columns:
			str+=('%s,'%(col_name))
		str=self.del_last_char(str)
		str+=') values('
		for col_name in columns:
			org+='?,'
		str=self.del_last_char(org)
		str+=')'
		return str
	
	def create_update_sql(self,database,table,columns,params):
		org='update %s..%s set '%(database,table)
		for col_name in columns:
			org+=('%s=?,'%(col_name))
		org=self.del_last_char(org)
		str=self.create_where_sql(params)
		return (org+str)
	
	def create_select_sql(self,database,table,columns,params):
		org='select '
		for col_name in columns:
			org+=('%s,'%(col_name))
		org=self.del_last_char(org)
		org+=(' from %s..%s '%(database,table))
		str=self.create_where_sql(params)
		return (org+str)
	
	def create_delete_sql(self,database,table,params):
		org='delete from %s..%s '%(database,table)
		str=self.create_where_sql(params)
		return (org+str)
		
	def write_file(self,filename,input_str):
		f=open(filename,'w')
		f.write(input_str)
		f.close()

	def zip_file(self,zipname,parentdir):
		zip = zipfile.ZipFile('%s.zip'%(zipname),'w')
		for current_path, subfolders, filesname in os.walk(r'%s'%(parentdir)):
			new_path = current_path.replace(parentdir,zipname)
			for file in filesname:
				zip.write(os.path.join(current_path, file),os.path.join(new_path,file))
		zip.close()
		
	def load_property(self,filename):
		values={}
		f=open(filename)
		for line in f.readlines():
			list=line.split('=',2)
			all_list = line.split('=')
			if len(all_list) >2:
				result='='*(len(all_list)-2)
				list[1]+=result
			values[list[0]]=list[1].replace('\n','')
		f.close()
		return values
	
	def convert_package2directory(self,package):
		list=package.split(".")
		dir=package
		if len(list)>1:
			dir=package.replace(".","/")
		return dir
	
	def template(self,tempname,data):
		father_path=self.get_fatherpath()
		logger.debug(father_path)
		template_loader=jinja2.FileSystemLoader(searchpath='%s/templates'%(father_path))
		template_env=jinja2.Environment(loader=template_loader)
		template=template_env.get_template(tempname)
		return template.render(data)
	
	def get_fatherpath(self):
		pwd=os.getcwd()
		father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
		return father_path
	
	def create_java_project(self,project):
		proj_name=project.get_name()
		srcs=project.get_srcs()
		libs=project.get_libs()
		configs=project.get_configs()
		for src in srcs:
			packages=src.get_packages()
			src_name=src.get_name()
			for package in packages:
				dir_path=self.convertPackageToDirectory(package)
				path=u'%s/%s/%s/%s'%(default,proj_name,src_name,dir_path)
				self.mkdirs(path)
		for lib in libs:
			lib_name=lib.get_name()
			path=u'%s/%s/%s'%(default,proj_name,lib_name)
			self.mkdirs(path)
		for config in configs:
			conf_name=config.get_name()
			path=u"%s/%s/%s"%(default,proj_name,conf_name)
			self.mkdirs(path)
			
	def mkdirs(self,dir_path):
		os.makedirs(dir_path, mode=755)

	def rmfiles(self,path):
		if os.path.isfile(path):
			try:
				os.remove(path)
			except IOError,e:
				logger.error(e)
		elif os.path.isdir(path):
			for item in os.listdir(path):
				itempath=os.path.join(path,item)
				self.rmfiles(itempath)
			try:
				os.rmdir(path)
			except IOError,e:
				logger.error('Failed to remove files.',exc_info=True)

	def mkdir(self):
		os.mkdir(default)

	def get_opt(self,option,longarg):
		try:
			opts,args = getopt.getopt(sys.argv[1:],'%s:'%(option),[longarg])
			for opt,arg in opts:
				if opt == '-%s'%(option):
					return arg
		except getopt.GetoptError, err:
			logger.error('Failed to get opt.',exc_info=True)
		return None

	def get_opts(self,map_options):
		map_vals={}
		try:
			logger.debug('Start get opt arg')
			str=''
			longargs=[]
			for key,val in map_options.items():
				str+=(key+':')
				longargs.append(val)
			opts,args = getopt.getopt(sys.argv[1:],str,longargs)
			logger.debug(opts)
			for opt,arg in opts:
				option=opt[1:]
				if map_options[option] is not None:
					map_vals[option]=arg
			logger.debug('Finish get opt arg')
		except getopt.GetoptError, err:
			logger.error('Failed to get opts.',exc_info=True)
		return map_vals
				
	def del_last_char(self,str):
		str_list=list(str)
		str_list.pop()
		return "".join(str_list)
	
	def get_sql_childs(self,comment):
		childs=[]
		
	def load_json(self,file):
		f=open(file,encoding='utf-8')
		data=json.load(f)
		

code_utils=CodeUtils()
