
import json

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
        
