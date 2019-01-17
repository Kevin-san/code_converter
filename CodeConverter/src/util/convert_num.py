#!/opt/python3/bin/python
# -*- coding: utf-8 -*-

import os,sys

def bin2oct(string_num):
	return oct(int(string_num,2))
	
def bin2dec(string_num):
	return int(string_num,2)
	
def bin2hex(string_num):
	return hex(int(string_num,2))
	
def oct2bin(string_num):
	return bin(int(string_num,8))
	
def oct2dec(string_num):
	return int(string_num,8)

def oct2hex(string_num):
	return hex(int(string_num,8))

def dec2bin(string_num):
	return bin(int(string_num,10))

def dec2oct(string_num):
	return oct(int(string_num,10))

def dec2hex(string_num):
	return hex(int(string_num,10))

def hex2bin(string_num):
	return bin(int(string_num,16))

def hex2oct(string_num):
	return oct(int(string_num,16))

def hex2dec(string_num):
	return int(string_num,16)

def strQ2B(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

    
def strB2Q(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 32:  # 全角空格直接转换
                inside_code = 12288
            elif (inside_code >= 33 and inside_code <= 126):  # 全角字符（除空格）根据关系转化
                inside_code += 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

if __name__=='__main__':
	test_bin_str='0b1100100'
	test_oct_str='0o144'
	test_dec_str='100'
	test_hex_str='0x64'
	test_half_str=" !\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
	print("2 %s to 8,10,16" %(test_bin_str))
	print(bin2oct(test_bin_str))
	print(bin2dec(test_bin_str))
	print(bin2hex(test_bin_str))
	
	print("8 %s to 2,10,16" %(test_oct_str))
	print(oct2bin(test_oct_str))
	print(oct2dec(test_oct_str))
	print(oct2hex(test_oct_str))
	
	print("10 %s to 2,8,16" %(test_dec_str))
	print(dec2bin(test_dec_str))
	print(dec2oct(test_dec_str))
	print(dec2hex(test_dec_str))
	
	print("16 %s to 2,8,10" %(test_hex_str))
	print(hex2bin(test_hex_str))
	print(hex2dec(test_hex_str))
	print(hex2oct(test_hex_str))
	
	print(test_half_str)
	test_whole_str=strB2Q(test_half_str)
	file=open('/home/cx24793/convert_num.txt','w+',encoding='utf-8')
	file.write(test_whole_str)
	file.close()
