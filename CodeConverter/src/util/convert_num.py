#!/opt/python3/bin/python
# -*- coding: utf-8 -*-

import os,sys
import re

import qrcode
from PIL import Image
from pyzbar import pyzbar


def make_qr_code_easy(content, save_path=None):
    """
    Generate QR Code by default
    :param content: The content encoded in QR Codeparams
    :param save_path: The path where the generated QR Code image will be saved in.
                      If the path is not given the image will be opened by default.
    """
    img = qrcode.make(data=content)
    if save_path:
        img.save(save_path)
    else:
        img.show()


def make_qr_code(content, save_path=None):
    """
    Generate QR Code by given params
    :param content: The content encoded in QR Code
    :param save_path: The path where the generated QR Code image will be saved in.
                      If the path is not given the image will be opened by default.
    """
    qr_code_maker = qrcode.QRCode(version=2,
                                  error_correction=qrcode.constants.ERROR_CORRECT_M,
                                  box_size=8,
                                  border=1,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    img = qr_code_maker.make_image(fill_color="black", back_color="white")
    if save_path:
        img.save(save_path)
    else:
        img.show()


def make_qr_code_with_icon(content, icon_path, save_path=None):
    """
    Generate QR Code with an icon in the center
    :param content: The content encoded in QR Code
    :param icon_path: The path of icon image
    :param save_path: The path where the generated QR Code image will be saved in.
                      If the path is not given the image will be opened by default.
    :exception FileExistsError: If the given icon_path is not exist.
                                This error will be raised.
    :return:
    """
    if not os.path.exists(icon_path):
        raise FileExistsError(icon_path)

    # First, generate an usual QR Code image
    qr_code_maker = qrcode.QRCode(version=4,
                                  error_correction=qrcode.constants.ERROR_CORRECT_H,
                                  box_size=8,
                                  border=1,
                                  )
    qr_code_maker.add_data(data=content)
    qr_code_maker.make(fit=True)
    qr_code_img = qr_code_maker.make_image(fill_color="black", back_color="white").convert('RGBA')

    # Second, load icon image and resize it
    icon_img = Image.open(icon_path)
    code_width, code_height = qr_code_img.size
    icon_img = icon_img.resize((code_width // 4, code_height // 4), Image.ANTIALIAS)

    # Last, add the icon to original QR Code
    qr_code_img.paste(icon_img, (code_width * 3 // 8, code_width * 3 // 8))

    if save_path:
        qr_code_img.save(save_path)
    else:
        qr_code_img.show()


def decode_qr_code(code_img_path):
    """
    Decode the given QR Code image, and return the content
    :param code_img_path: The path of QR Code image.
    :exception FileExistsError: If the given code_img_path is not exist.
                                This error will be raised.
    :return: The list of decoded objects
    """
    if not os.path.exists(code_img_path):
        raise FileExistsError(code_img_path)

    # Here, set only recognize QR Code and ignore other type of code
    return pyzbar.decode(Image.open(code_img_path), symbols=[pyzbar.ZBarSymbol.QRCODE])

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

def convert(one_string,space_character):    #one_string:输入的字符串；space_character:字符串的间隔符，以其做为分隔标志
    string_list = str(one_string).split(space_character)    #将字符串转化为list
    first = string_list[0].lower()
    others = string_list[1:]
    others_capital = [word.capitalize() for word in others]      #str.capitalize():将字符串的首字母转化为大写
    others_capital[0:0] = [first]
    hump_string = ''.join(others_capital)     #将list组合成为字符串，中间无连接符。
    return hump_string

def hump2underline(hunp_str):
    '''
    驼峰形式字符串转成下划线形式
    :param hunp_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    '''
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub

def underline2hump(underline_str):
    '''
    下划线形式字符串转成驼峰形式
    :param underline_str: 下划线形式字符串
    :return: 驼峰形式字符串
    '''
    if underline_str.isupper():
        underline_str=underline_str.lower()
    # 这里re.sub()函数第二个替换参数用到了一个匿名回调函数，回调函数的参数x为一个匹配对象，返回值为一个处理后的字符串
    sub = re.sub(r'(_\w)',lambda x:x.group(1)[1].upper(),underline_str)
    return sub

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
	
	test_name='ANT_XML'
	humpStr=underline2hump(test_name)
	print(humpStr)
	underlineStr=hump2underline(humpStr)
	print(underlineStr)

	make_qr_code_easy("make_qr_code_easy", "qrcode.png")
	results = decode_qr_code("qrcode.png")
	if len(results):
		print(results[0].data.decode("utf-8"))
	else:
		print("Can not recognize.")
	
	make_qr_code("make_qr_code", "qrcode.png")
	results = decode_qr_code("qrcode.png")
	if len(results):
		print(results[0].data.decode("utf-8"))
	else:
		print("Can not recognize.")
	
	make_qr_code_with_icon("https://blog.csdn.net/Zhipeng_Hou", "icon.jpg", "qrcode.png")
	results = decode_qr_code("qrcode.png")
	if len(results):
		print(results[0].data.decode("utf-8"))
	else:
		print("Can not recognize.")
