# -*- coding: utf-8 -*-


import os
import chardet
import logging
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QFileDialog, QDialog
from about import AboutDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import *
import urllib.parse
import webbrowser
import shelve
import pyperclip
import sys

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')
config = shelve.open('settings')


def close_window():
    logging.info("Exited window")
    QCoreApplication.instance().quit()


class Ui_window(object):
    def __init__(self):
        self.color_ico = None
        self.color = None
        self.find_textLineEdit = None
        self.open_file = None
        self.open_file_ico = None
        self.save_file = None
        self.save_file_ico = None
        self.save_as = None
        self.save_as_ico = None
        self.print = None
        self.print_ico = None
        self.quit = None
        self.quit_ico = None
        self.undo = None
        self.undo_ico = None
        self.redo = None
        self.redo_ico = None
        self.select = None
        self.select_ico = None
        self.cut = None
        self.cut_ico = None
        self.paste = None
        self.paste_ico = None
        self.search = None
        self.search_ico = None
        self.find = None
        self.insert_time = None
        self.auto_change_line = None
        self.font = None
        self.status_bar = None
        self.font_ico = None
        self.copy = None
        self.copy_ico = None
        self.help = None
        self.about = None
        self.help_ico = None
        self.window = None
        self.new_file_ico = None
        self.toolBar = None
        self.new_file = None
        self.statusbar = None
        self.bar_menu = None
        self.menu_4 = None
        self.menu_3 = None
        self.menu_2 = None
        self.menu = None
        self.menubar = None
        self.centralwidget = None
        self.text = None
        self.find_textline = None
        self.printer = QPrinter()
        self.saved = True
        self.encoding_file = "UTF-8"
        self.file_path = "无标题"
        self.layout = QGridLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        self.line_wrap = True
        logging.info("Initialization completed")

    def text_changed(self):
        # logging.info(f"Text changed")
        self.window.window_title = f"*{self.file_path} - 记事本"
        self.saved = False
        if self.statusbar.isVisible():
            self.statusbar.showMessage(f"编码:{self.encoding_file.upper()}\t | 文件:{self.file_path}\t | 字数:{len(self.text.toPlainText())}")

    def toggle_status_bar(self):
        self.statusbar.setVisible(self.status_bar.isChecked())

    def resized_text(self):
        logging.info(f"Window resized:{self.width} {self.height}")
        self.text.setGeometry(QtCore.QRect(0, 0, self.width, self.height-80))

    def save_file_as_func(self):
        select_file = QFileDialog.getSaveFileName(None, "选择保存位置", f"{os.environ['USERPROFILE']}/Desktop",
                                                  "文本文件 (*.txt);; Git Ignore源文件 (.gitignore);; Yaml文件 (*.yml "
                                                  "*.yaml);; Xml文件 (*.xml);; HTML (*.html *.htm)")
        if select_file != ("", ""):
            try:
                path = select_file[0]
                logging.info(f"FILE:{path}")
                with open(path, 'w', encoding=self.encoding_file) as file:
                    file.write(self.text.toPlainText())
                logging.info("FILE SAVED SUCCESSFULLY")
                self.window.window_title = f"{self.file_path} - 记事本"
                self.file_path = path
                self.saved = True
            except UnicodeDecodeError:
                logging.error("DECODE ERROR")
                QMessageBox.critical(None, "文件保存错误", f"无法成功使用'{self.encoding_file}'编码保存文件")

    def save_file_func(self):
        if self.file_path != "无标题":
            if not os.path.exists(os.path.dirname(self.file_path)):
                QMessageBox.critical(None, "non", f"目录不存在")
                self.save_file_as_func()
                return None
            else:
                try:
                    path = self.file_path
                    logging.info(f"FILE:{path}")
                    with open(path, 'w', encoding=self.encoding_file) as file:
                        file.write(self.text.toPlainText())
                    logging.info("FILE SAVED SUCCESSFULLY")
                    self.window.window_title = f"{self.file_path} - 记事本"
                    self.file_path = path
                    self.saved = True
                except UnicodeDecodeError:
                    logging.error("DECODE ERROR")
                    QMessageBox.critical(None, "文件保存错误", f"无法成功使用'{self.encoding_file}'编码保存文件")
        else:
            self.save_file_as_func()
            return None

    def quit_app(self):
        logging.info("Quit Triggered")
        if not self.saved:
            if QMessageBox.question(None, "询问", "文件未保存\n是否保存?") == QtWidgets.QMessageBox.No:
                close_window()
            else:
                self.save_file_as_func()
        else:
            close_window()

    def search_in_internet(self):
        website = self.text.textCursor().selectedText()
        website = urllib.parse.quote(website)
        if config['Search'] == 'Bing':
            webbrowser.open(f"https://www.bing.com/search?q={website}")
        elif config['Search'] == 'Baidu':
            webbrowser.open(f"https://www.baidu.com/s?wd={website}")
        elif config['Search'] == 'Google':
            webbrowser.open(f"https://www.google.com/search?q={website}")
        elif config['Search'] == 'DuckDuckGo':
            webbrowser.open(f"https://duckduckgo.com/?t=h_&q=1145{website}")

    def new_file_func(self):
        logging.info("New File")
        if not self.saved:
            if QMessageBox.question(None, "询问", "文件未保存\n是否保存?") == QtWidgets.QMessageBox.No:
                self.text.setText("")
            else:
                self.save_file_func()
                self.text.setText("")
        else:
            self.text.setText("")
        self.file_path = "无标题"
        self.window.window_title = f"{self.file_path} - 记事本"
        self.encoding_file = "UTF-8"

    def open_file_func(self):
        logging.info("OPEN FILE")
        if not self.saved:
            logging.info("FILE NOT SAVED")
            if QMessageBox.question(None, "询问", "文件未保存\n是否保存?") == QtWidgets.QMessageBox.No:
                pass
            else:
                self.save_file_as_func()

        select_file = QFileDialog()
        select_file.setFileMode(QFileDialog.ExistingFile)
        select_file.setDirectory(f"{os.environ['USERPROFILE']}/Desktop")
        select_file.setNameFilter("可打开的文本文件 (*.txt *.htm *.html *.yml *.xml *.cfg *.gitignore)")
        if select_file.exec_():
            try:
                path = select_file.selectedFiles()[0]
                logging.info(f"FILE:{path}")
                with open(path, 'rb') as file:
                    encoding = chardet.detect(file.read())['encoding']
                    logging.info(f"ENCODING:{encoding}")
                with open(path, encoding=encoding) as file:
                    self.text.setPlainText('\n'.join(file.readlines()))
                self.encoding_file = encoding
                logging.info("FILE OPENED SUCCESSFULLY")
                self.file_path = path
                self.saved = True
                self.window.window_title = f"{self.file_path} - 记事本"
            except UnicodeDecodeError:
                logging.error("DECODE ERROR")
                QMessageBox.critical(None, "文件打开错误", f"无法成功使用'{encoding}'编码打开文件")

    def print_func(self):
        settingsDialog = QPageSetupDialog(self.printer)
        settingsDialog.exec()
        printerDialog = QPrintDialog(self.printer)
        if QDialog.Accepted == printerDialog.exec():
            self.text.print(self.printer)

    def undo_func(self):
        self.text.undo()

    def redo_func(self):
        self.text.redo()

    def select_func(self):
        self.text.selectAll()

    def cut_func(self):
        pyperclip.copy(self.text.textCursor().selectedText())
        self.text.textCursor().removeSelectedText()

    def copy_func(self):
        pyperclip.copy(self.text.textCursor().selectedText())

    def paste_func(self):
        self.text.insertPlainText(pyperclip.paste())

    def find_func(self):
        findDlg = QtWidgets.QDialog(self)
        findDlg.setWindowTitle('查找...')

        self.find_textLineEdit = QtWidgets.QLineEdit(findDlg)
        find_next_button = QtWidgets.QPushButton('查找下一个', findDlg)
        find_last_button = QtWidgets.QPushButton('查找上一个', findDlg)

        v_layout = QtWidgets.QVBoxLayout(self)
        v_layout.addWidget(find_last_button)
        v_layout.addWidget(find_next_button)

        h_layout = QtWidgets.QHBoxLayout(findDlg)
        h_layout.addWidget(self.find_textLineEdit)
        h_layout.addLayout(v_layout)

        find_last_button.clicked.connect(self.show_findLast)
        find_next_button.clicked.connect(self.show_findNext)

        findDlg.show()

    def show_findLast(self):
        find_text = self.find_textLineEdit.text()
        print(find_text)
        print(self.text.find(find_text, QTextDocument.FindBackward))

    def show_findNext(self):
        find_text = self.find_textLineEdit.text()
        print(find_text)
        print(self.text.find(find_text, QTextDocument.FindBackward))
        if self.text.find(find_text, QTextDocument.FindBackward):
            QMessageBox.warning(None, '查找', '找不到 {}'.format(find_text))

    def switch_line_func(self):
        logging.info("Switch Line Wrap")
        if self.line_wrap:
            logging.info("Line Wrap True   Set to False")
            self.text.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        else:
            logging.info("Line Wrap False   Set to True")
            self.text.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)

        self.line_wrap = not self.line_wrap

    def font_func(self):
        font, status = QtWidgets.QFontDialog.getFont()
        if status:
            self.text.setFont(font)
            self.font_combo.setCurrentFont(font)


    def set_text_font(self):
        self.text.setFont(QtGui.QFont(self.font_combo.currentText()))

    def color_func(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.text.setTextColor(color)

    def replace_func(self):
        find, ok = QtWidgets.QInputDialog.getText( self,'Replace', '查找')
        if not ok:
            return None
        replace, ok = QtWidgets.QInputDialog.getText(self, 'Replace', '替换为')
        if ok:
            texts = self.text.toPlainText()
            self.text.setPlainText(texts.replace(find, replace))


    def about_func(self):
        dialog = AboutDialog(self.window)
        dialog.exec_()

    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(750, 480)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.text = QtWidgets.QTextEdit(self.centralwidget)
        self.text.setGeometry(QtCore.QRect(0, 30, 751, 400))
        self.text.setObjectName("text")
        self.text.setAcceptRichText(False)
        self.text.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)

        self.layout.addWidget(self.text)
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")
        self.bar_menu = QtWidgets.QMenu(self.menubar)
        self.bar_menu.setObjectName("menub")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(window)
        self.toolBar.setObjectName("toolBar")
        window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.new_file = QtWidgets.QAction(window)
        self.new_file.setObjectName("new_file")
        self.new_file_ico = QtGui.QIcon()
        self.new_file_ico.addPixmap(QtGui.QPixmap("resources/new_file_fr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.new_file.setIcon(self.new_file_ico)
        self.new_file.setShortcut("Ctrl+N")
        self.open_file = QtWidgets.QAction(window)
        self.open_file.setObjectName("open_file")
        self.open_file_ico = QtGui.QIcon()
        self.open_file_ico.addPixmap(QtGui.QPixmap("resources/blue-folder-open-document.png"), QtGui.QIcon.Normal,
                                     QtGui.QIcon.Off)
        self.open_file.setIcon(self.open_file_ico)
        self.open_file.setShortcut("Ctrl+O")
        self.save_file = QtWidgets.QAction(window)
        self.save_file.setObjectName("save_file")
        self.save_file_ico = QtGui.QIcon()
        self.save_file_ico.addPixmap(QtGui.QPixmap("resources/disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_file.setIcon(self.save_file_ico)
        self.save_file.setShortcut("Ctrl+S")
        self.save_as = QtWidgets.QAction(window)
        self.save_as.setObjectName("save_as")
        self.save_as_ico = QtGui.QIcon()
        self.save_as_ico.addPixmap(QtGui.QPixmap("resources/disk--pencil.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_as.setIcon(self.save_as_ico)
        self.save_as.setShortcut("Ctrl+Shift+S")
        self.print = QtWidgets.QAction(window)
        self.print.setObjectName("print")
        self.print_ico = QtGui.QIcon()
        self.print_ico.addPixmap(QtGui.QPixmap("resources/printer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.print.setIcon(self.print_ico)
        self.quit = QtWidgets.QAction(window)
        self.quit.setObjectName("quit")
        self.quit_ico = QtGui.QIcon()
        self.quit_ico.addPixmap(QtGui.QPixmap("resources/x_fr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quit.setIcon(self.quit_ico)
        self.undo = QtWidgets.QAction(window)
        self.undo.setObjectName("undo")
        self.undo_ico = QtGui.QIcon()
        self.undo_ico.addPixmap(QtGui.QPixmap("resources/arrow-curve-180-left.png"), QtGui.QIcon.Normal,
                                QtGui.QIcon.Off)
        self.undo.setIcon(self.undo_ico)
        self.undo.setShortcut("Ctrl+Z")
        self.redo = QtWidgets.QAction(window)
        self.redo.setObjectName("redo")
        self.redo_ico = QtGui.QIcon()
        self.redo_ico.addPixmap(QtGui.QPixmap("resources/arrow-curve.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.redo.setIcon(self.redo_ico)
        self.redo.setShortcut("Ctrl+Shift+Z")
        self.select = QtWidgets.QAction(window)
        self.select.setObjectName("select")
        self.select_ico = QtGui.QIcon()
        self.select_ico.addPixmap(QtGui.QPixmap("resources/selection-input.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.select.setIcon(self.select_ico)
        self.cut = QtWidgets.QAction(window)
        self.cut.setObjectName("cut")
        self.cut_ico = QtGui.QIcon()
        self.cut_ico.addPixmap(QtGui.QPixmap("resources/scissors.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cut.setIcon(self.cut_ico)
        self.paste = QtWidgets.QAction(window)
        self.paste.setObjectName("paste")
        self.paste_ico = QtGui.QIcon()
        self.paste_ico.addPixmap(QtGui.QPixmap("resources/clipboard-paste-document-text.png"), QtGui.QIcon.Normal,
                                 QtGui.QIcon.Off)
        self.paste.setIcon(self.paste_ico)
        self.search = QtWidgets.QAction(window)
        self.search.setObjectName("search")
        self.search_ico = QtGui.QIcon()
        self.search_ico.addPixmap(QtGui.QPixmap("resources/search_fr.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search.setIcon(self.search_ico)
        self.find = QtWidgets.QAction(window)
        self.find.setObjectName("find")
        self.replace = QtWidgets.QAction(window)
        self.replace.setObjectName("replace")
        self.insert_time = QtWidgets.QAction(window)
        self.insert_time.setObjectName("insert_time")
        self.auto_change_line = QtWidgets.QAction(window)
        self.auto_change_line.setCheckable(True)
        self.auto_change_line.setChecked(True)
        self.auto_change_line.setObjectName("auto_change_line")
        self.font = QtWidgets.QAction(window)
        self.font.setObjectName("font")
        self.font_ico = QtGui.QIcon()
        self.font_ico.addPixmap(QtGui.QPixmap("resources/edit-italic.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.font.setIcon(self.font_ico)
        self.color = QtWidgets.QAction(window)
        self.color.setObjectName("color")
        self.color_ico = QtGui.QIcon()
        self.color_ico.addPixmap(QtGui.QPixmap("resources/edit-color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.color.setIcon(self.color_ico)
        self.status_bar = QtWidgets.QAction(window)
        self.status_bar.setCheckable(True)
        self.status_bar.setChecked(True)
        self.status_bar.setObjectName("status_bar")
        self.status_bar.triggered.connect(self.toggle_status_bar)
        self.copy = QtWidgets.QAction(window)
        self.copy.setObjectName("copy")
        self.copy_ico = QtGui.QIcon()
        self.copy_ico.addPixmap(QtGui.QPixmap("resources/document-copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copy.setIcon(self.copy_ico)
        self.help = QtWidgets.QAction(window)
        self.help.setObjectName("help")
        self.help_ico = QtGui.QIcon()
        self.help_ico.addPixmap(QtGui.QPixmap("resources/question.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help.setIcon(self.help_ico)
        self.about = QtWidgets.QAction(window)
        self.about.setObjectName("about")
        self.about.setIcon(QtGui.QIcon("resources/question.png"))
        self.menu.addAction(self.new_file)
        self.menu.addAction(self.open_file)
        self.menu.addAction(self.save_file)
        self.menu.addAction(self.save_as)
        self.menu.addSeparator()
        self.menu.addAction(self.print)
        self.menu.addSeparator()
        self.menu.addAction(self.quit)
        self.menu_2.addAction(self.undo)
        self.menu_2.addAction(self.redo)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.select)
        self.menu_2.addAction(self.cut)
        self.menu_2.addAction(self.copy)
        self.menu_2.addAction(self.paste)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.search)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.find)
        self.menu_2.addAction(self.replace)
        self.menu_2.addSeparator()
        self.menu_2.addAction(self.insert_time)
        self.menu_3.addAction(self.auto_change_line)
        self.menu_3.addAction(self.font)
        self.menu_3.addAction(self.color)
        self.menu_4.addAction(self.status_bar)
        self.bar_menu.addAction(self.help)
        self.bar_menu.addAction(self.about)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.bar_menu.menuAction())

        self.text.textChanged.connect(self.text_changed)

        self.quit.triggered.connect(self.quit_app)
        self.open_file.triggered.connect(self.open_file_func)
        self.save_file.triggered.connect(self.save_file_func)
        self.save_as.triggered.connect(self.save_file_as_func)
        self.new_file.triggered.connect(self.new_file_func)
        self.resized.connect(self.resized_text)
        self.print.triggered.connect(self.print_func)
        self.undo.triggered.connect(self.undo_func)
        self.redo.triggered.connect(self.redo_func)
        self.copy.triggered.connect(self.copy_func)
        self.cut.triggered.connect(self.cut_func)
        self.replace.triggered.connect(self.replace_func)
        self.paste.triggered.connect(self.paste_func)
        self.select.triggered.connect(self.select_func)
        self.search.triggered.connect(self.search_in_internet)
        self.find.triggered.connect(self.find_func)
        self.auto_change_line.triggered.connect(self.switch_line_func)
        self.font.triggered.connect(self.font_func)
        self.color.triggered.connect(self.color_func)
        self.about.triggered.connect(self.about_func)
        self.retranslateUi(window)

        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setIconSize(QtCore.QSize(16, 16))
        self.toolBar.addAction(QtGui.QIcon("resources/new_file_fr.png"), "新建")
        self.toolBar.addAction(QtGui.QIcon("resources/blue-folder-open-document.png"), "打开")
        self.toolBar.addAction(QtGui.QIcon("resources/disk.png"), "保存")
        self.toolBar.addAction(QtGui.QIcon("resources/x_fr.png"), "退出")
        self.toolBar.addAction(QtGui.QIcon("resources/printer.png"), "打印")
        self.toolBar.addAction(QtGui.QIcon("resources/arrow-curve-180-left.png"), "撤销")
        self.toolBar.addAction(QtGui.QIcon("resources/arrow-curve.png"), "重做")
        self.toolBar.addAction(self.about)
        self.font_combo = QtWidgets.QFontComboBox()
        self.font_combo.setFontFilters(QtWidgets.QFontComboBox.AllFonts)
        self.font_combo.currentIndexChanged.connect(self.set_text_font)
        self.toolBar.addWidget(self.font_combo)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        self.window = window
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "无标题 - 记事本"))
        self.menu.setTitle(_translate("window", "文件"))
        self.menu_2.setTitle(_translate("window", "编辑"))
        self.menu_3.setTitle(_translate("window", "格式"))
        self.menu_4.setTitle(_translate("window", "查看"))
        self.bar_menu.setTitle(_translate("window", "帮助"))
        self.toolBar.setWindowTitle(_translate("window", "启用工具栏"))
        self.new_file.setText(_translate("window", "新建"))
        self.open_file.setText(_translate("window", "打开"))
        self.save_file.setText(_translate("window", "保存"))
        self.save_as.setText(_translate("window", "另存为"))
        self.print.setText(_translate("window", "打印"))
        self.quit.setText(_translate("window", "退出"))
        self.undo.setText(_translate("window", "撤销"))
        self.redo.setText(_translate("window", "重做"))
        self.select.setText(_translate("window", "全选"))
        self.cut.setText(_translate("window", "剪切"))
        self.paste.setText(_translate("window", "粘贴"))
        self.search.setText(_translate("window", "在Internet中搜索"))
        self.find.setText(_translate("window", "查找"))
        self.replace.setText(_translate("window", "替换"))
        self.insert_time.setText(_translate("window", "输入时间和日期"))
        self.auto_change_line.setText(_translate("window", "自动换行"))
        self.color.setText(_translate("window", "颜色"))
        self.font.setText(_translate("window", "字体"))
        self.status_bar.setText(_translate("window", "状态栏"))
        self.copy.setText(_translate("window", "复制"))
        self.help.setText(_translate("window", "帮助"))
        self.about.setText(_translate("window", "关于"))
