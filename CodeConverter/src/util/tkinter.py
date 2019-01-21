
#文本文件的打开,保存和另存；可一键访问历史记录（五个最近的历史记录（不重复））。
import tkinter as tk
#文件选择对话框
import os,json
import tkinter.filedialog
from tkinter import messagebox
#主窗口
root  =tk.Tk()
root.title("Text reader made by yy")
root.geometry('500x500')
##输入窗口（仅仅用作显示）
res = tk.Variable()
entry = tk.Entry(root,textvariable = res,width = 40)
res.set('Selected files:')
entry.pack()
 
def add_path(path1):
	global path_list
	try:
		with open('C:\yy.txt','r') as f:
			path_list = json.load(f)
			if path1 not in path_list:
				while len(path_list) > 4:
					path_list = path_list[1:]
				else:
					path_list.append(path1)
			else:
				pass
		with open('C:\yy.txt', 'w') as f:
			json.dump(path_list, f)
	except:
		with open('C:\yy.txt','w') as f:
			path_list = []
			path_list.append(path1)
			json.dump(path_list,f)

#初始化列表长度
try:
	with open('C:\yy.txt', 'r') as f:
		path_list = json.load(f)
		if len(path_list) < 5:
			while True:
				path_list.append('C:')
				if len(path_list) >= 5:
					break
except:
	path_list = []
 
 
def func1():		#open
	global filename,res
	filename = tkinter.filedialog.askopenfilename(filetypes = [(" please open txt file", "*.txt")])
	add_path(filename)
	try:
		with open(filename,'r') as f:
		 content = f.read()
		text.delete(0.0,tk.END)
		text.insert(tk.INSERT,content)
		basename = os.path.basename(filename)
		res.set('%s'%basename)
		button4.config(text = os.path.basename(path_list[-1]))
		button5.config(text = os.path.basename(path_list[-2]))
		button6.config(text = os.path.basename(path_list[-3]))
		button7.config(text = os.path.basename(path_list[-4]))
		button8.config(text = os.path.basename(path_list[-5]))
 
	except:
		pass
 
def func2():		#save
	with open(filename,'w') as f:
		try:
			f.write(text.get(0.0,tk.END))
			f.flush()
			basename = os.path.basename(filename)
			save_succed = messagebox.showinfo(title='message', message='%s  save succed' % basename)
			print(save_succed)
		except:
			save_error = messagebox.showinfo(title = 'unfortunately ',message = 'save failure')
			print(save_error)
 
#打开历史记录对应的文件
def func3(button,filename):		#open
	global res,button4
	add_path(filename)
	try:
		with open(filename,'r') as f:
		 content = f.read()
		text.delete(0.0,tk.END)
		text.insert(tk.INSERT,content)
		basename = os.path.basename(filename)
		res.set('%s'%basename)
	except:
		pass
 
def save_as():
	filename1 = tkinter.filedialog.asksaveasfilename()
	add_path(filename1)
	with open(filename1, 'w') as f:
		f.write(text.get(0.0, tk.END))
		basename = os.path.basename(filename1)
		save_succed = messagebox.showinfo(title='message', message='%s  saveas  succed' % basename)
		print(save_succed)
#制作底部框体和（打开保存另存）按钮
fm2 = tk.Frame(root)
button1 = tk.Button(fm2,text = 'open',command = func1)
button1.pack(side = "left")
 
button2 = tk.Button(fm2,text = 'save',command = func2)
button2.pack(side = "left")
 
button3 = tk.Button(fm2,text = 'saveas',command = save_as)
button3.pack(side = "left")
 
fm2.pack(side = 'bottom')
 
#制作右侧的历史记录按钮按钮
 
 
#右侧总框架
fm3 = tk.Frame(root)
#右侧label
label_right = tk.Label(fm3,text  = '历史记录 :')
label_right.pack(side = 'top')
#历史文件访问地址获取，通过path_list
a,b,c,d,e = os.path.basename(path_list[-1]),os.path.basename(path_list[-2]),os.path.basename(path_list[-3]),os.path.basename(path_list[-4]),os.path.basename(path_list[-5])
#右侧历史记录的键
#注意lambda花式传参方式
button4 = tk.Button(fm3,text = a,command = lambda func1 = func3:func3(button4,path_list[-1]))
button4.pack(side = "top")
 
button5 = tk.Button(fm3,text = b,command = lambda func1 = func3:func3(button5,path_list[-2]))
button5.pack(side = "top")
 
button6 = tk.Button(fm3,text = c,command = lambda func1 = func3:func3(button6,path_list[-3]))
button6.pack(side = "top")
 
button7 = tk.Button(fm3,text = d,command = lambda func1 = func3:func3(button6,path_list[-4]))
button7.pack(side = "top")
 
button8 = tk.Button(fm3,text = e,command = lambda func1 = func3:func3(button6,path_list[-5]))
button8.pack(side = "top")
 
fm3.pack(side = 'right')
 
 
 
#滚动条
scroll = tk.Scrollbar()
scroll.pack(side = tk.RIGHT,fill = tk.Y)
#文本
text = tk.Text(root,width = 200,height = 20)
text.pack(side = tk.LEFT,fill = tk.Y)
#滚动条和文本相互绑定
scroll.config(command = text.yview)
text.config(yscrollcommand = scroll.set)
 
root.mainloop()

==========================================================================================
from tkinter import *
from tkinter.ttk import *
from 万年历.guess_num import Apps


class App:
    def __init__(self):
        self.windos = Tk()
        self.windos.title("✽万年历 ❀")
        self.windos.geometry("430x400")
        self.lis1 = ["周一", "周二", "周三", "周四", "周五", "周六", "周天"]
        self.images=[]
        self.creat_image_lis()
        self.creat_res()
        self.windos.mainloop()
    def func1(self):
        self.get_total_days(self.a, self.b)
        print(self.lis1[self.get_week(self.a, self.b) - 1])
        self.print_days(self.a, self.b)
    def creat_image_lis(self):
        for i in range(1,13):
            self.images.append("res/%s.png"%i)
    def view_image(self):
        self.ima=PhotoImage(file=self.images[self.b-1])
        self.L3.config(image=self.ima)

    def go(self,*args):

        self.T1.delete(0.0,END)
        try:
            self.a = int(self.C1.get())
            self.b = int(self.C2.get())
            self.func1()
            self.view_image()
        except Exception:
            self.T1.insert(END,"请输入年份和月份")

    def run_game(self):
        a1=Apps()
        if self.windos.quit():#如果主程序关闭
            Apps.windows.quit() #子程序关闭

    def creat_res(self):
        self.L1=Label(self.windos,text="年份:")
        self.L2=Label(self.windos,text="月份:")
        self.L3=Label(self.windos)
        self.T1=Text(self.windos)
        self.T1.place(x=10, y=10, width=280, height=150)
        self.B1 = Button(self.windos, text="显示", command=self.go)
        self.B1.place(x=300, y=80)
        self.B2 = Button(self.windos, text="退出", command=self.windos.quit)
        self.B2.place(x=300, y=130)
        self.B3=Button(self.windos,text="娱乐",command=self.run_game)
        self.B3.place(x=300, y=180)
        self.temp1 = StringVar()
        self.temp2 = StringVar()
        self.C1=Combobox(self.windos,values=[x for x in range(1900,9999)])
        self.C2=Combobox(self.windos,values=[x for x in range(1,13)])
        self.C1.place(x=300, y=30, width=60, height=30)
        self.C2.place(x=375, y=30, width=50, height=30)
        self.L1.place(x=300, y=0, width=70, height=30)
        self.L2.place(x=370, y=0, width=50, height=30)
        self.L3.place(x=10, y=170, width=280, height=220)
==========================================================================================
from tkinter import *

class Btn_def():
    """按键的功能"""
    def save(self, filename, contents):
        """保存文件"""
        try:
            with open(filename, 'w') as file:
                file.write(contents.get('1.0', END))
        except FileNotFoundError:
            pass

    def load(self, filename, contents):
        """打开文件"""
        try:
            with open(filename) as file:
                contents.delete('1.0', END)
                contents.insert(INSERT, file.read())
        except FileNotFoundError:
            pass
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from button_def import Btn_def

top = Tk()
top.title("TEXT EDITOR")

contents = ScrolledText()
contents.pack(side=BOTTOM, expand=True, fill=BOTH)

filename = Entry()
filename.pack(side=LEFT, expand=True, fill=X)

Btn = Btn_def()
btn1 = Button(top, text='open', command=lambda: Btn.load(filename.get(), contents)).pack(side=RIGHT)
btn2 = Button(top, text='save', command=lambda: Btn.save(filename.get(), contents)).pack(side=RIGHT)

top.mainloop()
==========================================================================================
# -*- encoding: utf8 -*-
#python 2.7
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
import os
 
 
filename = ''
 
def author():
    showinfo('author:','sundy')
 
def about():
    showinfo('Copyright:','sundy')
 
def openfile():
    global filename
    filename = askopenfilename(defaultextension = '.txt')
    if filename == '':
        filename = None
    else:
        root.title('FileName:'+os.path.basename(filename))
        textPad.delete(1.0,END)
        f = open(filename,'r')
        textPad.insert(1.0,f.read())
        f.close()
 
def new():
    global filename
    root.title('未命名文件')
    filename = None
    textPad.delete(1.0,END)
 
def save():
    global filename
    try:
        f = open(filename,'w')
        msg = textPad.get(1.0,END)
        f.write(msg)
        f.close()
    except:
        saveas()
 
 
def saveas():
    f = asksaveasfilename(initialfile= '未命名.txt', defaultextension='.txt')
    global filename
    filename = f
    fh = open(f,'w')
    msg = textPad.get(1.0,END)
    fh.write(msg)
    fh.close()
    root.title('FileName:'+os.path.basename(f))
 
def cut():
    textPad.event_generate('<<Cut>>')
 
def copy():
    textPad.event_generate('<<Copy>>')
 
def paste():
    textPad.event_generate('<<Paste>>')
 
def redo():
    textPad.event_generate('<<Redo>>')
 
def undo():
    textPad.event_generate('<<Undo>>')
 
def selectAll():
    textPad.tag_add('sel','1.0',END)
 
def search():
    def dosearch():
        myentry = entry1.get()             #获取查找的内容--string型
        whatever = str(textPad.get(1.0,END))
        # print textPad.index('zxc')
        # print myentry
        # print "%d个"%(whatever.count(myentry))    #计算substr在S中出现的次数
        showinfo("查找结果：","you searched %s, there are %d in the text"%(myentry,whatever.count(myentry)))
        # print whatever.find(myentry)
 
        # teIndex = textPad.index(myentry)
        # textPad.linestart(teIndex)
        # textPad.mark_set('insert', teIndex)
        # textPad.mark_set(myentry,CURRENT + '+5c')
        # textPad.mark_set(myentry,CURRENT + ' wordstart')
    topsearch = Toplevel(root)
    topsearch.geometry('300x30+200+250')
    label1 = Label(topsearch,text='Find')
    label1.grid(row=0, column=0,padx=5)
    entry1 = Entry(topsearch,width=20)
    entry1.grid(row=0, column=1,padx=5)
    button1 = Button(topsearch,text='查找',command=dosearch)
    button1.grid(row=0, column=2)
     
 
root = Tk()
root.title('Sundy Node')
root.geometry("800x500+100+100")
 
#Create Menu
menubar = Menu(root)
root.config(menu = menubar)
 
filemenu = Menu(menubar)
filemenu.add_command(label='新建', accelerator='Ctrl + N', command= new)
filemenu.add_command(label='打开', accelerator='Ctrl + O',command = openfile)
filemenu.add_command(label='保存', accelerator='Ctrl + S', command=save)
filemenu.add_command(label='另存为', accelerator='Ctrl + Shift + S',command=saveas)
menubar.add_cascade(label='文件',menu=filemenu)
 
editmenu = Menu(menubar)
editmenu.add_command(label='撤销', accelerator='Ctrl + Z', command=undo)
editmenu.add_command(label='重做', accelerator='Ctrl + y', command=redo)
editmenu.add_separator()
editmenu.add_command(label = "剪切",accelerator = "Ctrl + X",command=cut)
editmenu.add_command(label = "复制",accelerator = "Ctrl + C", command=copy)
editmenu.add_command(label = "粘贴",accelerator = "Ctrl + V", command= paste)
editmenu.add_separator()
editmenu.add_command(label = "查找",accelerator = "Ctrl + F", command=search)
editmenu.add_command(label = "全选",accelerator = "Ctrl + A", command= selectAll)
menubar.add_cascade(label = "操作",menu = editmenu)
aboutmenu = Menu(menubar)
aboutmenu.add_command(label = "作者", command=author)
aboutmenu.add_command(label = "关于", command = about)
menubar.add_cascade(label = "about",menu=aboutmenu)
 
#toolbar
toolbar = Frame(root, height=25,bg='grey')
shortButton = Button(toolbar, text='打开',command = openfile)
shortButton.pack(side=LEFT, padx=5, pady=5)
 
shortButton = Button(toolbar, text='保存', command = save)
shortButton.pack(side=LEFT)
toolbar.pack(expand=NO,fill=X)
 
#Status Bar
status = Label(root, text='Ln20',bd=1, relief=SUNKEN,anchor=W)
status.pack(side=BOTTOM, fill=X)
 
#linenumber&text
lnlabel =Label(root, width=2, bg='antique white')
lnlabel.pack(side=LEFT, fill=Y)
 
textPad = Text(root, undo=True)
textPad.pack(expand=YES, fill=BOTH)
 
scroll = Scrollbar(textPad)
textPad.config(yscrollcommand= scroll.set)
scroll.config(command = textPad.yview)
scroll.pack(side=RIGHT,fill=Y)
 
root.mainloop()
==========================================================================================
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import os

filename=""

def author():
    showinfo(title="作者",message="木里")

def power():
    showinfo(title="版权信息",message="2017-12-14-14:40 周四 北京邮电大学")

def mynew():
    global top,filename,textPad
    top.title("未命名文件")
    filename=None
    textPad.delete(1.0,END)

def myopen():
    global filename
    filename=askopenfilename(defaultextension=".txt")
    if filename=="":
        filename=None
    else:
        top.title("记事本"+os.path.basename(filename))
        textPad.delete(1.0,END)
        f=open(filename,'r')
        textPad.insert(1.0,f.read())
        f.close()

def mysave():
    global filename
    try:
        f=open(filename,'w')
        msg=textPad.get(1.0,'end')
        f.write(msg)
        f.close()
    except:
        mysaveas()

def mysaveas():
    global filename
    f=asksaveasfilename(initialfile="未命名.txt",defaultextension=".txt")
    filename=f
    fh=open(f,'w')
    msg=textPad.get(1.0,END)
    fh.write(msg)
    fh.close()
    top.title("记事本"+os.path.basename(f))

def cut():
    global textPad
    textPad.event_generate("<<Cut>>")

def copy():
    global textPad
    textPad.event_generate("<<Copy>>")

def paste():
    global textPad
    textPad.event_generate("<<Paste>>")

def undo():
    global textPad
    textPad.event_generate("<<Undo>>")

def redo():
    global textPad
    textPad.event_generate("<<Redo>>")

def select_all():
    global textPad
    # textPad.event_generate("<<Cut>>")
    textPad.tag_add("sel","1.0","end")

def find():
    t=Toplevel(top)
    t.title("查找")
    t.geometry("260x60+200+250")
    t.transient(top)
    Label(t,text="查找：").grid(row=0,column=0,sticky="e")
    v=StringVar()
    e=Entry(t,width=20,textvariable=v)
    e.grid(row=0,column=1,padx=2,pady=2,sticky="we")
    e.focus_set()
    c=IntVar()
    Checkbutton(t,text="不区分大小写",variable=c).grid(row=1,column=1,sticky='e')
    Button(t,text="查找所有",command=lambda:search(v.get(),c.get(),textPad,t,e)).grid(row=0,column=2,sticky="e"+"w",padx=2,pady=2)
    def close_search():
        textPad.tag_remove("match","1.0",END)
        t.destroy()
    t.protocol("WM_DELETE_WINDOW",close_search)

def mypopup(event):
    # global editmenu
    editmenu.tk_popup(event.x_root,event.y_root)

def search(needle,cssnstv,textPad,t,e):
    textPad.tag_remove("match","1.0",END)
    count=0
    if needle:
        pos="1.0"
        while True:
            pos=textPad.search(needle,pos,nocase=cssnstv,stopindex=END)
            if not pos:break
            lastpos=pos+str(len(needle))
            textPad.tag_add("match",pos,lastpos)
            count+=1
            pos=lastpos
        textPad.tag_config('match',fg='yellow',bg="green")
        e.focus_set()
        t.title(str(count)+"个被匹配")

top=Tk()
top.title("记事本")
top.geometry("1000x600+100+50")

menubar=Menu(top)

# 文件功能
filemenu=Menu(top)
filemenu.add_command(label="新建",accelerator="Ctrl+N",command=mynew)
filemenu.add_command(label="打开",accelerator="Ctrl+O",command=myopen)
filemenu.add_command(label="保存",accelerator="Ctrl+S",command=mysave)
filemenu.add_command(label="另存为",accelerator="Ctrl+shift+s",command=mysaveas)
menubar.add_cascade(label="文件",menu=filemenu)

# 编辑功能
editmenu=Menu(top)
editmenu.add_command(label="撤销",accelerator="Ctrl+Z",command=undo)
editmenu.add_command(label="重做",accelerator="Ctrl+Y",command=redo)
editmenu.add_separator()
editmenu.add_command(label="剪切",accelerator="Ctrl+X",command=cut)
editmenu.add_command(label="复制",accelerator="Ctrl+C",command=copy)
editmenu.add_command(label="粘贴",accelerator="Ctrl+V",command=paste)
editmenu.add_separator()
editmenu.add_command(label="查找",accelerator="Ctrl+F",command=find)
editmenu.add_command(label="全选",accelerator="Ctrl+A",command=select_all)
menubar.add_cascade(label="编辑",menu=editmenu)

# 关于 功能
aboutmenu=Menu(top)
aboutmenu.add_command(label="作者",command=author)
aboutmenu.add_command(label="版权",command=power)
menubar.add_cascade(label="关于",menu=aboutmenu)

top['menu']=menubar

shortcutbar=Frame(top,height=25,bg='light sea green')
shortcutbar.pack(expand=NO,fill=X)
Inlabe=Label(top,width=2,bg='antique white')
Inlabe.pack(side=LEFT,anchor='nw',fill=Y)

textPad=Text(top,undo=True)
textPad.pack(expand=YES,fill=BOTH)
scroll=Scrollbar(textPad)
textPad.config(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT,fill=Y)

# 热键绑定
textPad.bind("<Control-N>",mynew)
textPad.bind("<Control-n>",mynew)
textPad.bind("<Control-O>",myopen)
textPad.bind("<Control-o>",myopen)
textPad.bind("<Control-S>",mysave)
textPad.bind("<Control-s>",mysave)
textPad.bind("<Control-A>",select_all)
textPad.bind("<Control-a>",select_all)
textPad.bind("<Control-F>",find)
textPad.bind("<Control-f>",find)

textPad.bind("<Button-3>",mypopup)
top.mainloop()
==========================================================================================
#!/usr/bin/env python
#-*-coding:utf-8 -*-

__version__ = 0.1
__author__ = {'name' : 'Albert Camus',
              'Email' : 'abcamus_dev@163.com',
              'Blog' : '',
              'QQ' : '',
              'Created' : ''}

from json.decoder import errmsg
import sys, tkFileDialog, os
from Tkinter import *
from ImageTk import PhotoImage

class MainUI(Frame):
"""
绘制窗口对象，定义按钮
"""
    def __init__(self, parent):
        Frame.__init__(self, parent)
        #create main menu
        self.menubar = Menu(parent)
        # 'sl' is short for showline
        self.attribute = {'font':'Monaco', 'bg':0x000000, 'sl':False}
        self.fname = 'default.txt'
        # create file menu
        self.fmenu = Menu(self.menubar, tearoff = 0)
        self.fmenu.add_command(label = 'Open', command = self.open)
        #fmenu.add_separator()
        self.fmenu.add_command(label = 'Save', command = self.save)
        self.fmenu.add_command(label = 'Exit', command = self.exit)
        self.menubar.add_cascade(label = "File", menu = self.fmenu)

        # create edit menu
        editmenu = Menu(self.menubar, tearoff = 0)
        editmenu.add_command(label = 'line number', command = self.ShowLineNum)
        self.menubar.add_cascade(label = 'Edit', menu = editmenu)
        # create help menu
        helpmenu = Menu(self.menubar, tearoff = 0)
        helpmenu.add_command(label = 'About The Author', command = self.aboutAuthor)
        self.menubar.add_cascade(label = 'Help', menu = helpmenu)
        parent['menu'] = self.menubar
        # Text config
        self.text = Text(font = self.attribute['font'])
        self.text.pack(fill = BOTH, expand = YES)

    def save(self):
        txtContent = self.text.get(1.0, END)  
        self.saveFile(content = txtContent) 

    def ShowLineNum(self):
        self.linenum = 1.0
        self.text.delete(1.0, END)
        for line in self.filecontent:
            if self.attribute['sl'] is False:
                self.text.insert(self.linenum, str(int(self.linenum))+' '+line)
            else:
                self.text.insert(self.linenum, line)
                self.linenum += 1
                self.attribute['sl'] = not self.attribute['sl']

    def open(self):
        self.filename = tkFileDialog.askopenfilename(initialdir = os.getcwd())
        self.filecontent = self.openFile(fname = self.filename)
        self.linenum = 1.0
        if self.filecontent is not None:
            for line in self.filecontent:
                self.text.insert(self.linenum, line.decode('utf-8'))
                self.linenum += 1
        else:
            print "content is None"

    '''
     The fname is file name with full path  
    ''' 
    def openFile(self, fname = None):
        if fname is None:
            return -1
        self.fname = fname
        try:
            myFile = open(fname, 'r+')
        except IOError, errmsg:
            print 'Open file error:', errmsg
        else:
            content = myFile.readlines()
            myFile.close()
            return content

    def saveFile(self, content = None):  
        if content is None:
            return -1
        myFile = open(self.fname,'w')
        myFile.write(content.encode('utf-8'))
        myFile.flush()
        myFile.close()
        return 0

    def exit(self):
        sys.exit(0)

    def printScale(self, text):
        print 'text = ', text

    def printItem(self):
        print 'add_separator'

    def destroy_ui(self, ui):
        ui.destroy()

    def aboutAuthor(self):
        author_ui = Toplevel()
        author_ui.title('About')
        #author_ui.iconbitmap('icons/48x48.ico')
        author_ui.geometry('200x80')
        about_string = Label(author_ui, text = 'Author: Albert Camus')
        confirmButton = Button(author_ui, text = 'Confirm',
                               command = lambda: self.destroy_ui(author_ui))
        about_string.pack()
        confirmButton.pack()

class Note():
    def __init__(self):
        self.tk = Tk()
        self.tk.title('宙斯的神殿')
        """
        原来实在windows下实现的，移植到Linux Mint下之后，老是报找不到ico文件，网上查了一下，用PhotoImage替代了。
        """
        icon = PhotoImage(file='title.ico')
        self.tk.call('wm', 'iconphoto', self.tk._w, icon)
        #self.tk.iconbitmap(r'/home/camus/github/note-editor/title.ico')

        self.tk.geometry('800x600')
        self.has_sub = False
        self.createUI()
        self.tk.mainloop()

    def popup(self, event):
        self.submenubar.post(event.x_root, event.y_root)

    def SubOpen(self):
        self.subfilename = tkFileDialog.askopenfilename(initialdir = os.getcwd())
        self.filecontent = self.MainText.openFile(fname = self.subfilename)
        if self.filecontent is not None:
            self.MainText.SubText.delete(1.0, END)
            self.linenum = 1.0
            for eachline in self.filecontent:
            self.MainText.SubText.insert(self.linenum, eachline.decode('gb2312'))
                self.linenum += 1

    def CreateSubWin(self):
        if self.has_sub is True:
            # hide the sub window
            self.MainText.SubText.forget()
            self.has_sub = False
        else:
            self.has_sub = True
            self.MainText.SubText.pack(side = 'right', anchor = NW)

    def createUI(self):
        #create main menu
        self.MainText = MainUI(self.tk)

        # special for sub window editor
        self.MainText.SubText = Text(self.MainText.text, bg = 'green')
        self.MainText.menubar.add_command(label = 'subwin', command = self.CreateSubWin)
        self.submenubar = Menu(self.MainText.menubar)
        self.submenubar.add_command(label = 'open', command = self.SubOpen)
        self.tk.bind('<Button-3>', self.popup)

if __name__ == '__main__':  
    Note()
==========================================================================================
#################################################################
#author: 陈月白
#_blogs: http://www.cnblogs.com/chenyuebai/
#################################################################
from tkinter import *
import hashlib
import time

LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("文本处理工具_v1.2   by: 陈月白")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志")
        self.log_label.grid(row=12, column=0)
        #文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,command=self.str_trans_to_md5)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=1, column=11)


    #功能函数
    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0,END).strip().replace("\n","").encode()
        #print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                #print(myMd5_Digest)
                #输出到界面
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,myMd5_Digest)
                self.write_log_to_Text("INFO:str_trans_to_md5 success")
            except:
                self.result_data_Text.delete(1.0,END)
                self.result_data_Text.insert(1.0,"字符串转MD5失败")
        else:
            self.write_log_to_Text("ERROR:str_trans_to_md5 failed")


    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


gui_start()

==========================================================================================
from tkinter import *
from PIL import Image, ImageTk
 
class Window(Frame):
 
    def __init__(self, master= None):
 
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
 
    def init_window(self):
 
        self.master.title("第一个窗体")
 
        self.pack(fill=BOTH, expand=1)
 
        # 实例化一个Menu对象，这个在主窗体添加一个菜单
        menu = Menu(self.master)
        self.master.config(menu=menu)
 
        # 创建File菜单，下面有Save和Exit两个子菜单
        file = Menu(menu)
        file.add_command(label='Save')
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File',menu=file)
 
        # 创建Edit菜单，下面有一个Undo菜单
        edit = Menu(menu)
        edit.add_command(label='Undo')
        edit.add_command(label='Show  Image',command=self.showImg)
        edit.add_command(label='Show  Text',command=self.showTxt)
        menu.add_cascade(label='Edit',menu=edit)
        
 
    def client_exit(self):
        exit()
 
    def showImg(self):
        load = Image.open('pic.jpg') # 我图片放桌面上
        render= ImageTk.PhotoImage(load)
 
        img = Label(self,image=render)
        img.image = render
        img.place(x=0,y=0)
 
    def showTxt(self):
        text = Label(self, text='GUI图形编程')
        text.pack()
 
root = Tk()
root.geometry("400x300")
app = Window(root)
root.mainloop()



