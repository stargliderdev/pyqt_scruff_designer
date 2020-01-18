#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QSpinBox, QApplication, QToolButton, QMessageBox, \
    QLineEdit, QComboBox

import qlib as qc
import parameters as gl

class Properties(QDialog):
    def __init__(self, parent=None):
        super(Properties, self).__init__(parent)
        self.resize(400, 600)
        self.setWindowTitle('Propertis')
        self.ctrl_list = ['QComboBox', 'QLineEdit', 'QSpinBox', 'QPlainTextEdit', 'QDateEdit', 'QDoubleSpinBox',
                          'QCheckBox',
                          'QTableWidget', 'QPushButton', 'QToolButton', 'QListWidget', 'QVBoxLayout', 'QHBoxLayout']
        self.ret = {'responce': False}
        masterLayout = QVBoxLayout(self)
        self.controlCbx = QComboBox()
        self.controlCbx.addItems(self.ctrl_list)
        self.labelEdt = QLineEdit()
        self.controlNameEdt = QLineEdit()
        self.layoutCbx = QComboBox()
        self.layoutCbx.addItems(gl.layouts_list)
        self.maxWight = QLineEdit()
        self.maxHeight = QLineEdit()
        self.minWight = QLineEdit()
        self.minHeight = QLineEdit()
        
        masterLayout.addLayout(qc.addHLayout(['Widget', self.controlCbx]))
        masterLayout.addLayout(qc.addHLayout(['Label', self.labelEdt]))
        masterLayout.addLayout(qc.addHLayout(['Name', self.controlNameEdt]))
        masterLayout.addLayout(qc.addHLayout(['Layout', self.layoutCbx]))
        masterLayout.addLayout(qc.addHLayout(['Width', 'max', self.maxWight, 'min', self.minWight]))
        masterLayout.addLayout(qc.addHLayout(['Height','max', self.maxHeight, 'min', self.minHeight]))
        masterLayout.addStretch()
        
        
        okBtn = QPushButton('Valida')
        okBtn.clicked.connect(self.ok_click)
        
        cancelBtn = QPushButton('Sair')
        cancelBtn.clicked.connect(self.cancel_btn_click)
        masterLayout.addLayout(qc.addHLayout([okBtn, cancelBtn]))
      
    def cancel_btn_click(self):
        self.close()
    
    def ok_click(self):
        if self.validate():
            ctr_data = {'control': self.controlCbx.currentText(), 'label': self.labelEdt.text(),
                        'control_name': self.controlNameEdt.text(),
                        'max_width': self.maxWight.text(),
                        'min_width': self.minWight.text(),
                        'max_height': self.maxHeight.text(),
                        'min_height': self.minHeight.text(),
                        'layout': self.layoutCbx.currentText()
                        }
            self.ret = {'responce': True, 'ctr_data': ctr_data}
            self.close()

    def validate(self):
        flag = True
        if self.controlCbx.currentText() in ['QVBoxLayout', 'QHBoxLayout']:
            if self.controlNameEdt.text() == '':
                QMessageBox.critical(None, "Asneira", "Layouts have to had a name")
                flag = False
        return flag

def main():
    app = QApplication(sys.argv)
    form = Properties()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

