#!/usr/local/jython2.7/bin/jython

# -*- coding:UTF-8 -*-

#!/usr/local/jython2.7/bin/jython

# -*- coding:UTF-8 -*-

from java.sql import *
from org.apache.commons.lang import StringUtils
from com.ssmb.eae.util import EAESecurity
from java.lang import *
drivers={'sybase':'com.sybase.jdbc4.jdbc.SybDriver','sqlserver':'net.sourceforge.jtds.jdbc.Driver'}

import log.logger

logger=log.logger.get_log('conn','connection')

class ConnectionUtil(object):

	def __init__(self):
		self.util=_PasswordUtil()
	
	# get connection for database
	def get_connection(self,jdbcconf):
		conn = None
		try:
			url = jdbcconf.get_url()
			user = jdbcconf.get_user()
			password = jdbcconf.get_passwd()
			if jdbcconf.is_encrypted() is True:
				self.util.set_encrypted(password)
				password = self.util.get_decrypted()
			Class.forName(jdbcconf.get_driver())
			conn = DriverManager.getConnection(url,user,password)
			logger.debug('Connection Init!')
		except Exception,ex:
			logger.error('Failed to connect to db',exc_info=True)
		return conn
	# close connection
	def close_connection(self,conn):
		try:
			if conn is not None:
				conn.close()
		except SQLException,e:
			logger.exception(e)
	# close statement
	def close_statement(self,st):
		try:
			if st is not None:
				st.close()
		except SQLException,e:
			logger.error(e)
	# close resultset
	def close_result_set(self,rst):
		try:
			if rst is not None:	
				rst.close()
		except SQLException,e:
			logger.error(e)
	
	
class JdbcConf(object):
	def __init__(self,database,url,user,passwd,is_encrypted):
		self._driver = drivers[database]
		self._url = url
		self._user =user
		self._passwd =passwd
		self._is_encrypted=is_encrypted
		
	def get_driver(self):
		return self._driver
	
	def set_driver(self,new_driver):
		self._driver = new_driver
	
	def get_url(self):
		return self._url
		
	def set_url(self,new_url):
		self._url=new_url
		
	def get_user(self):
		return self._user
		
	def set_user(self,new_user):
		self._user=new_user
		
	def get_passwd(self):
		return self._passwd
		
	def set_passwd(self,new_passwd):
		self._passwd=new_passwd
	
	def is_encrypted(self):
		return self._is_encrypted == 'True'
	
	def set_is_encrypted(self,new_is_encrypted):
		self._is_encrypted = new_is_encrypted
		
	def check_value(self):
		if self._database == '' or self._url == '' or self._user == '' or self._passwd == '':
			return False
		else:
			return True

class _PasswordUtil(object):
	def __init__(self):
		self._encrypted=''
		self._decrypted=''
		self._key='asdf$(h#faoRtgs31f*1#252'
		self._login=''

	def encrypt(self):
		try:
			self._encrypted = EAESecurity.encrypt(self._decrypted,self._key)
		except Exception,ex:
			logger.error(u"Error to encrypt pwd %s"%(ex))
	
	def decrypt(self):
		try:
			self._decrypted = EAESecurity.decrypt(self._encrypted,self._key)
		except Exception,ex:
			logger.error(u"Error to decrypt pwd %s"%(ex))
			
	def set_encrypted(self,new_encrypted):
		self._encrypted = new_encrypted
		
	def get_encrypted(self):
		if StringUtils.isBlank(self._encrypted):
			self.encrypt()
		return self._encrypted
	
	def set_decrypted(self,new_decrypted):
		self._decrypted=new_decrypted
		
	def get_decrypted(self):
		if StringUtils.isBlank(self._decrypted):
			self.decrypt()
		return self._decrypted
		
	def set_login(self,new_login):
		self._login = new_login
	
	def get_login(self):
		return self._login
		
connection=ConnectionUtil()
