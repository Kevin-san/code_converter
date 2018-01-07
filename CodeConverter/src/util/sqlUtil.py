# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''

class SqlUtil(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def getColumnSql(self,database,table):
        return u'select * from %s.%s'%(database,table)
    
    def getColumn(self,database,table):
        return u'select * from %s..%s'%(database,table)
    
    
sqlUtil=SqlUtil()