# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''
import os
import sys,getopt
import zipfile
import jinja2
import re
from com.ziclix.python.sql import procedure

default=u"F:\\code"
pattern=re.compile(r'[\s_+]+')
wordPattern = re.compile(r'[a-z]+')

class CodeUtils(object):
    
    def delete_last_char(self,str):
        str_list=list(str)
        str_list.pop()
        return "".join(str_list)
    
    def convert2property(self,str):
        list=pattern.split(str)
        first = list[0]
        m = wordPattern.search(first)
        if m:
            property=self.to_first_lower(first)
        else:
            property=first.lower()
        if len(list)==1:
            return property
        for index in (1,len(list)):
            property+=(self.to_first_upper_other_lower(list[index]))
        return property
    
    def to_first_lower(self,str):
        return str[:1].lower() + str[1:]
        
    def to_first_upper_other_lower(self,str):
        result = str.lower()
        return result.capitalize()
    
    def write_file(self,filename,input_string):
        f= open(filename,'w')
        f.write(input_string)
        f.close()

    def zip_file(self,zipname,parentdir):
        f_zip = zipfile.ZipFile('%s.zip'%(zipname),'w')
        for current_path, subfolders, filesname in os.walk(r'%s'%(parentdir)):
            new_path = current_path.replace(parentdir,zipname)
            for file in filesname:
                f_zip.write(os.path.join(current_path, file),os.path.join(new_path,file))
        f_zip.close()
        
    def load_property(self,filename):
        values={}
        with open(filename) as f:
            for line in f.readlines():
                list=line.split('=',2)
                all_list = line.split('=')
                if len(all_list) >2:
                    result='='*(len(all_list)-2)
                    list[1]+=result
                values[list[0]]=list[1]
        return values
    
    def convert_package2directory(self,package):
        list=package.split(".")
        dir=package
        if len(list)>1:
            dir=package.replace(".","/")
        return dir
    
    def template(self,tempname,data):
        TemplateLoader=jinja2.FileSystemLoader(searchpath='C:/Users/xcKev/git/CodeConverter/CodeConverter/src/templates')
        TemplateEnv=jinja2.Environment(loader=TemplateLoader)
        template=TemplateEnv.get_template(tempname)
        return template.render(data)
    
    def create_java(self,project):
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
            os.remove(path)
        elif os.path.isdir(path):
            for item in os.listdir(path):
                itempath=os.path.join(path,item)
                self.rmfiles(itempath)
                os.rmdir(path)      
    def mkdir(self):
        os.mkdir(default)
                   
    def get_opt(self,option,option_comment):
        try:
            opts,args = getopt.getopt(sys.argv[1:],'%s:'%(option),option_comment)
        except getopt.GetoptError as err:
            print(err)  # will print something like "option -a not recognized"
            sys.exit(2)
        for opt,arg in opts,args:
                if opt == '-%s'(option):
                    return arg
        return None

class SqlUtil(object):
    
    def get_my_sql(self,database,table):
        return u'select * from %s.%s'%(database,table)
    
    def get_sy_sql(self,database,table):
        return u'select * from %s..%s'%(database,table)
    
    def get_my_procedure_comment(self,database,procedure):
        return u"select body from mysql.proc where db='%s' and name='%s' and type='PROCEDURE'"%(database,procedure)
    
    def get_sy_procedure_comment(self,database,procedure):
        return u"select text %s.dbo.syscomments WHERE id = ( SELECT id FROM %s.dbo.sysobjects WHERE name = '%s');"%(database,database,procedure)
sqlutil=SqlUtil()
codeutil=CodeUtils()
    