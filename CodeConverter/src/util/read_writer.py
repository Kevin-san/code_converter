
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
import os,gzip
import generateDS
import beautifulsoup
import PyPdf2

class JsonConverter(object):

    def __init__(self,sort_keys=False,indent=None):
        self._sort_keys=sort_keys
        self._indent=indent
        
    def convert_to_json(self,values):
        return json.dumps(values,sort_keys=self._sort_keys,indent=self._indent)
        
    def convert_to_json_as_file(self,values,filename):
        file=open(filename,'w')
        result=json.dump(values,file,sort_keys=self._sort_keys,indent=self._indent)
        file.close()

class JsonParser(object):

    def __init__(self,encoding='utf-8'):
        self._encoding=encoding
        
    def parse_to_values(self,json_str):
        return json.loads(json_str,encoding=self._encoding)
        
    def parse_to_values_by_file(self,filename):
        file=open(filename,'r')
        result=json.load(file)
        file.close()
        return result


class XmlEntity(object):
    def __init__(self,tag,attrib,text):
        
class XmlParser(object):
    
    def __init__(self,_xmlname):
        self.xml_tree=ET.parse(_xmlname)
        self._root=xml_tree.getroot()
        
    def reset_xml_root(self,_xmlstring):
        self.xml_tree=ET.parse(
        self._root=ET.fromstring(_xmlstring)
        
    def create_node(self,tag,attrib,text):
        element=ET.Element(tag,attrib)
        element.text=text
        return element
    
    def add_node(self,parent,tag,attrib,text):
        element=self.create_node(tag,attrib,text)
        if parent:
            parent.append(element)
        
    def find_elements(self,tags):
        return self._root.findall(tags)
        
    def create_dict(self):
        dict_new={}
        list_new=[]
        for child in self._root:
            dict_init={}
            dict_init[child.tag]=[child.text,child.attrib]
        for key,value in enumerate(self._root):
            dict_init={}
            list_init=[]
            for item in value:
                list_init.append([item.tag,item.text])
                for lists in list_init:
                    dict_init[lists[0]] = lists[1]
            dict_new[key]=dict_init
        return dict_new
    
    def get_dict(self,element):
        dict_temp={}
        if len(element.getchildren()) == 0:
            
        for child in element:
            
        
    def dict_to_xml(self,input_dict,root_tag,node_tag):
        root_name = ET.Element(root_tag)
        for (k, v) in input_dict.items():
            node_name = ET.SubElement(root_name, node_tag)
            for key, val in sorted(v.items(),key=lambda e:e[0],reverse=True):
                key = ET.SubElement(node_name, key)
                key.text = val
        return root_name
    
    def out_xml(self,root):
        """格式化root转换为xml文件"""
        rough_string = ET.tostring(root, 'utf-8')
        reared_content = MD.parseString(rough_string)
        with open(out_file, 'w+') as fs:
            reared_content.writexml(fs, addindent=" ", newl="\n", encoding="utf-8")
        return True

        
    
        
