# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''

class JProject(object):
    def __init__(self, name,srcs=[],libs=[],configs=[]):
        self._name=name
        self._srcs=srcs
        self._libs=libs
        self._configs=configs
        
    def set_name(self,new_name):
        self._name=new_name
        
    def get_name(self):
        return self._name
    
    def set_srcs(self,new_srcs):
        self._srcs=new_srcs
        
    def get_srcs(self):
        return self._srcs
    
    def set_libs(self,new_libs):
        self._libs=new_libs
        
    def get_libs(self):
        return self._libs
    
    def set_configs(self,new_configs):
        self._configs=new_configs
        
    def get_configs(self):
        return self._configs
        

class Class(object):
    def __init__(self,c_name,p_name,import_classes={},extend='',implements_classes={},properties=[],methods=[]):
        self.name=c_name
        self.package=p_name
        self.import_classes=import_classes
        self.extend=extend
        self.implements_classes=implements_classes
        self.properties=properties
        self.methods=methods
    def set_name(self,new_name):
        self.name=new_name
        
    def get_name(self):
        return self.name
    
    def set_package(self,new_package):
        self.package=new_package
        
    def get_package(self):
        return self.package
    
    def set_import_classes(self,new_import_classes):
        self.import_classes=new_import_classes
        
    def get_import_classes(self):
        return self.import_classes
    
    def set_implements_classes(self,new_implements_classes):
        self.implements_classes=new_implements_classes
        
    def get_implements_classes(self):
        return self.implements_classes
    
    def set_extend(self,new_extend):
        self.extend=new_extend
        
    def get_extend(self):
        return self.extend
    
    def set_properties(self,new_properties):
        self.properties=new_properties
        
    def get_properties(self):
        return self.properties
    
    def set_methods(self,new_methods):
        self.methods=new_methods
        
    def get_methods(self):
        return self.methods
    
class Source(object):
    
    def __init__(self,name,packages=[]):
        self._name=name
        self._packages=packages
        
    def set_name(self,new_name):
        self._name=new_name
    
    def get_name(self):
        return self._name
    
    def set_packages(self,new_packages):
        self._packages=new_packages
        
    def get_packages(self):
        return self._packages
    
class Lib(object):
    def __init__(self,name,lib_names=[]):
        self._name=name
        self._lib_names=[]
        
    def set_name(self,new_name):
        self._name=new_name
        
    def get_name(self):
        return self._name
    
    def set_lib_names(self,new_lib_names):
        self._lib_names=new_lib_names
        
    def get_lib_names(self):
        return self._lib_names
    
class Config(object):
    def __init__(self,name,configurations=[]):
        self._name=name
        self._configurations=configurations
        
    def set_name(self,new_name):
        self._name=new_name
        
    def get_name(self):
        return self._name
    
    def set_configurations(self,new_configurations):
        self._configurations=new_configurations
        
    def get_configurations(self):
        return self._configurations
    
        
        