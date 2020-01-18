#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import platform
import sys
import string
import time
import datetime


from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, \
    QTableWidget, QMenu, QPushButton, QDialog, QTableWidgetItem, QPlainTextEdit,QSpinBox,\
    QWidget, QMainWindow, QApplication, QMessageBox, QStyleFactory, QCheckBox, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


def print_listo_2_file(name,content_list):
    f = open(name,'w')
    print >>f, content_list

def read_file(file_name, mode = 1):
    try:
        f = open(file_name, "r")
        try:
            if mode == 1:
                # lines into a list.
                toto = f.readlines()
            elif mode == 2:
                # Read the entire contents of a file at once.
                toto = f.read()
            elif mode == 3:
                # OR read one line at a time.
                toto= f.readline()
            
        finally:
            f.close()
    except IOError:
        toto = 'error' 

    return toto



def print2file(name,content):
    f = open(name,'w')
    print >>f, content

def read_file(file_name, mode = 1):
    try:
        f = open(file_name, "r")
        try:
            if mode == 1:
                # lines into a list.
                toto = f.readlines()
            elif mode == 2:
                # Read the entire contents of a file at once.
                toto = f.read()
            elif mode == 3:
                # OR read one line at a time.
                toto= f.readline()
            
        finally:
            f.close()
    except IOError:
        toto = 'error' 

    return toto


def write(obj, dic = {}):
        a = type(obj)
        if a == QLineEdit:
            return unicode(obj.text())
        elif a == QCheckBox:
            return obj.isChecked()
        elif a == QPlainTextEdit:
            return unicode(obj.toPlainText())
        elif a == QComboBox:
            return dic[obj.currentText()]



def read_field(obj,field,dic):
    try:
        a = type(obj)
        toto = dic[field]
        if toto == None:
            pass
        elif a == QCheckBox:
            obj.setChecked(toto)
        elif a == QLineEdit:
            if type(toto) == int :
                obj.setText(str(toto))
            else:
                obj.setText(toto.decode('utf-8'))
        elif a == QTextEdit:
            obj.setText(toto.decode('utf-8'))
        elif a == QPlainTextEdit:
            obj.appendPlainText(toto.decode('utf-8'))
        elif a == QComboBox:
            obj.setEditable(True)
            obj.setEditText(toto.decode('utf-8'))
        elif a == QDateEdit:
            obj.setDate(toto)
    except e:

        print('erro em def read_record()')
        print(str(e) +  '\n ', obj.objectName() ,'\nin field:', field,'\nin dic:',dic)
        


if __name__ == '__main__':
    print('não corre')