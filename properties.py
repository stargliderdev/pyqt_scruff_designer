#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QSpinBox, QApplication, QToolButton, QMessageBox, \
    QLineEdit, QComboBox, QCheckBox

import qlib as qc
import parameters as gl

class Properties(QDialog):
    def __init__(self, data_dict,parent=None):
        super(Properties, self).__init__(parent)
        self.resize(400, 600)
        self.setWindowTitle('Properties')
        self.ctrl_list = ['QLineEdit','QLabel','QPushButton','QTableWidget','QToolButton',  'QComboBox','QDateEdit', 'QCheckBox','QSpinBox', 'QPlainTextEdit', 'QDoubleSpinBox',
                          'QListWidget','QCalendarWidget',
                          'QTimeEdit','QDateTimeEdit',
                          'QCommandLinkButton','QTreeWidget', 'QVBoxLayout', 'QHBoxLayout','addStretch']
        self.ret = {'responce': False}
        self.data_dict = data_dict
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
        if not self.data_dict['new']:
            self.refresh_form()
        else:
            self.set_values()
        
    def refresh_form(self):
        self.controlCbx.setCurrentText(self.data_dict['widget'])
        self.labelEdt.setText(self.data_dict['label'])
        self.controlNameEdt.setText(self.data_dict['widget_name'])
        self.layoutCbx.setCurrentText(self.data_dict['layout'])
        if self.data_dict['max_width'] != '-1':
            self.maxWight.setText(self.data_dict['max_width'])
        if self.data_dict['min_width'] != '-1':
            self.minWight.setText(self.data_dict['min_width'])
        if self.data_dict['max_height'] != '-1':
            self.maxHeight.setText(self.data_dict['max_height'])
        if self.data_dict['min_height'] != '-1':
            self.minHeight.setText(self.data_dict['min_height'])
        
    def set_values(self):
        if gl.ADD_SELF == 2:
            self.controlNameEdt.setText('self.')
    
    def cancel_btn_click(self):
        self.close()
    
    def ok_click(self):
        gl.ADD_SELF = self.addSelf.checkState()
        if self.validate():
            ctr_data = {'widget': self.controlCbx.currentText(), 'label': self.labelEdt.text(),
                        'widget_name': self.controlNameEdt.text(),
                        'layout': self.layoutCbx.currentText(),
                        'new': False }
            if self.maxWight.text() != '':
                ctr_data['max_width'] = self.maxWight.text()
            else:
                ctr_data['max_width'] = '-1'
            if self.minWight.text() != '':
                ctr_data['min_width'] = self.minWight.text()
            else:
                ctr_data['min_width'] = '-1'
            if self.maxHeight.text() != '':
                ctr_data['max_height'] = self.maxHeight.text()
            else:
                ctr_data['max_height'] = '-1'
            if self.minHeight.text() != '':
                ctr_data['min_height'] = self.minHeight.text()
            else:
                ctr_data['min_height'] = '-1'
            self.ret = {'responce': True, 'ctr_data': ctr_data}
            self.close()
    
    def validate(self):
        flag = True
        if self.controlNameEdt.text() == '' or self.controlNameEdt.text() == 'self.' and self.controlCbx.currentText() != 'addStretch':
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
        if    self.controlCbx.currentText() == 'addStretch': self.controlNameEdt.setText('')
        return flag

def main():
    app = QApplication(sys.argv)
    form = Properties()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()

