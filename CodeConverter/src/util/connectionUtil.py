# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''
from java.sql import *
from java.lang import Class
import java.lang.Exception

import logging
logging.getLogger("util.connectionUtil")

class ConnectionUtil(object):

    def __init__(self):
       '''
       constructors
       ''' 
        
    def getConnection(self,driver,url,user,password):
        try:
            Class.forName(driver)
            conn=DriverManager.getConnection(url, user, password)
        except Exception:
            raise
        return conn
    
    def closeConnection(self,conn):
        if conn is not None:
            conn.close()
            
    def closeStatement(self,stat):
        if stat is not None:
            stat.close()
            
    def closeResultSet(self,rst):
        if rst is not None:
            rst.close()
connectionUtil=ConnectionUtil()  