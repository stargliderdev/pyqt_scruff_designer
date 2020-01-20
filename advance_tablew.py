#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QCheckBox
import qlib as qc

class TestClass(QDialog):
    def __init__(self, parent=None):
        super(TestClass, self).__init__(parent)
        masterLayout = QVBoxLayout(self)
        lay0 = QHBoxLayout()
        lay1 = QHBoxLayout()
        lay2 = QHBoxLayout()
        lay3 = QHBoxLayout()
        self.headersEdt = QLineEdit()
        masterLayout.addLayout(qc.addHLayout(['Headers',self.headersEdt]))
        self.rowsEdt = QLineEdit()
        self.rowsEdt.setMaximumWidth(30)
        self.rowsEdt.setMinimumWidth(30)
        self.colsEdt = QLineEdit()
        self.colsEdt.setMaximumWidth(30)
        self.colsEdt.setMinimumWidth(30)
        self.selectBeaCbx = QComboBox()
        masterLayout.addLayout(qc.addHLayout(['Rows/Colunms',self.rowsEdt,self.colsEdt,True]))
        masterLayout.addLayout(qc.addHLayout(['Seelct Beahvori', self.selectBeaCbx]))
        self.setSelectMode = QComboBox()
        masterLayout.addLayout(qc.addHLayout(['Select Mode', self.setSelectMode]))
        self.editTriggers = QComboBox()
        masterLayout.addLayout(qc.addHLayout(['Edit Triggers', self.editTriggers]))
        label2 = QLabel('Vertical Header Size')
        lay2.addWidget(label2)
        self.vheaderSize = QLineEdit()
        self.vheaderSize.setMaximumWidth(30)
        self.vheaderSize.setMinimumWidth(30)
        lay2.addWidget(self.vheaderSize)
        self.alterntingRow = QCheckBox('Alternating Row')
        masterLayout.addWidget(self.alterntingRow)
        label3 = QLabel('Set Style Sheet')
        lay3.addWidget(label3)
        self.styleSheetEdt = QLineEdit()
        lay3.addWidget(self.styleSheetEdt)
        self.vHeaderVisibleChk = QCheckBox('Vertical Header Visible')
        masterLayout.addWidget(self.vHeaderVisibleChk)

        self.resizeToContentsChk = QCheckBox('Resize To Contents')
        masterLayout.addWidget(self.resizeToContentsChk)
        self.onDblClickBtn = QLineEdit()
        masterLayout.addWidget(self.onDblClickBtn)
        self.onSingleClickEdt = QLineEdit()
        masterLayout.addWidget(self.onSingleClickEdt)
        masterLayout.addLayout(lay0)
        masterLayout.addLayout(lay1)
        masterLayout.addLayout(lay2)
        masterLayout.addLayout(lay3)
        okBtn = QPushButton('O.K.')
        cancelBtn = QPushButton('Cancel')
        masterLayout.addLayout(qc.addHLayout([okBtn,cancelBtn]))

def main():
    app = QApplication(sys.argv)
    form = TestClass()
    form.show()
    app.exec_()
if __name__ == '__main__':
    main()

