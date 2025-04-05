from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('关于 ILoveScratch记事本')
        self.setWindowIcon(QIcon('resources/notepad.png'))
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        
        # 标题和版本
        title = QLabel('ILoveScratch记事本 0.7.0 Beta')
        title.setStyleSheet('font-size: 18px; font-weight: bold;')
        layout.addWidget(title, alignment=Qt.AlignCenter)
        
        # 开发信息
        dev_info = QLabel('开发者: ILoveScratch Dev\n版本 0.7.0 Beta')
        layout.addWidget(dev_info, alignment=Qt.AlignCenter)
        
        # 依赖信息
        deps_text = QTextBrowser()
        deps_text.setPlainText(
            '依赖库：\n'
            '- PyQt5 (GPLv3)\n'
            '- chardet (LGPL)\n'
            '- pyperclip (BSD)'
        )
        layout.addWidget(deps_text)
        
        # 开源协议
        license_text = QTextBrowser()
        license_text.setPlainText(
            '本软件遵循GNU GPLv3协议发行\n\n'
            'Copyright © 2025 ILoveScratch2\n'
            'PyQt5版权归属Riverbank Computing Limited'
        )
        layout.addWidget(license_text)
        
        # 确认按钮
        btn_ok = QPushButton('确定')
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)