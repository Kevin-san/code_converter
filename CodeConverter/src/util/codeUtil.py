# -*- coding: utf-8 -*-
'''
Created on 2018年1月3日

@author: xcKev
'''
import os
import sys,getopt
import zipfile
import logging
import jinja2

default=u"F:\\code"
logging.getLogger("util.codeUtil")
class CodeUtil(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def writeFile(self,filename,inputString):
        with open(filename,'w') as f:
            f.write(inputString)

    def zipFile(self,zipname,parentdir):
        zip = zipfile.ZipFile('%s.zip'%(zipname),'w')
        for current_path, subfolders, filesname in os.walk(r'%s'%(parentdir)):
            new_path = current_path.replace(parentdir,zipname)
            for file in filesname:
                zip.write(os.path.join(current_path, file),os.path.join(new_path,file))
        zip.close()
        
    def loadProperty(self,filename):
        values={}
        with open(filename) as f:
            for line in f.readlines():
                list=line.split('=',2)
                allList = line.split('=')
                if len(allList) >2:
                    result='='*(len(allList)-2)
                    list[1]+=result
                values[list[0]]=list[1]
        return values
    
    def convertPackageToDirectory(self,package):
        list=package.split(".")
        dir=package
        if len(list)>1:
            dir=package.replace(".","/")
        print(dir)
        return dir
    
    def template(self,tempname,data):
        TemplateLoader=jinja2.FileSystemLoader(searchpath='/templates')
        TemplateEnv=jinja2.Environment(loader=TemplateLoader)
        template=TemplateEnv.get_template(tempname)
        return template.render(data)
    
    def createJavaProject(self,project):
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
            except IOError:
                logging.error(u"IOError")
        elif os.path.isdir(path):
            for item in os.listdir(path):
                itempath=os.path.join(path,item)
                self.rmfiles(itempath)
            try:
                os.rmdir(path)
            except IOError:
                logging.error(u"IOError")
                
    def mkdir(self):
        os.mkdir(default)
                   
    def getOpt(self,option,optionComment):
        try:
            opts,args = getopt.getopt(sys.argv[1:],'%s:'%(option),optionComment)
        except getopt.GetoptError as err:
            print(err)  # will print something like "option -a not recognized"
            sys.exit(2)
        for opt,arg in opts,args:
                if opt == '-%s'(option):
                    return arg
        return None

codeUtil=CodeUtil()
    