# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''
import re

pattern=re.compile(r'[\s_+]+')
wordPattern = re.compile(r'[a-z]+')
class BeanUtil(object):


    def __init__(self, params):
        '''
        Constructor
        '''
    def convertToProperty(self,str):
        list=pattern.split(str)
        first = list[0]
        m = wordPattern.match(property)
        if len(list)==1 and m:
            property=first[:1].lower() + first[1:]
            return property
        else:
            property=first.lower()
        for index in (1,len(list)):
                property+=(self.toFirstUpperCase(list[index]))
        return property
            
        
    def toFirstUpperCase(self,str):
        result = str.lower()
        return result.capitalize()
    
beanUtil=BeanUtil()