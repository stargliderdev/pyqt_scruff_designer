#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QDesktopWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, \
    QTableWidget, QMenu, QPushButton, QDialog, QTableWidgetItem, QPlainTextEdit,QSpinBox,\
    QWidget, QTabWidget, QApplication, QMessageBox, QStyleFactory, QCheckBox, QAction,QHBoxLayout
from PyQt5.QtCore import Qt
import json

import parameters as gl
import properties

import parameters as pa

TAB = '    '


class MainWindow(QDialog):
    def __init__(self,  parent = None):
        super(MainWindow,  self).__init__(parent)
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle('PyQt Scruff Designer')
        self.ctrl_list = ['QComboBox','QLineEdit','QSpinBox','QPlainTextEdit','QDateEdit','QDoubleSpinBox','QCheckBox',
                          'QTableWidget','QPushButton','QToolButton','QListWidget']

        mainLayout = QVBoxLayout(self)
        self.tabuladorTabWidget = QTabWidget()

        self.make_tab_designer()
        self.tabuladorTabWidget.addTab(self.tab1, 'Designer')

        # self.make_tab_sql()
        # self.tabuladorTabWidget.addTab(self.tab2, 'SQL')

        # self.make_tab_tab()
        # self.tabuladorTabWidget.addTab(self.tab3, 'Make Tab')

        mainLayout.addWidget(self.tabuladorTabWidget)

    def make_tab_designer(self):

        self.tab1 = QWidget()
        mainTabLayout = QVBoxLayout(self.tab1)
        tabLayout = QVBoxLayout()
        self.addBtn = QPushButton('+')
        self.addBtn.clicked.connect(self.add_click)
        
        self.upBtn = QPushButton('UP')
        self.upBtn.clicked.connect(self.up_click)
        

        self.downBtn = QPushButton('DWN')
        self.downBtn.clicked.connect(self.down_click)

        tabLayout.addLayout(self.addHDumLayout([self.addBtn,self.upBtn,self.downBtn,True]))

        self.grdMain =QTableWidget(self)
        lineHeaders =['Widget','Name','Label','Layout','Sort','Width (min,max)','Height','data']
        self.grdMain.setColumnCount(len(lineHeaders))
        self.grdMain.setSelectionBehavior(QTableWidget.SelectRows)
        self.grdMain.setSelectionMode(QTableWidget.SingleSelection)
        self.grdMain.setEditTriggers(QTableWidget.NoEditTriggers)
        self.grdMain.verticalHeader().setDefaultSectionSize(20)
        self.grdMain.setAlternatingRowColors (True)
        self.grdMain.verticalHeader().setVisible(False)
        self.grdMain.setHorizontalHeaderLabels(lineHeaders)
        self.grdMain.cellDoubleClicked.connect(self.cell_click)
        
        designLayout = QHBoxLayout()
        designLayout.addWidget(self.grdMain)
        tabLayout.addLayout(designLayout)

        okBtn = QPushButton('O.K.')
        okBtn.clicked.connect(self.build_click)
        self.cancelBtn = QPushButton('Cancela')
        self.cancelBtn.clicked.connect(self.cancel_btn_click)
        
        self.saveBtn = QPushButton('Save')
        self.saveBtn.clicked.connect(self.save_btn_click)
        
        self.loadBtn = QPushButton('Load')
        self.loadBtn.clicked.connect(self.load_btn_click)
        
        tabLayout.addLayout(self.addHDumLayout([okBtn,self.saveBtn,self.loadBtn,self.cancelBtn]))
        mainTabLayout.addLayout(tabLayout)

    def make_tab_sql(self):
        self.tab2 = QWidget()
        mainTabLayout = QVBoxLayout(self.tab2)
        tabLayout = QVBoxLayout()
        self.run_sqlBtn = QPushButton('Run')

        self.table_LineEdit = QLineEdit()
        self.table_LineEdit.setText('table')

        self.index_field_LineEdit = QLineEdit()
        self.index_field_LineEdit.setText('index_field')
        tabLayout.addLayout(self.addHDumLayout([self.run_sqlBtn,self.table_LineEdit, self.index_field_LineEdit,True]))

        self.sql_PlainText = QPlainTextEdit()
        self.sql_PlainText.appendPlainText('hardware')
        tabLayout.addWidget(self.sql_PlainText)

        mainTabLayout.addLayout(tabLayout)

    def make_tab_tab(self):
        self.tab3 = QWidget()
        mainTabLayout = QVBoxLayout(self.tab3)
        tabLayout = QVBoxLayout()

        self.gen_nameLineEdit = QLineEdit()
        self.gen_nameLineEdit.setMaxLength(15)
        self.tab_desc_LE = QLineEdit()
        tabLayout.addLayout(self.addHDumLayout(['generator', self.gen_nameLineEdit, 'Descr', self.tab_desc_LE]))

        self.tab_numberSpin = QSpinBox()
        self.tab_numberSpin.setMaximumWidth(60)
        self.tab_numberSpin.setMinimumWidth(60)
        tabLayout.addLayout(self.addHDumLayout(['Tab #', self.tab_numberSpin, True]))

        self.codePlainText = QPlainTextEdit()
        tabLayout.addLayout(self.addHDumLayout(['Code', self.codePlainText]))

        self.make_Button = QPushButton('MAKE')

        tabLayout.addLayout(self.addHDumLayout([ self.make_Button]))

        mainTabLayout.addLayout(tabLayout)

    def make_tab_click(self):
        TAB = ' ' *8
        l_stack = 0
        l_stack_str = ''
        self.tab_stack = 0
        self.tab_string = ''
        self.tab_page_stack = 0
        self.tab_page_string = ''
        toto = 'mainLayout = QVBoxLayout(self)\n'
        toto += '(...)\n'
        toto += 'self.tabuladorTabWidget = QTabWidget()\n'
        toto += TAB + 'self.' + str(self.gen_nameLineEdit.text()) + '()\n'
        toto += TAB + 'self.tabuladorTabWidget.addTab(self.tab' + str(self.tab_numberSpin.value()) + ', \'' + self.tab_desc_LE.text() + '\')\n'
        toto += TAB + 'mainLayout.addWidget(self.tabuladorTabWidget)\n(...)\n'
        toto += 'def ' + str(self.gen_nameLineEdit.text()) + '(self):\n'
        toto += TAB + 'self.tab' + str(self.tab_numberSpin.value()) + ' = QWidget()\n'
        toto += TAB + 'mainTabLayout = QVBoxLayout(self.tab' + str(self.tab_numberSpin.value()) + ')\n'
        toto += TAB + 'tabLayout = QVBoxLayout()\n'

        for linha in range(0, self.grdMain.rowCount()):
            if self.grdMain.cellWidget(linha, 1).isChecked() :
                data = self.get_row(linha)
                if int(data['layout']) == 0 and l_stack_str == '': # normal
                    toto += TAB + data['ctrl_name'] + ' = ' + data['control'] + self.set_name(data)
                    toto += self.set_width(data)
                    toto += self.set_size(data)
                    toto += TAB + 'tabLayout.addLayout(self.addHDumLayout([' + self.set_label(data) + data['ctrl_name']
                    if data['stretch']:
                        toto += ', True'
                    toto += ']))\n'
                    toto += '\n'

                elif int(data['layout']) > 0: # detectou layout
                    if l_stack == int(data['layout']): # é igual ao do anterior, adiciona
                        toto += TAB + data['ctrl_name'] + ' = ' + data['control'] + self.set_name(data)
                        toto += self.set_width(data)
                        toto += self.set_size(data)
                        l_stack_str += ',' + self.set_label(data) + data['ctrl_name']

                    elif l_stack != int(data['layout']): # 'e outro
                        # fecha o anterior
                        if l_stack_str != '':
                            toto += TAB + 'tabLayout.addLayout(self.addHDumLayout([\'' + l_stack_str + ']))\n'
                            l_stack_str = ''
                            toto += '\n'
                        # cria o novo control
                        toto += TAB + data['ctrl_name'] + ' = ' + data['control'] + self.set_name(data)
                        toto += self.set_width(data)
                        toto += self.set_size(data)
                        # adiciona ao stack para posterior utilização
                        l_stack_str += self.set_label(data) + data['ctrl_name']

                    l_stack = int(data['layout'])
                elif int(data['layout']) == 0 and l_stack_str != '': # mudou para o laytou 0
                    # fecha o anterior
                    toto += TAB + 'tabLayout.addLayout(self.addHDumLayout([' + l_stack_str + ']))\n'
                    toto += '\n'
                    l_stack_str = ''
                    l_stack = 0
                    # adiciona o ctrl normal.
                    toto += TAB + data['ctrl_name'] + ' = ' + data['control'] + self.set_name(data)
                    toto += self.set_width(data)
                    toto += self.set_size(data)
                    toto += TAB + 'tabLayout.addLayout(self.addHDumLayout(['  + self.set_label(data) + data['ctrl_name']
                    if data['stretch']:
                        toto += ', True'
                    toto += ']))\n'
                    toto += '\n'

        if l_stack_str != '': # mudou para o laytou 0
            # fecha o anterior
            toto += TAB + 'tabLayout.addLayout(self.addHDumLayout([' + l_stack_str + ']))\n'
            toto += '\n'
            toto += TAB + 'mainTabLayout.addLayout(tabLayout)'

        self.codePlainText.setPlainText(toto)
    
    def cell_click(self, row,col):
        if col == 0:
            data = json.loads(self.grdMain.item(row, 7).text())
            data['new']= False
            self.update_layouts()
            form = properties.Properties(data)
            form.exec_()
            self.refresh_table_line(form.ret['ctr_data'], row)
            
    def add_click(self):
        form = properties.Properties({'new':True})
        form.exec_()
        ret = form.ret
        row = self.grdMain.rowCount()
        if ret['responce']:
            if row == 0:
                self.grdMain.insertRow(0)
                row = 0
            else:
                self.grdMain.insertRow(row)
            self.refresh_table_line(ret['ctr_data'], row)
            
    def refresh_table_line(self, data, row):
        item = QTableWidgetItem()
        item.setText(data['control'])
        self.grdMain.setItem(row, 0, item)
        item = QTableWidgetItem()
        item.setText(data['control_name'])
        self.grdMain.setItem(row, 1, item)
        item = QTableWidgetItem()
        item.setText(data['label'])
        self.grdMain.setItem(row, 2, item)

        item = QTableWidgetItem()
        item.setText(data['layout'])
        self.grdMain.setItem(row, 3, item)

        # store data at colum 7 hiden
        item = QTableWidgetItem()
        item.setText(json.dumps(data))
        self.grdMain.setItem(row, 7, item)
        self.update_layouts()
            
    def update_layouts(self):
        gl.layouts_list = ['None']
        for row in range(0, self.grdMain.rowCount()):
            try:
                h = self.grdMain.item(row, 0).text()
                if h in ('QVBoxLayout', 'QHBoxLayout'):
                    gl.layouts_list.append(self.grdMain.item(row, 1).text())
            except AttributeError:
                pass
            
        
    def refresh_row(self):
        item = QTableWidgetItem()
        item.setText(str(data['order']))
        self.grdMain.setItem(line, col, item)
    
        col += 1

    def up_click(self):
        row = self.grdMain.currentRow()
        if row > 0:
            current_data = json.loads(self.grdMain.item(row, 7).text())
            next_data = json.loads(self.grdMain.item(row-1, 7).text())
            self.refresh_table_line(current_data, row - 1)
            self.refresh_table_line(next_data, row)
            self.grdMain.selectRow(row -1)


    def down_click(self):
        row = self.grdMain.currentRow()
        if row < self.grdMain.rowCount() -1:
            current_data = json.loads(self.grdMain.item(row, 7).text())
            next_data = json.loads(self.grdMain.item(row+1, 7).text())
            self.refresh_table_line(current_data, row + 1)
            self.refresh_table_line(next_data, row)
            self.grdMain.selectRow(row +1)

    def get_row(self, linha):
        source_dict = {}
        if self.grdMain.cellWidget(linha, 0).isChecked():
            source_dict['data'] = True
        else:
            source_dict['data'] = False

        if self.grdMain.cellWidget(linha, 1).isChecked():
            source_dict['check'] = True
        else:
            source_dict['check'] = False

        source_dict['field'] = str(self.grdMain.item(linha,2).text())
        source_dict['layout'] = str(self.grdMain.cellWidget(linha, 3).currentText())
        source_dict['order'] = str(self.grdMain.item(linha,4).text())
        source_dict['control'] = str(self.grdMain.cellWidget(linha, 5).currentText())
        source_dict['label'] = str(self.grdMain.item(linha,6).text()).encode('utf-8')
        source_dict['ctrl_name'] = str(self.grdMain.item(linha,7).text())
        source_dict['size'] = str(self.grdMain.item(linha,8).text())
        source_dict['dictionary'] = str(self.grdMain.item(linha,9).text())
        source_dict['width'] = str(self.grdMain.item(linha,10).text())
        source_dict['height'] = str(self.grdMain.item(linha,11).text())
        if self.grdMain.item(linha,12) == None:
            source_dict['btn_label'] =''
        else:
            source_dict['btn_label'] = str(self.grdMain.item(linha,12).text())
        if self.grdMain.item(linha,13) == None:
            source_dict['btn_call'] = ''
        else:
            source_dict['btn_call'] = str(self.grdMain.item(linha,13).text())
        if self.grdMain.cellWidget(linha, 14).isChecked():
            source_dict['stretch'] = True
        else:
            source_dict['stretch'] = False
        return source_dict

    

    def update_row(self, data, line):
        col = 0
        
        item = QTableWidgetItem()
        dum = QComboBox()
        dum.addItems(self.ctrl_list)
        dum.setEditable(True)
        dum.setEditText(data['control'])
        item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.grdMain.setCellWidget(line, col,dum )  # go
        self.grdMain.setItem(line, col, item)

        col +=1
        
        item = QTableWidgetItem()
        dum = QComboBox()
        dum.addItems(['0','1','2','3','4','5'])
        dum.setEditable(True)
        item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.grdMain.setCellWidget(line, col,dum )  # layout
        dum.setEditText(data['layout'])
        self.grdMain.setItem(line, col, item)

        col +=1

        item = QTableWidgetItem()
        item.setText(str(data['order']))
        self.grdMain.setItem(line, col, item)
        
        col +=1


        item = QTableWidgetItem()
        item.setText(data['label'])
        self.grdMain.setItem(line, col, item)

        col +=1
        item = QTableWidgetItem()
        item.setText(data['ctrl_name'])
        self.grdMain.setItem(line, col, item)
        col +=1

        item = QTableWidgetItem()
        item.setText(str(data['size']))
        self.grdMain.setItem(line, col, item)

        col +=1
        item = QTableWidgetItem()
        item.setText(str(data['dictionary']))
        self.grdMain.setItem(line, col, item)

        col +=1
        item = QTableWidgetItem()
        item.setText(str(data['width']))
        self.grdMain.setItem(line, col, item)
        
        col +=1
        item = QTableWidgetItem()
        item.setText(str(data['height']))
        self.grdMain.setItem(line, col, item)
        
        col +=1
        item = QTableWidgetItem()
        item.setText(str(data['btn_label']))
        self.grdMain.setItem(line, col, item)

        col +=1
        item = QTableWidgetItem()
        item.setText(str(data['btn_call']))
        self.grdMain.setItem(line, col, item)

    def cancel_btn_click(self):
        self.close()

    def make_tab(selfsef):
        pass

    def make_data_model(self, fields):
        # pprint.pprint(fields)

        self.grdMain.setRowCount(0)
        
        linha = 0
        self.grdMain.setRowCount(len(fields))
        #print fields[-1]
        for n in fields:
            self.set_row(n, linha)
            linha += 1
        self.grdMain.resizeColumnsToContents()

    def set_row(self, n, linha):
        col = 0
        item = QTableWidgetItem() # dados
        item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.grdMain.setCellWidget(linha, 0, QCheckBox())
        self.grdMain.cellWidget(linha, 0).setChecked(True)
        self.grdMain.setItem(linha, 0, item)

        col +=1        

        item = QTableWidgetItem() # enable
        item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.grdMain.setCellWidget(linha, 1, QCheckBox())
        self.grdMain.cellWidget(linha, 1).setChecked(True)
        self.grdMain.setItem(linha, 1, item)
        col +=1
        
        item = QTableWidgetItem()
        item.setText(n['column_name'])
        self.grdMain.setItem(linha, 2, item)
        col +=1

        item = QTableWidgetItem()
        dum = QComboBox()
        dum.addItems(['0','1','2','3','4'])
        dum.setEditable(True)
        item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.grdMain.setCellWidget(linha, 3,dum )  # layout
        self.grdMain.setItem(linha, 3, item)
        col +=1

        
        item = QTableWidgetItem()
        item.setText('0')
        self.grdMain.setItem(linha, 4, item)

        col +=1
        item = QTableWidgetItem()
        dum = QComboBox()
        dum.addItems(self.ctrl_list)
        dum.setEditable(True)
        dum.setEditText(self.get_control(n['data_type']))
        item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.grdMain.setCellWidget(linha, 5,dum )  # go
        self.grdMain.setItem(linha, 5, item)

        col +=1
        item = QTableWidgetItem()
        item.setText(n['column_name'])
        self.grdMain.setItem(linha, 6, item)
        col +=1

        item = QTableWidgetItem()
        item.setText('self.' + n['column_name'])
        self.grdMain.setItem(linha, 7, item)
        col +=1

        item = QTableWidgetItem()
        if n['character_maximum_length'] == None : 
            item.setText('0')
        else:
            item.setText(str(n['character_maximum_length']))
        self.grdMain.setItem(linha, 8, item)
        col +=1

        item = QTableWidgetItem()
        item.setText('-1')
        self.grdMain.setItem(linha, 9, item)

        col +=1
        item = QTableWidgetItem()
        item.setText('0')
        self.grdMain.setItem(linha, 10, item)
        
        item = QTableWidgetItem()
        item.setText('0')
        self.grdMain.setItem(linha, 11, item)

        item = QTableWidgetItem()
        item.setText('')
        self.grdMain.setItem(linha, 12, item)

        item = QTableWidgetItem()
        item.setText('')
        self.grdMain.setItem(linha, 13, item)
        col +=1        

        item = QTableWidgetItem() # stretch
        item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.grdMain.setCellWidget(linha, 14, QCheckBox())
        self.grdMain.cellWidget(linha, 14).setChecked(False)
        self.grdMain.setItem(linha, 14, item)

    def get_control(self,data_type):
        toto = ''
        if data_type == 'boolean':
            toto = 'QCheckBox'
        elif data_type == 'character varying' or data_type == 'character' :
            toto = 'QLineEdit'
        elif data_type == 'text':
            toto = 'QPlainTextEdit'
        elif data_type == 'timestamp without time zone' or data_type == 'time without time zone' :
            toto = 'QDateTimeEdit'
        # elif data_type == ''
        elif data_type == 'date':
            toto = 'QDateEdit'
        elif data_type == 'numeric':
            toto = 'QDoubleSpinBox'
        elif data_type == 'smallint':
            toto = 'QSpinBox'
        elif data_type == 'integer':
            toto = 'QComboBox'
        return toto

    def make_form_code(self):
        print('make')
        pa.btn_calls = ''
        toto = ''
        TAB = ' ' *8
        l_stack = 0
        l_stack_str = ''
        self.tab_stack = 0
        self.tab_string = ''
        self.tab_page_stack = 0
        self.tab_page_string = ''

        print('linhas a processar:', self.grdMain.rowCount())

        for linha in range(0, self.grdMain.rowCount()):
            # if self.grdMain.cellWidget(linha, 1).isChecked() :
            data =self.get_row(linha)
            if int(data['layout']) == 0 and l_stack_str == '': # normal
                toto += TAB + data['ctrl_name'] + ' = ' + data['control'] + self.set_name(data)
                toto += self.set_width(data)
                toto += self.set_height(data)
                toto += self.set_size(data)
                if data['control'] in ['QPushButton','QToolButton']:
                    toto += TAB + 'masterLayout.addLayout(self.addHDumLayout(['  + data['ctrl_name']
                    self.add_connection(data)
                else:
                    toto += TAB + 'masterLayout.addLayout(self.addHDumLayout([' + self.set_label(data) + data['ctrl_name']
                
                if data['stretch']:
                    toto += ', True'
                toto += ']))\n'
                toto += '\n'

            elif int(data['layout']) > 0: # detectou layout
                if l_stack == int(data['layout']): # é igual ao do anterior, adiciona
                    toto += TAB + data['ctrl_name'] + ' = ' + data['control'] + self.set_name(data)
                    toto += self.set_width(data)
                    toto += self.set_height(data)
                    toto += self.set_size(data)
                    if data['control'] in ['QPushButton','QToolButton']:
                        l_stack_str += ',' + data['ctrl_name']
                        toto += self.add_connection(data)
                    else:
                        l_stack_str += ',' + self.set_label(data) + data['ctrl_name']

                elif l_stack != int(data['layout']): # 'e outro
                    # fecha o anterior
                    if l_stack_str != '':
                        toto += TAB + 'masterLayout.addLayout(self.addHDumLayout([' + l_stack_str + ']))\n'
                        l_stack_str = ''
                        toto += '\n'
                    # cria o novo control
                    toto += TAB + data['ctrl_name'] + ' = ' + data['control'] + self.set_name(data)
                    toto += self.set_width(data)
                    toto += self.set_height(data)
                    toto += self.set_size(data)
                    # adiciona ao stack para posterior utilização
                    if data['control'] in ['QPushButton','QToolButton']:
                        l_stack_str += data['ctrl_name']
                        toto += self.add_connection(data)
                    else:
                        l_stack_str += self.set_label(data) + data['ctrl_name']

                l_stack = int(data['layout'])
            elif int(data['layout']) == 0 and l_stack_str != '': # mudou para o laytou 0
                # fecha o anterior
                toto += TAB + 'masterLayout.addLayout(self.addHDumLayout([' + l_stack_str + ']))\n'
                toto += '\n'
                l_stack_str = ''
                l_stack = 0
                # adiciona o ctrl normal.
                toto += TAB + data['ctrl_name'] + ' = ' + data['control'] + self.set_name(data)
                toto += self.set_width(data)
                toto += self.set_height(data)
                toto += self.set_size(data)
                if data['control'] in ['QPushButton','QToolButton']:
                    toto += TAB + 'masterLayout.addLayout(self.addHDumLayout(['  + data['ctrl_name']
                    toto += self.add_connection(data)
                else:
                    toto += TAB + 'masterLayout.addLayout(self.addHDumLayout(['  + self.set_label(data) + data['ctrl_name']
                if data['stretch']:
                    toto += ', True'
                toto += ']))\n'
                toto += '\n'

        if l_stack_str != '': # mudou para o laytou 0
                # fecha o anterior
                toto += TAB + 'masterLayout.addLayout(self.addHDumLayout([' + l_stack_str + ']))\n'
                toto += '\n'

        print(toto)
        print('linhas geradas', len(toto))
        return str(toto)

    def add_connection(self,data):
        toto = ' ' * 8 + 'self.connect(' + data['ctrl_name'] + ', SIGNAL("clicked()"), self.' + data['btn_call'] + ')\n'        
        pa.btn_calls += ' ' * 4 + 'def ' + data['btn_call'] + ' (self):\n'
        pa.btn_calls += ' ' * 8 + 'pass\n'

        return toto

    def set_width(self, data):
        toto = ''
        if int(data['width']) > 0:
            toto += ' ' * 8 +  data['ctrl_name'] + '.setMaximumWidth(' + data['width'] + ')\n'
            toto += ' ' * 8 +  data['ctrl_name'] + '.setMinimumWidth(' + data['width'] + ')\n'

        return toto
    
    def set_height(self, data):
        toto = ''
        if int(data['height']) > 0:
            toto += ' ' * 8 +  data['ctrl_name'] + '.setMaximumHeight(' + data['height'] + ')\n'
            toto += ' ' * 8 +  data['ctrl_name'] + '.setMinimumHeight(' + data['height'] + ')\n'

        return toto

    def set_size(self,data):
        if data['control'] == 'QLineEdit':
            if int(data['size']) > 0 :
                return ' ' * 8 +  data['ctrl_name'] + '.setMaxLength(' + data['size'] + ')\n'
            else:
                return ''
        else:
            return ''

    def set_name(self,data):
        if data['control'] == 'QPushButton':
            toto = '(\'' + data['btn_label'] + '\')\n'
        elif data['control'] == 'QToolButton':
            toto = '()\n'
            toto += ' ' *8 + data['ctrl_name']  + '.setText(\'' + data['btn_label'] + '\')\n'
        else:
            toto = '()\n'
        return toto

    def set_label(self, data):
        if data['label'] == '':
            return ''
        else:
            return '\'' + data['label'] + '\', '

    def make_read_code(self):
        TAB = ' ' *8
        read = '    def refresh_form(self):\n'
        for linha in range(0, self.grdMain.rowCount()):
            if self.grdMain.cellWidget(linha, 0).isChecked() :
                data = self.get_row(linha)

                read += TAB + 'stdio.read_field(' + data['ctrl_name'] + ',\'' + data['field'] + '\',' + 'dict_' + ')\n\n'

        return read 

    def make_insert_code(self):
        print('make insert SQL')
        TAB = ' ' *8
        table = str(self.table_LineEdit.text())
        write = '    def insert_record(self):\n'
        write += TAB + 'sql = \'\'\'INSERT INTO ' + table + '(\n'
        write_fields = ''
        write_dict_item = ' ) VALUES ('
        write_controls = TAB + 'data = ()\n'
        for linha in range(0, self.grdMain.rowCount()):
            if self.grdMain.cellWidget(linha, 0).isChecked() :
                data = self.get_row(linha)
                write_fields += TAB + data['field'] + ',\n'
                write_dict_item += '%s,'
                if not data['dictionary'] == '-1':
                    foo = '),' + data['dictionary']  + ')'
                else:
                    foo = '),)'
                write_controls += TAB + 'data += (stdio.write_field(' + data['ctrl_name']  + foo + '\n'
                write += write_fields[:-3] + '\n' + TAB + write_dict_item[:-1] + ')\'\'\'\n' + write_controls + '\n'
        return write

    def make_update_code(self):
        TAB = ' ' *8
        table = str(self.table_LineEdit.text())
        index_field = str(self.index_field_LineEdit.text())
        write = '    def update_record(self):\n'
        write += TAB + 'sql = \'\'\'UPDATE ' + table + '\n'
        write_fields = ''
        write_dict_item = ' ) VALUES ('
        write_controls = TAB + 'data = ()\n'
        for linha in range(0, self.grdMain.rowCount()):
            if self.grdMain.cellWidget(linha, 0).isChecked() :
                data = self.get_row(linha)
                write_fields += TAB + data['field'] + '=%s,\n'
                write_dict_item += '%s,'
                if not data['dictionary'] == '-1' :
                    foo = '),' + data['dictionary']  + ')'
                else:
                    foo = '),)'
                write_controls += TAB + 'data += (stdio.write_field(' + data['ctrl_name']  + foo + '\n'
                write_fields = write_fields[:-3] + ' WHERE ' + index_field + '= %s\'\'\'\n\n'
                write += write_fields + write_controls
        return write
      

    def save_btn_click(self):
        members =  {}
        dict_index_key = 0
        for row in range(0, self.grdMain.rowCount()):
            line_data = json.loads(self.grdMain.item(row, 7).text())
            members[str((str(dict_index_key).zfill(2)))] = line_data
            dict_index_key +=1
        f = open('file.json', 'w')
        f.write(json.dumps(members))
        f.close()

    def load_btn_click(self):       
        f = open('file.json', 'r')
        members = json.load(open("file.json"))
        self.grdMain.setRowCount(len(members))
        row = 0
        for key, value in sorted(members.items()):
            self.refresh_table_line(value, row)
            row +=1
        self.grdMain.resizeColumnsToContents()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    
    def setSizes(self, object,w,h):       
        object.setMaximumHeight (h)
        object.setMinimumHeight(h)
        object.setMaximumWidth(w)
        object.setMinimumWidth(w)

    def setSizeWidth(self, object, value):
        object.setMaximumWidth(value)
        object.setMinimumWidth(value)

    def setBtnSquare(self, object,value=60):       
        object.setMaximumHeight (value)
        object.setMinimumHeight(value)
        object.setMaximumWidth(value)
        object.setMinimumWidth(value)

    def addHDumLayout(self, listobj1, label_size = 120, align = Qt.AlignRight):
        """ v 2.0 SET2012"""  
        dumLayout = QHBoxLayout()
        for n in listobj1:

            if (type(n)==str) or (type(n) == str):
                toto = QLabel(n)
                toto.setMinimumWidth(label_size)
                toto.setMaximumWidth(label_size)
                toto.setAlignment(align)
                dumLayout.addWidget(toto)
            elif type(n) == bool:
                dumLayout.addStretch()
            else:
                dumLayout.addWidget(n)
        return dumLayout
    def check_obj(self, obj):
        if type(obj) == QLineEdit:
            if obj.text().isEmpty():
                return False
            else:
                return True
        if type(obj) == QPlainTextEdit:
            if obj.toPlainText().isEmpty():
                return False
            else:
                return True
        
    def addVDumLayout(self, listobj1, label_size = 120, align = Qt.AlignVCenter|Qt.AlignRight):  
        """ v 2.0 SET2012"""  
        dumLayout = QVBoxLayout()
        for n in listobj1:        
            if (type(n)==str) or (type(n) == str):
                toto = QLabel(n)
                toto.setMinimumWidth(label_size)
                toto.setMaximumWidth(label_size)
                toto.setAlignment(align)
                dumLayout.addWidget(toto)
            elif type(n) == bool:
                dumLayout.addStretch()
            else:

                dumLayout.addWidget(n)
        return dumLayout

    def build_click(self):
        toto = ''
        import_code = self.make_import_code()
        class_code = self.make_class_code()
        stretch_code = self.add_stretch()
        main_code = self.make_main_code()
        toto = import_code + '\n' + class_code + '\n' + stretch_code + main_code
        sourceFile = open('./test.py', 'w')
        print(toto, file=sourceFile)
        sourceFile.close()
        from subprocess import Popen
        p = Popen(['python3','./test.py'])
    
    def make_import_code(self):
        block_import = '''#!/usr/bin/python\n# -*- coding: utf-8 -*-\n'''
        import_set = set()
        for linha in range(0, self.grdMain.rowCount()):
            if self.grdMain.item(linha, 0).text() in ['addStretch']:
                pass
            else:
                import_set.add(self.grdMain.item(linha, 0).text())
    
        import_set = list(import_set)
        block_import += 'import sys\n'
        block_import += 'from PyQt5.QtWidgets import QDialog, QApplication, QVBoxLayout, '
        for n in import_set:
            block_import += n + ', '
        return block_import[:-2] + '\n'
        
    def make_class_code(self):
        class_name = 'TestClass'
        class_code = 'class ' + class_name + '(QDialog):\n'
        class_code += TAB + 'def __init__(self, parent=None):\n'
        class_code += TAB + TAB + 'super(' + class_name + ', self).__init__(parent)\n'
        class_code += TAB +TAB + 'masterLayout = QVBoxLayout(self)\n'
        class_code += self.make_layouts()
        for line in range(0,self.grdMain.rowCount()):
            if self.grdMain.item(line, 3).text() != 'None':
                # print('add widget',self.grdMain.item(line, 0).text())
                class_code += self.widget_code({'widget_type': self.grdMain.item(line, 0).text(),
                                                'w_name': self.grdMain.item(line, 1).text(),
                                                'label':self.grdMain.item(line, 2).text(),
                                                'layout': self.grdMain.item(line, 3).text()})
                # class_code += TAB + TAB +  self.grdMain.item(line, 3).text() + '.addWidget(' + self.grdMain.item(line, 1).text() + ')\n'
            else:
                if self.grdMain.item(line, 0).text() in ['QVBoxLayout', 'QHBoxLayout','addStretch']:
                    pass
                else:
                    class_code += self.widget_code({'widget_type': self.grdMain.item(line, 0).text(),
                                                    'w_name': self.grdMain.item(line, 1).text(),
                                                    'label': self.grdMain.item(line, 2).text(),
                                                    'layout': 'masterLayout'})
                    # class_code += TAB + TAB + 'masterLayout.addWidget(' + self.grdMain.item(line, 1).text() + ')\n'
        class_code += self.add_layouts_code()
        return class_code
    
    def widget_code(self, data):
        widget_code = ''
        if data['widget_type'] == 'addStretch':
            pass
        else:
            if data['widget_type'] in ['QLabel', 'QPushButton','QCheckBox']:
                widget_code += TAB + TAB + data['w_name'] + ' = ' + data['widget_type'] +  '(\'''' + data['label'] + '''\')\n'''
            else:
                widget_code += TAB + TAB + data['w_name'] + ' = ' + data['widget_type'] + '()\n'
            widget_code += TAB + TAB + data['layout'] + '.addWidget(' + data['w_name'] + ')\n'
        return widget_code
    
    def make_main_code(self):
        class_name = 'TestClass'
        main_code = 'def main():\n'
        main_code += TAB + 'app = QApplication(sys.argv)\n'
        main_code += TAB + 'form = ' + class_name  + '()\n'
        main_code += TAB + 'form.show()\n'
        main_code += TAB + 'app.exec_()\n'
        main_code += '''if __name__ == '__main__':\n'''
        main_code += TAB + 'main()\n'
        return main_code

    def make_layouts(self):
        layouts_code = ''
        for linha in range(0, self.grdMain.rowCount()):
            h = self.grdMain.item(linha, 0).text()
            if h in ('QVBoxLayout', 'QHBoxLayout'):
                layouts_code += TAB + TAB + self.grdMain.item(linha, 1).text() + ' = ' + h + '()\n'
        return layouts_code
    
    def add_layouts_code(self):
        add_layouts_code = ''
        for linha in range(0, self.grdMain.rowCount()):
            h = self.grdMain.item(linha, 0).text()
            if h in ('QVBoxLayout', 'QHBoxLayout'):
                add_layouts_code += TAB + TAB + 'masterLayout.addLayout(' + self.grdMain.item(linha, 1).text() + ')\n'
        return add_layouts_code
    
    def add_stretch(self):
        stretch_code = ''
        for linha in range(0, self.grdMain.rowCount()):
            h = self.grdMain.item(linha, 0).text()
            if h == 'addStretch' and self.grdMain.item(linha, 3).text() != 'None':
                stretch_code += TAB + TAB + self.grdMain.item(linha, 3).text() + '.addStretch()\n'
            elif h == 'addStretch' and self.grdMain.item(linha, 3).text() == 'None':
                stretch_code += TAB + TAB + 'masterLayout.addStretch()\n'

        return stretch_code + '\n'

def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
