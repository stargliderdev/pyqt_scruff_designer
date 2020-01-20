#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtGui import QBrush, QColor, QPalette, QFont
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QPushButton, QLabel, QPlainTextEdit, QDesktopWidget
from PyQt5.QtCore import Qt

class ShowCode(QDialog):
    def __init__(self, code, parent=None):
        super(ShowCode, self).__init__(parent)
        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Show Code')
        masterLayout = QVBoxLayout(self)
        label = QLabel('Show Code')
        masterLayout.addWidget(label)
        palette = QPalette()
        brush = QBrush(QColor(0, 255, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        brush = QBrush(QColor(0, 255, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        brush = QBrush(QColor(0, 0, 0))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        brush = QBrush(QColor(165, 164, 164))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
        brush = QBrush(QColor(244, 244, 244))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        font = QFont('courier new', 11)
        font.setWeight(80)
        font.setBold(False)
        self.showCodeTEdt = QPlainTextEdit()
        self.showCodeTEdt.setPalette(palette)
        self.showCodeTEdt.setFont(font)
        masterLayout.addWidget(self.showCodeTEdt)
        okBtn = QPushButton('O.K.')
        okBtn.clicked.connect(self.ok_click)
        
        masterLayout.addWidget(okBtn)
        self.showCodeTEdt.setPlainText(code)
    
    def ok_click(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
def main():
    app = QApplication(sys.argv)
    form = ShowCode()
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()

