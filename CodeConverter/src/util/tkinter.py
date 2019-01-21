#!/usr/bin/env python3

import platform
import sys
import html
from PyQt5.QtCore import QSize, Qt,pyqtSignal
from PyQt5.QtGui import QColor, QFont,QFontMetrics, QIcon, QKeySequence, QPixmap,QTextCharFormat
from PyQt5.QtWidgets import QAction,QApplication,QMenu,QTextEdit



class RichTextLineEdit(QTextEdit):
    returnPressed=pyqtSignal()
    (Bold, Italic, Underline, StrikeOut, Monospaced, Sans, Serif,
     NoSuperOrSubscript, Subscript, Superscript) = range(10)


    def __init__(self, parent=None):
        super(RichTextLineEdit, self).__init__(parent)

        self.monofamily = "courier"
        self.sansfamily = "helvetica"
        self.seriffamily = "times"
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setTabChangesFocus(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        fm = QFontMetrics(self.font())
        h = int(fm.height() * (1.4 if platform.system() == "Windows"
                                   else 1.2))
        self.setMinimumHeight(h)
        self.setMaximumHeight(int(h * 1.2))
        self.setToolTip("Press <b>Ctrl+M</b> for the text effects "
                "menu and <b>Ctrl+K</b> for the color menu")


    def toggleItalic(self):
        self.setFontItalic(not self.fontItalic())


    def toggleUnderline(self):
        self.setFontUnderline(not self.fontUnderline())


    def toggleBold(self):
        self.setFontWeight(QFont.Normal
                if self.fontWeight() > QFont.Normal else QFont.Bold)


    def sizeHint(self):
        return QSize(self.document().idealWidth() + 5,
                     self.maximumHeight())


    def minimumSizeHint(self):
        fm = QFontMetrics(self.font())
        return QSize(fm.width("WWWW"), self.minimumHeight())


    def contextMenuEvent(self, event):
        self.textEffectMenu()


    def keyPressEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            handled = False
            if event.key() == Qt.Key_B:
                self.toggleBold()
                handled = True
            elif event.key() == Qt.Key_I:
                self.toggleItalic()
                handled = True
            elif event.key() == Qt.Key_K:
                self.colorMenu()
                handled = True
            elif event.key() == Qt.Key_M:
                self.textEffectMenu()
                handled = True
            elif event.key() == Qt.Key_U:
                self.toggleUnderline()
                handled = True
            if handled:
                event.accept()
                return
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.returnPressed.emit()
            event.accept()
        else:
            QTextEdit.keyPressEvent(self, event)


    def colorMenu(self):
        pixmap = QPixmap(22, 22)
        menu = QMenu("Colour")
        for text, color in (
                ("&Black", Qt.black),
                ("B&lue", Qt.blue),
                ("Dark Bl&ue", Qt.darkBlue),
                ("&Cyan", Qt.cyan),
                ("Dar&k Cyan", Qt.darkCyan),
                ("&Green", Qt.green),
                ("Dark Gr&een", Qt.darkGreen),
                ("M&agenta", Qt.magenta),
                ("Dark Mage&nta", Qt.darkMagenta),
                ("&Red", Qt.red),
                ("&Dark Red", Qt.darkRed)):
            color = QColor(color)
            pixmap.fill(color)
            action = menu.addAction(QIcon(pixmap), text, self.setColor)
            action.setData(color)
        self.ensureCursorVisible()
        menu.exec_(self.viewport().mapToGlobal(
                   self.cursorRect().center()))


    def setColor(self):
        action = self.sender()
        if action is not None and isinstance(action, QAction):
            color = QColor(action.data())
            if color.isValid():
                self.setTextColor(color)


    def textEffectMenu(self):
        format = self.currentCharFormat()
        menu = QMenu("Text Effect")
        for text, shortcut, data, checked in (
                ("&Bold", "Ctrl+B", RichTextLineEdit.Bold,
                 self.fontWeight() > QFont.Normal),
                ("&Italic", "Ctrl+I", RichTextLineEdit.Italic,
                 self.fontItalic()),
                ("Strike &out", None, RichTextLineEdit.StrikeOut,
                 format.fontStrikeOut()),
                ("&Underline", "Ctrl+U", RichTextLineEdit.Underline,
                 self.fontUnderline()),
                ("&Monospaced", None, RichTextLineEdit.Monospaced,
                 format.fontFamily() == self.monofamily),
                ("&Serifed", None, RichTextLineEdit.Serif,
                 format.fontFamily() == self.seriffamily),
                ("S&ans Serif", None, RichTextLineEdit.Sans,
                 format.fontFamily() == self.sansfamily),
                ("&No super or subscript", None,
                 RichTextLineEdit.NoSuperOrSubscript,
                 format.verticalAlignment() ==
                 QTextCharFormat.AlignNormal),
                ("Su&perscript", None, RichTextLineEdit.Superscript,
                 format.verticalAlignment() ==
                 QTextCharFormat.AlignSuperScript),
                ("Subs&cript", None, RichTextLineEdit.Subscript,
                 format.verticalAlignment() ==
                 QTextCharFormat.AlignSubScript)):
            action = menu.addAction(text, self.setTextEffect)
            if shortcut is not None:
                action.setShortcut(QKeySequence(shortcut))
            action.setData(data)
            action.setCheckable(True)
            action.setChecked(checked)
        self.ensureCursorVisible()
        menu.exec_(self.viewport().mapToGlobal(
                   self.cursorRect().center()))


    def setTextEffect(self):
        action = self.sender()
        if action is not None and isinstance(action, QAction):
            what = action.data()
            if what == RichTextLineEdit.Bold:
                self.toggleBold()
                return
            if what == RichTextLineEdit.Italic:
                self.toggleItalic()
                return
            if what == RichTextLineEdit.Underline:
                self.toggleUnderline()
                return
            format = self.currentCharFormat()
            if what == RichTextLineEdit.Monospaced:
                format.setFontFamily(self.monofamily)
            elif what == RichTextLineEdit.Serif:
                format.setFontFamily(self.seriffamily)
            elif what == RichTextLineEdit.Sans:
                format.setFontFamily(self.sansfamily)
            if what == RichTextLineEdit.StrikeOut:
                format.setFontStrikeOut(not format.fontStrikeOut())
            if what == RichTextLineEdit.NoSuperOrSubscript:
                format.setVerticalAlignment(
                        QTextCharFormat.AlignNormal)
            elif what == RichTextLineEdit.Superscript:
                format.setVerticalAlignment(
                        QTextCharFormat.AlignSuperScript)
            elif what == RichTextLineEdit.Subscript:
                format.setVerticalAlignment(
                        QTextCharFormat.AlignSubScript)
            self.mergeCurrentCharFormat(format)


    def toSimpleHtml(self):
        htmltext = ""
        black = QColor(Qt.black)
        block = self.document().begin()
        while block.isValid():
            iterator = block.begin()
            while iterator != block.end():
                fragment = iterator.fragment()
                if fragment.isValid():
                    format = fragment.charFormat()
                    family = format.fontFamily()
                    color = format.foreground().color()                  
                    text=html.escape(fragment.text())
                    if (format.verticalAlignment() ==
                        QTextCharFormat.AlignSubScript):
                        text = "<sub>{0}</sub>".format(text)
                    elif (format.verticalAlignment() ==
                          QTextCharFormat.AlignSuperScript):
                        text = "<sup>{0}</sup>".format(text)
                    if format.fontUnderline():
                        text = "<u>{0}</u>".format(text)
                    if format.fontItalic():
                        text = "<i>{0}</i>".format(text)
                    if format.fontWeight() > QFont.Normal:
                        text = "<b>{0}</b>".format(text)
                    if format.fontStrikeOut():
                        text = "<s>{0}</s>".format(text)
                    if color != black or family:
                        attribs = ""
                        if color != black:
                            attribs += ' color="{0}"'.format(color.name())
                        if family:
                            attribs += ' face="{0}"'.format(family)
                        text = "<font{0}>{1}</font>".format(attribs,text)
                    htmltext += text
                iterator += 1
            block = block.next()
        return htmltext

if __name__ == "__main__":
    def printout(lineedit):
        print(str(lineedit.toHtml()))
        print(str(lineedit.toPlainText()))
        print(str(lineedit.toSimpleHtml()))                
    app = QApplication(sys.argv)
    lineedit = RichTextLineEdit()
    lineedit.returnPressed.connect(lambda:printout(lineedit))
    lineedit.show()
    lineedit.setWindowTitle("RichTextEdit")
    app.exec_()
=========================================================================================
#!/usr/bin/env python3

import gzip
import os
import platform
import sys
from PyQt5.QtCore import (QAbstractTableModel, QDateTime, QModelIndex,
        QSize, QTimer, QVariant, Qt,pyqtSignal)
from PyQt5.QtGui import ( QColor, QCursor, QFont,
        QFontDatabase, QFontMetrics, QPainter, QPalette, QPixmap)
from PyQt5.QtWidgets import QApplication,QDialog,QHBoxLayout, QLabel, QMessageBox,QScrollArea, QSplitter, QTableView,QWidget


(TIMESTAMP, TEMPERATURE, INLETFLOW, TURBIDITY, CONDUCTIVITY,
 COAGULATION, RAWPH, FLOCCULATEDPH) = range(8)

TIMESTAMPFORMAT = "yyyy-MM-dd hh:mm"


class WaterQualityModel(QAbstractTableModel):

    def __init__(self, filename):
        super(WaterQualityModel, self).__init__()
        self.filename = filename
        self.results = []


    def load(self):
        self.beginResetModel()
        exception = None
        fh = None
        try:
            if not self.filename:
                raise IOError("no filename specified for loading")
            self.results = []
            line_data = gzip.open(self.filename).read()
            for line in line_data.decode("utf8").splitlines():
                parts = line.rstrip().split(",")
                date = QDateTime.fromString(parts[0] + ":00",
                                            Qt.ISODate)

                result = [date]
                for part in parts[1:]:
                    result.append(float(part))
                self.results.append(result)

        except (IOError, ValueError) as e:
            exception = e
        finally:
            if fh is not None:
                fh.close()
            self.endResetModel()
            if exception is not None:
                raise exception


    def data(self, index, role=Qt.DisplayRole):
        if (not index.isValid() or
            not (0 <= index.row() < len(self.results))):
            return QVariant()
        column = index.column()
        result = self.results[index.row()]
        if role == Qt.DisplayRole:
            item = result[column]
            if column == TIMESTAMP:
                #item = item.toString(TIMESTAMPFORMAT)
                item=item
            else:
                #item = QString("%1").arg(item, 0, "f", 2)
                item = "{0:.2f}".format(item)
            return item
        elif role == Qt.TextAlignmentRole:
            if column != TIMESTAMP:
                return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
        elif role == Qt.TextColorRole and column == INLETFLOW:
            if result[column] < 0:
                return QVariant(QColor(Qt.red))
        elif (role == Qt.TextColorRole and
              column in (RAWPH, FLOCCULATEDPH)):
            ph = result[column]
            if ph < 7:
                return QVariant(QColor(Qt.red))
            elif ph >= 8:
                return QVariant(QColor(Qt.blue))
            else:
                return QVariant(QColor(Qt.darkGreen))
        return QVariant()


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == TIMESTAMP:
                return "Timestamp"
            elif section == TEMPERATURE:
                return "\u00B0" +"C"
            elif section == INLETFLOW:
                return "Inflow"
            elif section == TURBIDITY:
                return "NTU"
            elif section == CONDUCTIVITY:
                return "\u03BCS/cm"
            elif section == COAGULATION:
                return "mg/L"
            elif section == RAWPH:
                return "Raw Ph"
            elif section == FLOCCULATEDPH:
                return "Floc Ph"
        return int(section + 1)


    def rowCount(self, index=QModelIndex()):
        return len(self.results)


    def columnCount(self, index=QModelIndex()):
        return 8


class WaterQualityView(QWidget):
    clicked = pyqtSignal(QModelIndex)
    FLOWCHARS = (chr(0x21DC), chr(0x21DD), chr(0x21C9))

    def __init__(self, parent=None):
        super(WaterQualityView, self).__init__(parent)
        self.scrollarea = None
        self.model = None
        self.setFocusPolicy(Qt.StrongFocus)
        self.selectedRow = -1
        self.flowfont = self.font()
        size = self.font().pointSize()
        if platform.system() == "Windows":
            fontDb = QFontDatabase()
            for face in [face.toLower() for face in fontDb.families()]:
                if face.contains("unicode"):
                    self.flowfont = QFont(face, size)
                    break
            else:
                self.flowfont = QFont("symbol", size)
                WaterQualityView.FLOWCHARS = (chr(0xAC), chr(0xAE),
                                              chr(0xDE))


    def setModel(self, model):
        self.model = model
        #self.connect(self.model,
        #        SIGNAL("dataChanged(QModelIndex,QModelIndex)"),
        #        self.setNewSize)
        self.model.dataChanged.connect(self.setNewSize)
        #self.connect(self.model, SIGNAL("modelReset()"), self.setNewSize)
        self.model.modelReset.connect(self.setNewSize)
        self.setNewSize()


    def setNewSize(self):
        self.resize(self.sizeHint())
        self.update()
        self.updateGeometry()


    def minimumSizeHint(self):
        size = self.sizeHint()
        fm = QFontMetrics(self.font())
        size.setHeight(fm.height() * 3)
        return size


    def sizeHint(self):
        fm = QFontMetrics(self.font())
        size = fm.height()
        return QSize(fm.width("9999-99-99 99:99 ") + (size * 4),
                     (size / 4) + (size * self.model.rowCount()))


    def paintEvent(self, event):
        if self.model is None:
            return
        fm = QFontMetrics(self.font())
        timestampWidth = fm.width("9999-99-99 99:99 ")
        size = fm.height()
        indicatorSize = int(size * 0.8)
        offset = int(1.5 * (size - indicatorSize))
        minY = event.rect().y()
        maxY = minY + event.rect().height() + size
        minY -= size
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        y = 0
        for row in range(self.model.rowCount()):
            x = 0
            if minY <= y <= maxY:
                painter.save()
                painter.setPen(self.palette().color(QPalette.Text))
                if row == self.selectedRow:
                    painter.fillRect(x, y + (offset * 0.8),
                            self.width(), size, self.palette().highlight())
                    painter.setPen(self.palette().color(
                            QPalette.HighlightedText))
                #timestamp = self.model.data(
                        #self.model.index(row, TIMESTAMP)).toDateTime()
                timestamp = self.model.data(self.model.index(row, TIMESTAMP))       
                painter.drawText(x, y + size,
                        timestamp.toString(TIMESTAMPFORMAT))
                #print(timestamp.toString(TIMESTAMPFORMAT))
                x += timestampWidth
                temperature = self.model.data(
                        self.model.index(row, TEMPERATURE))
                #temperature = temperature.toDouble()[0]
                temperature = float(temperature)
                if temperature < 20:
                    color = QColor(0, 0,
                            int(255 * (20 - temperature) / 20))
                elif temperature > 25:
                    color = QColor(int(255 * temperature / 100), 0, 0)
                else:
                    color = QColor(0, int(255 * temperature / 100), 0)
                painter.setPen(Qt.NoPen)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize,
                                    indicatorSize)
                x += size
                rawPh = self.model.data(self.model.index(row, RAWPH))
                #rawPh = rawPh.toDouble()[0]
                rawPh = float(rawPh)
                if rawPh < 7:
                    color = QColor(int(255 * rawPh / 10), 0, 0)
                elif rawPh >= 8:
                    color = QColor(0, 0, int(255 * rawPh / 10))
                else:
                    color = QColor(0, int(255 * rawPh / 10), 0)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize,
                                    indicatorSize)
                x += size
                flocPh = self.model.data(
                        self.model.index(row, FLOCCULATEDPH))
                #flocPh = flocPh.toDouble()[0]
                flocPh = float(flocPh)
                if flocPh < 7:
                    color = QColor(int(255 * flocPh / 10), 0, 0)
                elif flocPh >= 8:
                    color = QColor(0, 0, int(255 * flocPh / 10))
                else:
                    color = QColor(0, int(255 * flocPh / 10), 0)
                painter.setBrush(color)
                painter.drawEllipse(x, y + offset, indicatorSize,
                                    indicatorSize)
                painter.restore()
                painter.save()
                x += size
                flow = self.model.data(
                        self.model.index(row, INLETFLOW))
                #flow = flow.toDouble()[0]
                flow = float(flow)
                char = None
                if flow <= 0:
                    char = WaterQualityView.FLOWCHARS[0]
                elif flow < 3.6:
                    char = WaterQualityView.FLOWCHARS[1]
                elif flow > 4.7:
                    char = WaterQualityView.FLOWCHARS[2]
                if char is not None:
                    painter.setFont(self.flowfont)
                    painter.drawText(x, y + size, char)
                painter.restore()
            y += size
            if y > maxY:
                break


    def mousePressEvent(self, event):
        fm = QFontMetrics(self.font())
        self.selectedRow = event.y() // fm.height()
        self.update()
        #self.emit(SIGNAL("clicked(QModelIndex)"),
        #          self.model.index(self.selectedRow, 0))
        self.clicked.emit(self.model.index(self.selectedRow, 0))



    def keyPressEvent(self, event):
        if self.model is None:
            return
        row = -1
        if event.key() == Qt.Key_Up:
            row = max(0, self.selectedRow - 1)
        elif event.key() == Qt.Key_Down:
            row = min(self.selectedRow + 1, self.model.rowCount() - 1)
        if row != -1 and row != self.selectedRow:
            self.selectedRow = row
            if self.scrollarea is not None:
                fm = QFontMetrics(self.font())
                y = fm.height() * self.selectedRow
                print(y)
                self.scrollarea.ensureVisible(0, y)
            self.update()
            #self.emit(SIGNAL("clicked(QModelIndex)"),
            #          self.model.index(self.selectedRow, 0))
            self.clicked.emit(self.model.index(self.selectedRow, 0))
        else:
            QWidget.keyPressEvent(self, event)


class MainForm(QDialog):

    def __init__(self, parent=None):
        super(MainForm, self).__init__(parent)

        self.model = WaterQualityModel(os.path.join(
                os.path.dirname(__file__), "waterdata.csv.gz"))
        self.tableView = QTableView()
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setModel(self.model)
        self.waterView = WaterQualityView()
        self.waterView.setModel(self.model)
        scrollArea = QScrollArea()
        scrollArea.setBackgroundRole(QPalette.Light)
        scrollArea.setWidget(self.waterView)
        self.waterView.scrollarea = scrollArea

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.tableView)
        splitter.addWidget(scrollArea)
        splitter.setSizes([600, 250])
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        self.setWindowTitle("Water Quality Data")
        QTimer.singleShot(0, self.initialLoad)


    def initialLoad(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        splash = QLabel(self)
        pixmap = QPixmap(os.path.join(os.path.dirname(__file__),
                "iss013-e-14802.jpg"))
        #print(os.path.join(os.path.dirname(__file__),
        #        "iss013-e-14802.jpg"))
        splash.setPixmap(pixmap)
        splash.setWindowFlags(Qt.SplashScreen)
        splash.move(self.x() + ((self.width() - pixmap.width()) / 2),
                    self.y() + ((self.height() - pixmap.height()) / 2))
        splash.show()
        QApplication.processEvents()
        try:
            self.model.load()
        except IOError as e:
            QMessageBox.warning(self, "Water Quality - Error", e)
        else:
            self.tableView.resizeColumnsToContents()
        splash.close()
        QApplication.processEvents()
        QApplication.restoreOverrideCursor()


app = QApplication(sys.argv)
form = MainForm()
form.resize(850, 620)
form.show()
app.exec_()
============================================================================================
print df.columns.size#列数 2
print df.iloc[:,0].size#行数 3
print df.ix[[0]].index.values[0]#索引值 0
print df.ix[[0]].values[0][0]#第一行第一列的值 11
print df.ix[[1]].values[0][1]#第二行第二列的值 121
============================================================================================
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

===============================================================================

#!/usr/bin/env python3

import os
import sys
from PyQt5.QtCore import (QEvent, QFile, QFileInfo, QIODevice, QRegExp,
                          QTextStream,Qt)
from PyQt5.QtWidgets import (QAction, QApplication,  QFileDialog,
                             QMainWindow, QMessageBox, QTextEdit)
from PyQt5.QtGui import QFont, QIcon,QColor,QKeySequence,QSyntaxHighlighter,QTextCharFormat,QTextCursor
import qrc_resources


__version__ = "1.1.0"


class PythonHighlighter(QSyntaxHighlighter):

    Rules = []
    Formats = {}

    def __init__(self, parent=None):
        super(PythonHighlighter, self).__init__(parent)

        self.initializeFormats()

        KEYWORDS = ["and", "as", "assert", "break", "class",
                "continue", "def", "del", "elif", "else", "except",
                "exec", "finally", "for", "from", "global", "if",
                "import", "in", "is", "lambda", "not", "or", "pass",
                "print", "raise", "return", "try", "while", "with",
                "yield"]
        BUILTINS = ["abs", "all", "any", "basestring", "bool",
                "callable", "chr", "classmethod", "cmp", "compile",
                "complex", "delattr", "dict", "dir", "divmod",
                "enumerate", "eval", "execfile", "exit", "file",
                "filter", "float", "frozenset", "getattr", "globals",
                "hasattr", "hex", "id", "int", "isinstance",
                "issubclass", "iter", "len", "list", "locals", "map",
                "max", "min", "object", "oct", "open", "ord", "pow",
                "property", "range", "reduce", "repr", "reversed",
                "round", "set", "setattr", "slice", "sorted",
                "staticmethod", "str", "sum", "super", "tuple", "type",
                "vars", "zip"] 
        CONSTANTS = ["False", "True", "None", "NotImplemented",
                     "Ellipsis"]

        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % keyword for keyword in KEYWORDS])),
                "keyword"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % builtin for builtin in BUILTINS])),
                "builtin"))
        PythonHighlighter.Rules.append((QRegExp(
                "|".join([r"\b%s\b" % constant
                for constant in CONSTANTS])), "constant"))
        PythonHighlighter.Rules.append((QRegExp(
                r"\b[+-]?[0-9]+[lL]?\b"
                r"|\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b"
                r"|\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b"),
                "number"))
        PythonHighlighter.Rules.append((QRegExp(
                r"\bPyQt4\b|\bQt?[A-Z][a-z]\w+\b"), "pyqt"))
        PythonHighlighter.Rules.append((QRegExp(r"\b@\w+\b"),
                "decorator"))
        stringRe = QRegExp(r"""(?:'[^']*'|"[^"]*")""")
        stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((stringRe, "string"))
        self.stringRe = QRegExp(r"""(:?"["]".*"["]"|'''.*''')""")
        self.stringRe.setMinimal(True)
        PythonHighlighter.Rules.append((self.stringRe, "string"))
        self.tripleSingleRe = QRegExp(r"""'''(?!")""")
        self.tripleDoubleRe = QRegExp(r'''"""(?!')''')


    @staticmethod
    def initializeFormats():
        baseFormat = QTextCharFormat()
        baseFormat.setFontFamily("courier")
        baseFormat.setFontPointSize(12)
        for name, color in (("normal", Qt.black),
                ("keyword", Qt.darkBlue), ("builtin", Qt.darkRed),
                ("constant", Qt.darkGreen),
                ("decorator", Qt.darkBlue), ("comment", Qt.darkGreen),
                ("string", Qt.darkYellow), ("number", Qt.darkMagenta),
                ("error", Qt.darkRed), ("pyqt", Qt.darkCyan)):
            format = QTextCharFormat(baseFormat)
            format.setForeground(QColor(color))
            if name in ("keyword", "decorator"):
                format.setFontWeight(QFont.Bold)
            if name == "comment":
                format.setFontItalic(True)
            PythonHighlighter.Formats[name] = format


    def highlightBlock(self, text):
        NORMAL, TRIPLESINGLE, TRIPLEDOUBLE, ERROR = range(4)

        textLength = len(text)
        prevState = self.previousBlockState()

        self.setFormat(0, textLength,
                       PythonHighlighter.Formats["normal"])

        if text.startswith("Traceback") or text.startswith("Error: "):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["error"])
            return
        if (prevState == ERROR and
            not (text.startswith(sys.ps1) or text.startswith("#"))):
            self.setCurrentBlockState(ERROR)
            self.setFormat(0, textLength,
                           PythonHighlighter.Formats["error"])
            return

        for regex, format in PythonHighlighter.Rules:
            i = regex.indexIn(text)
            while i >= 0:
                length = regex.matchedLength()
                self.setFormat(i, length,
                               PythonHighlighter.Formats[format])
                i = regex.indexIn(text, i + length)

        # Slow but good quality highlighting for comments. For more
        # speed, comment this out and add the following to __init__:
        # PythonHighlighter.Rules.append((QRegExp(r"#.*"), "comment"))
        if not text:
            pass
        elif text[0] == "#":
            self.setFormat(0, len(text),
                           PythonHighlighter.Formats["comment"])
        else:
            stack = []
            for i, c in enumerate(text):
                if c in ('"', "'"):
                    if stack and stack[-1] == c:
                        stack.pop()
                    else:
                        stack.append(c)
                elif c == "#" and len(stack) == 0:
                    self.setFormat(i, len(text),
                                   PythonHighlighter.Formats["comment"])
                    break

        self.setCurrentBlockState(NORMAL)

        if self.stringRe.indexIn(text) != -1:
            return
        # This is fooled by triple quotes inside single quoted strings
        for i, state in ((self.tripleSingleRe.indexIn(text),
                          TRIPLESINGLE),
                         (self.tripleDoubleRe.indexIn(text),
                          TRIPLEDOUBLE)):
            if self.previousBlockState() == state:
                if i == -1:
                    i = text.length()
                    self.setCurrentBlockState(state)
                self.setFormat(0, i + 3,     
                               PythonHighlighter.Formats["string"])
            elif i > -1:
                self.setCurrentBlockState(state)
                self.setFormat(i, text.length(),
                               PythonHighlighter.Formats["string"])


    def rehighlight(self):
        QApplication.setOverrideCursor(QCursor(
                                                    Qt.WaitCursor))
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()


class TextEdit(QTextEdit):

    def __init__(self, parent=None):
        super(TextEdit, self).__init__(parent)


    def event(self, event):
        if (event.type() == QEvent.KeyPress and
            event.key() == Qt.Key_Tab):
            cursor = self.textCursor()
            cursor.insertText("    ")
            return True
        return QTextEdit.event(self, event)


class MainWindow(QMainWindow):

    def __init__(self, filename=None, parent=None):
        super(MainWindow, self).__init__(parent)

        font = QFont("Courier", 11)
        font.setFixedPitch(True)
        self.editor = TextEdit()
        self.editor.setFont(font)
        self.highlighter = PythonHighlighter(self.editor.document())
        self.setCentralWidget(self.editor)

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        fileNewAction = self.createAction("&New...", self.fileNew,
                QKeySequence.New, "filenew", "Create a Python file")
        fileOpenAction = self.createAction("&Open...", self.fileOpen,
                QKeySequence.Open, "fileopen",
                "Open an existing Python file")
        self.fileSaveAction = self.createAction("&Save", self.fileSave,
                QKeySequence.Save, "filesave", "Save the file")
        self.fileSaveAsAction = self.createAction("Save &As...",
                self.fileSaveAs, icon="filesaveas",
                tip="Save the file using a new name")
        fileQuitAction = self.createAction("&Quit", self.close,
                "Ctrl+Q", "filequit", "Close the application")
        self.editCopyAction = self.createAction("&Copy",
                self.editor.copy, QKeySequence.Copy, "editcopy",
                "Copy text to the clipboard")
        self.editCutAction = self.createAction("Cu&t", self.editor.cut,
                QKeySequence.Cut, "editcut",
                "Cut text to the clipboard")
        self.editPasteAction = self.createAction("&Paste",
                self.editor.paste, QKeySequence.Paste, "editpaste",
                "Paste in the clipboard's text")
        self.editIndentAction = self.createAction("&Indent",
                self.editIndent, "Ctrl+]", "editindent",
                "Indent the current line or selection")
        self.editUnindentAction = self.createAction("&Unindent",
                self.editUnindent, "Ctrl+[", "editunindent",
                "Unindent the current line or selection")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileNewAction, fileOpenAction,
                self.fileSaveAction, self.fileSaveAsAction, None,
                fileQuitAction))
        editMenu = self.menuBar().addMenu("&Edit")
        self.addActions(editMenu, (self.editCopyAction,
                self.editCutAction, self.editPasteAction, None,
                self.editIndentAction, self.editUnindentAction))
        fileToolbar = self.addToolBar("File")
        fileToolbar.setObjectName("FileToolBar")
        self.addActions(fileToolbar, (fileNewAction, fileOpenAction,
                                      self.fileSaveAction))
        editToolbar = self.addToolBar("Edit")
        editToolbar.setObjectName("EditToolBar")
        self.addActions(editToolbar, (self.editCopyAction,
                self.editCutAction, self.editPasteAction, None,
                self.editIndentAction, self.editUnindentAction))


        self.editor.selectionChanged.connect(self.updateUi)
        self.editor.document().modificationChanged.connect(self.updateUi)
        QApplication.clipboard().dataChanged.connect(self.updateUi)

        self.resize(800, 600)
        self.setWindowTitle("Python Editor")
        self.filename = filename
        if self.filename is not None:
            self.loadFile()
        self.updateUi()


    def updateUi(self, arg=None):
        self.fileSaveAction.setEnabled(
                self.editor.document().isModified())
        enable = not self.editor.document().isEmpty()
        self.fileSaveAsAction.setEnabled(enable)
        self.editIndentAction.setEnabled(enable)
        self.editUnindentAction.setEnabled(enable)
        enable = self.editor.textCursor().hasSelection()
        self.editCopyAction.setEnabled(enable)
        self.editCutAction.setEnabled(enable)
        self.editPasteAction.setEnabled(self.editor.canPaste())


    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/{0}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def closeEvent(self, event):
        if not self.okToContinue():
            event.ignore()


    def okToContinue(self):
        if self.editor.document().isModified():
            reply = QMessageBox.question(self,
                            "Python Editor - Unsaved Changes",
                            "Save unsaved changes?",
                            QMessageBox.Yes|QMessageBox.No|
                            QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                return self.fileSave()
        return True


    def fileNew(self):
        if not self.okToContinue():
            return
        document = self.editor.document()
        document.clear()
        document.setModified(False)
        self.filename = None
        self.setWindowTitle("Python Editor - Unnamed")
        self.updateUi()


    def fileOpen(self):
        if not self.okToContinue():
            return
        dir = (os.path.dirname(self.filename)
               if self.filename is not None else ".")
        fname = str(QFileDialog.getOpenFileName(self,
                "Python Editor - Choose File", dir,
                "Python files (*.py *.pyw)")[0])
        if fname:
            self.filename = fname
            self.loadFile()


    def loadFile(self):
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            self.editor.setPlainText(stream.readAll())
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self, "Python Editor -- Load Error",
                    "Failed to load {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()
        self.setWindowTitle("Python Editor - {0}".format(
                QFileInfo(self.filename).fileName()))


    def fileSave(self):
        if self.filename is None:
            return self.fileSaveAs()
        fh = None
        try:
            fh = QFile(self.filename)
            if not fh.open(QIODevice.WriteOnly):
                raise IOError(str(fh.errorString()))
            stream = QTextStream(fh)
            stream.setCodec("UTF-8")
            stream << self.editor.toPlainText()
            self.editor.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self, "Python Editor -- Save Error",
                    "Failed to save {0}: {1}".format(self.filename, e))
            return False
        finally:
            if fh is not None:
                fh.close()
        return True


    def fileSaveAs(self):
        filename = self.filename if self.filename is not None else "."
        filename,filetype = QFileDialog.getSaveFileName(self,
                "Python Editor -- Save File As", filename,
                "Python files (*.py *.pyw)")
        if filename:
            self.filename = filename
            self.setWindowTitle("Python Editor - {0}".format(
                    QFileInfo(self.filename).fileName()))
            return self.fileSave()
        return False


    def editIndent(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.clearSelection()
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.StartOfLine)
            while pos <= end:
                cursor.insertText("    ")
                cursor.movePosition(QTextCursor.Down)
                cursor.movePosition(QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, end - start)
        else:
            pos = cursor.position()
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.insertText("    ")
            cursor.setPosition(pos + 4)
        cursor.endEditBlock()


    def editUnindent(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        if cursor.hasSelection():
            start = pos = cursor.anchor()
            end = cursor.position()
            if start > end:
                start, end = end, start
                pos = start
            cursor.setPosition(pos)
            cursor.movePosition(QTextCursor.StartOfLine)
            while pos <= end:
                cursor.clearSelection()
                cursor.movePosition(QTextCursor.NextCharacter,
                                    QTextCursor.KeepAnchor, 4)
                if cursor.selectedText() == "    ":
                    cursor.removeSelectedText()
                cursor.movePosition(QTextCursor.Down)
                cursor.movePosition(QTextCursor.StartOfLine)
                pos = cursor.position()
            cursor.setPosition(start)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, end - start)
        else:
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.StartOfBlock)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor, 4)
            if cursor.selectedText() == "    ":
                cursor.removeSelectedText()
        cursor.endEditBlock()


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/icon.png"))
    fname = None
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    form = MainWindow(fname)
    form.show()
    app.exec_()


main()
================================================================================
from pygments.lexers import PythonLexver
from pygments.formatters import HtmlFormatter
from pygments import highlight

formatter = HtmlFormatter(encoding='utf-8', style = 'emacs', linenos = True)
code = highlight('print "hello, world"', PythonLexer(), formatter)

print code

css = formatter.get_style_defs()

