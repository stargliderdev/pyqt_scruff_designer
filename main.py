#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget, QLabel, QVBoxLayout, QLineEdit, QComboBox, \
    QTableWidget, QMenu, QPushButton, QDialog, QTableWidgetItem, QPlainTextEdit, QSpinBox, \
    QWidget, QTabWidget, QApplication, QMessageBox, QStyleFactory, QToolButton, QAction, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
import json

import parameters as gl
import properties

TAB = '    '

class MainWindow(QDialog):
    def __init__(self,  parent = None):
        super(MainWindow,  self).__init__(parent)
        self.resize(1024, 768)
        self.center()
        self.setWindowTitle('PyQt Scruff Designer')

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
        
        self.upBtn = QToolButton()
        self.upBtn.setIcon(QIcon('up.png'))
        self.upBtn.clicked.connect(self.up_click)
        

        self.downBtn = QToolButton()
        self.downBtn.setIcon(QIcon('down.png'))
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
        self.grdMain.setColumnWidth(7,0)
        self.grdMain.cellDoubleClicked.connect(self.cell_click)
        
        designLayout = QHBoxLayout()
        designLayout.addWidget(self.grdMain)
        tabLayout.addLayout(designLayout)

        okBtn = QPushButton('Make')
        okBtn.clicked.connect(self.preview_click)
        showBtn = QPushButton('Show')
        showBtn.clicked.connect(self.show_click)
        self.saveBtn = QPushButton('Save')
        self.saveBtn.clicked.connect(self.save_btn_click)
        
        self.loadBtn = QPushButton('Load')
        self.loadBtn.clicked.connect(self.load_btn_click)
        self.cancelBtn = QPushButton('Cancela')
        self.cancelBtn.clicked.connect(self.cancel_btn_click)
        
        tabLayout.addLayout(self.addHDumLayout([okBtn, showBtn, self.saveBtn, self.loadBtn, self.cancelBtn]))
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
    
    def cell_click(self, row,col):
        if col == 0:
            data = json.loads(self.grdMain.item(row, 7).text())
            data['new']= False
            self.update_layouts()
            form = properties.Properties(data)
            form.exec_()
            if form.ret['responce']:
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
        self.grdMain.setColumnWidth(7, 0)
        
    def refresh_table_line(self, data, row):
        item = QTableWidgetItem()
        item.setText(data['widget'])
        self.grdMain.setItem(row, 0, item)
        item = QTableWidgetItem()
        item.setText(data['widget_name'])
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
        source_dict['widget'] = str(self.grdMain.cellWidget(linha, 5).currentText())
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
  
    def cancel_btn_click(self):
        self.close()

     

    def save_btn_click(self):
        fileName, selectedFilter = QFileDialog.getSaveFileName(
            self, self.tr("Save Design"), "./", self.tr("*.json"), None)
        
        if fileName !='':
            members =  {}
            dict_index_key = 0
            for row in range(0, self.grdMain.rowCount()):
                line_data = json.loads(self.grdMain.item(row, 7).text())
                members[str((str(dict_index_key).zfill(2)))] = line_data
                dict_index_key +=1
            f = open(fileName, 'w')
            f.write(json.dumps(members))
            f.close()

    def load_btn_click(self):
        fileName, selectedFilter = QFileDialog.getOpenFileName(
            self, self.tr("Open Design"), "./", self.tr("*.json"), None)
    
        if fileName != '':
            # f = open('file.json', 'r')
            members = json.load(open(fileName))
            self.grdMain.setRowCount(len(members))
            row = 0
            for key, value in sorted(members.items()):
                self.refresh_table_line(value, row)
                row +=1

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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

    def show_click(self):
        toto = self.build()
        import show
        form = show.ShowCode(toto)
        form.exec_()
        
    def preview_click(self):
        toto = self.build()
        sourceFile = open('./test.py', 'w')
        print(toto, file=sourceFile)
        sourceFile.close()
        from subprocess import Popen
        p = Popen(['python3','./test.py'])

    def build(self):
        toto = ''
        import_code = self.make_import_code()
        class_code = self.make_class_code()
        stretch_code = self.add_stretch()
        main_code = self.make_main_code()
        toto = import_code + '\n' + class_code + '\n' + stretch_code + main_code
        return toto
        
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
        class_code += TAB +TAB + gl.LAYOUT_DEFAULT + ' = QVBoxLayout(self)\n'
        class_code += self.make_layouts()
        for line in range(0,self.grdMain.rowCount()):
            
            if self.grdMain.item(line, 3).text() != 'None':
                class_code += self.widget_code(json.loads(self.grdMain.item(line,7).text()))
            else:
                if self.grdMain.item(line, 0).text() in ['QVBoxLayout', 'QHBoxLayout','addStretch']:
                    pass
                else:
                    class_code += self.widget_code(json.loads(self.grdMain.item(line, 7).text()))
        class_code += self.add_layouts_code()
        return class_code
    
    def widget_code(self, data):
        widget_code = ''
        if data['layout'] == 'None': data['layout'] = gl.LAYOUT_DEFAULT
        if data['widget'] == 'addStretch':
            pass
        else:
            if data['widget'] in ['QLabel', 'QPushButton','QCheckBox']:
                widget_code += TAB + TAB + data['widget_name'] + ' = ' + data['widget'] +  '(\'''' + data['label'] + '''\')\n'''
            else:
                widget_code += TAB + TAB + data['widget_name'] + ' = ' + data['widget'] + '()\n'
            if data['max_width'] != '-1':
                widget_code += TAB + TAB + data ['widget_name'] + '.setMaximumWidth(' + data['max_width'] + ')\n'
            if data['min_width'] != '-1':
                widget_code += TAB + TAB + data ['widget_name'] + '.setMinimumWidth(' + data['min_width'] + ')\n'
            if data['max_height'] != '-1':
                widget_code += TAB + TAB + data['widget_name'] + '.setMaximumHeight(' + data['max_height'] + ')\n'
            if data['min_height'] != '-1':
                widget_code += TAB + TAB + data['widget_name'] + '.setMinimumHeight(' + data['min_height'] + ')\n'
            widget_code += TAB + TAB + data['layout'] + '.addWidget(' + data['widget_name'] + ')\n'
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
