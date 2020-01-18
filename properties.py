#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QSpinBox, QApplication, QToolButton, QMessageBox, \
    QLineEdit, QComboBox, QCheckBox

import qlib as qc
import parameters as gl

class Properties(QDialog):
    def __init__(self, parent=None):
        super(Properties, self).__init__(parent)
        self.resize(400, 600)
        self.setWindowTitle('Properties')
        self.ctrl_list = ['QLineEdit','QLabel','QPushButton','QTableWidget','QToolButton',  'QComboBox','QDateEdit', 'QCheckBox','QSpinBox', 'QPlainTextEdit', 'QDoubleSpinBox',
                           'QListWidget', 'QVBoxLayout', 'QHBoxLayout','addStretch']
        self.ret = {'responce': False}
        masterLayout = QVBoxLayout(self)
        self.controlCbx = QComboBox()
        self.controlCbx.addItems(self.ctrl_list)
        self.labelEdt = QLineEdit()
        self.controlNameEdt = QLineEdit()
        self.addSelf = QCheckBox('Add self.')
        self.addSelf.setCheckState(gl.ADD_SELF)
        self.layoutCbx = QComboBox()
        self.layoutCbx.addItems(gl.layouts_list)
        self.maxWight = QLineEdit()
        self.maxHeight = QLineEdit()
        self.minWight = QLineEdit()
        self.minHeight = QLineEdit()
        
        masterLayout.addLayout(qc.addHLayout(['Widget', self.controlCbx]))
        masterLayout.addLayout(qc.addHLayout(['Label', self.labelEdt]))
        masterLayout.addLayout(qc.addHLayout(['Name', self.controlNameEdt,self.addSelf]))
        masterLayout.addLayout(qc.addHLayout(['Layout', self.layoutCbx]))
        masterLayout.addLayout(qc.addHLayout(['Width', 'max', self.maxWight, 'min', self.minWight]))
        masterLayout.addLayout(qc.addHLayout(['Height','max', self.maxHeight, 'min', self.minHeight]))
        masterLayout.addStretch()
        
        
        okBtn = QPushButton('Valida')
        okBtn.clicked.connect(self.ok_click)
        
        cancelBtn = QPushButton('Sair')
        cancelBtn.clicked.connect(self.cancel_btn_click)
        masterLayout.addLayout(qc.addHLayout([okBtn, cancelBtn]))
        self.set_values()
    
    
    def set_values(self):
        if gl.ADD_SELF == 2:
            self.controlNameEdt.setText('self.')
      
    def cancel_btn_click(self):
        self.close()
    
    def ok_click(self):
        gl.ADD_SELF = self.addSelf.checkState()
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
        if self.controlNameEdt.text() == '' or self.controlNameEdt.text() == 'self.' :
            QMessageBox.critical(None, "Error", "Missing Widget name")
            flag = False
        else:
            if self.labelEdt.text() == '' and self.controlCbx.currentText() in ['QLabel','QPushButton','QCheckBox']:
                QMessageBox.critical(None, "Error", "This widget needs a label")
                flag = False
            if self.controlCbx.currentText() in ['QVBoxLayout', 'QHBoxLayout']:
                if self.controlNameEdt.text() == '':
                    QMessageBox.critical(None, "Error", "Layouts have to had a name")
                    flag = False
            
        return flag

def main():
    app = QApplication(sys.argv)
    form = Properties()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

