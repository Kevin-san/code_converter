# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''
from util.beanUtil import beanUtil

class Property(object):
    def __init__(self,is_static,name,p_type):
        self.is_static=is_static
        self.name=beanUtil.convertToProperty(name)
        self.cap_name=beanUtil.toFirstUpperCase(beanUtil.convertToProperty(name))
        self.p_type=p_type
    
    def set_p_type(self,new_p_type):
        self.p_type=new_p_type
        
    def get_p_type(self):
        return self.p_type
    
    def set_name(self,new_name):
        self.name=new_name
        self.cap_name=beanUtil.toFirstUpperCase(beanUtil.convertToProperty(new_name))
        
    def get_name(self):
        return self.name
    
    def get_cap_name(self):
        return self.cap_name
    
    def set_is_static(self,new_is_static):
        self.is_static=new_is_static
        
    def get_is_static(self):
        return self.is_static
    
class Method(object):
    
    def __init__(self,is_static,ret_type,m_name,m_comment,parameters=[]):
        self.is_static=is_static
        self.ret_type=ret_type
        self.name=m_name
        self.parameters=parameters
        self.comment=m_comment
        
    def set_name(self,new_name):
        self.name=new_name
        
    def get_name(self):
        return self.name
    
    def set_is_static(self,new_is_static):
        self.is_static=new_is_static
        
    def get_is_static(self):
        return self.is_static
    
    def set_ret_type(self,new_ret):
        self.ret_type=new_ret
        
    def get_ret_type(self):
        return self.ret_type
    
    def set_parameters(self,new_parameters):
        self.parameters=new_parameters
        
    def get_parameters(self):
        return self.parameters
    
    def set_comment(self,new_comment):
        self.comment=new_comment
        
    def get_comment(self):
        return self.comment
    
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
    
    