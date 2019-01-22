#-*-coding:utf-8-*-

import configparser
import os
import yaml
from optparse import OptionParser
from optparse import OptionGroup

class Properties:

	def __init__(self,file_path):
		self.file_name=file_path
		self.proplines=[]
		self.properties={}
		self.propmaps={}
		self.load_lines()
		self.load_lines2map()
		self.load_lines2properties()

	def __get_dicts(self,strName,dictName,value):
		if strName.find('.')>0:
			k = strName.split('.')[0]
			dictName.setdefault(k,{})
			return self.__get_dicts(strName[len(k)+1:],dictName[k],value)
		else:
			dictName[strName] = value
			return
	def load_lines(self):
		file_h=open(self.file_name,'r')
		for line in file_h.readlines():
			line=line.strip().replace('\n','')
			self.proplines.append(line)
		file_h.close()

	def load_lines2map(self):
		for item_line in self.proplines:
			if item_line.find('=') > 0 and not line.startswith('#'):
				strs = item_line.split('=',1)
				self.propmaps[strs[0].strip()]=strs[1].strip()

	def load_lines2properties(self):
		for item_line in self.proplines:
			if item_line.find('=') > 0 and not line.startswith('#'):
				strs = item_line.split('=',1)
				self.__get_dicts(strs[0].strip(),self.properties,strs[1].strip())

	def has_key(self,key):
		return key in self.propmaps

	def get(self,key):
		default_value=''
		if key in self.propmaps:
			return self.propmaps[key]
		elif key.find('.')>0:
			return self.get_childs_key(self.properties,key)
		return default_value

	def get_childs_key(self,maps,key):
		default_value=''
		if key.find('.')>0:
			str_keys=key.split('.')
			str_first=str_keys.pop(0)
			str_other = '.'.join(str_keys)
			if str_first in maps:
				return self.get_childs_key(maps[str_first],str_other)
			return default_value
		else:
			return maps[key]

class Configs:
	def __init__(self,file_path):
		self.file_name=file_path
		self.config = configparser.ConfigParser()
		self.config.read(self.file_name)

	def get_sections(self):
		return self.config.sections()

	def get_options(self,section):
		return self.config.options(section)

	def get_config(self,section,option):
		return self.config.get(section,option)

	def get_key_values(self,section):
		return self.config.items(section)

	def has_section(self,section):
		return self.config.has_section(section)

	def has_option(self,section,option):
		return self.has_option(section,option)

class YamlConfig:

	def __init(self,file_path):
		self.file_h = open(file_path,'r')
		cfg = self.file_h.read()
		self.dicts = yaml.load(cfg)

	def has_key(self,key):
		return key in self.dicts

	def get(self,key):
		default_value=''
		if key in self.dicts:
			return self.dicts[key]
		elif key.find(':')>0:
			return self.get_childs_key(self.properties,key)
		return default_value

	def get_childs_key(self,maps,key):
		default_value=''
		if key.find(':')>0:
			str_keys=key.split(':')
			str_first=str_keys.pop(0)
			str_other = ':'.join(str_keys)
			if str_first in maps:
				return self.get_childs_key(maps[str_first],str_other)
			return default_value
		else:
			return maps[key]

def get_env(key):
	return os.getenv(key,None)
