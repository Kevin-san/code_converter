#-*-coding:utf-8-*-

import base64
import hashlib

def encode2base64(string):
	return base64.b64encode(string.encode('utf-8')).decode('utf-8')

def decode2base64(string):
	return base64.b64decode(string.encode('utf-8')).decode('utf-8')

def encode2md5(string):
	return hashlib.md5(string.encode('utf-8')).hexdigest()

