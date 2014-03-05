#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import sqlite3
from PySide import QtGui
from PySide import QtCore
import os
from ConfigParser import SafeConfigParser
import psycopg2
from threading import Thread


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        #check database connection

        parser = SafeConfigParser()
        parser.read('postgis.ini')

        self.postgisdatabase = parser.get('postgis configuration', 'postgisdatabase')
        self.postgisusername = parser.get('postgis configuration', 'postgisusername')
        self.postgispassword = parser.get('postgis configuration', 'postgispassword')
        self.postgishost = parser.get('postgis configuration', 'postgishost')
        self.postgisport = parser.get('postgis configuration', 'postgisport')
        self.postgisschema = parser.get('postgis configuration', 'postgisschema')
        self.postgistable = parser.get('postgis configuration', 'postgistable')
        self.postgiscolumn = parser.get('postgis configuration', 'postgiscolumn')
        self.searchmethod = parser.get('postgis configuration', 'searchmethod')


        self.postgisconnectionstring = ("dbname=" + self.postgisdatabase + " " + "user=" + self.postgisusername + " " + "password=" + self.postgispassword + " " + "host=" + self.postgishost + " " + "port=" + self.postgisport)
        try:
            connection = psycopg2.connect(self.postgisconnectionstring)
        except Exception:
            pass

        def resource_path(relative_path):
            """ Get absolute path to resource, works for dev and for PyInstaller """
            try:
                # PyInstaller creates a temp folder and stores path in _MEIPASS
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)


        icon = resource_path("os_icon.png")
        print icon

        self.setWindowIcon(QtGui.QIcon(icon))

        self.search = QtGui.QLabel('Search:')
        self.results = QtGui.QLabel('Results')

        self.searchEdit = QtGui.QLineEdit()
        self.resultsTable = QtGui.QTableWidget()

        self.exitButton = QtGui.QPushButton("Exit", self)
        self.exitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)

        self.searchEdit.textChanged.connect(self.countSearch)

        self.searchhbox = QtGui.QHBoxLayout()
        self.searchhbox.addWidget(self.search)
        self.searchhbox.addWidget(self.searchEdit)

        self.resultshbox = QtGui.QHBoxLayout()
        self.resultshbox.addWidget(self.results)
        self.resultshbox.addWidget(self.resultsTable)

        self.buttonhbox = QtGui.QHBoxLayout()
        self.buttonhbox.addWidget(self.exitButton)

        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addLayout(self.searchhbox)
        self.vbox.addLayout(self.resultshbox)
        self.vbox.addLayout(self.buttonhbox)

        self.setLayout(self.vbox)

        self.setGeometry(500, 800, 600, 500)
        self.setWindowTitle('AddressBase PostGIS Search Tool')
        self.center()
        self.show()

    def countSearch(self):
        self.searchtext = self.searchEdit.text()

        if len(self.searchtext) > 3:
            self.thread = Thread(target=self.searchClicked())
            self.thread.start()


    def searchClicked(self):

        connection = psycopg2.connect(self.postgisconnectionstring)

        cursor = connection.cursor()

        if self.searchmethod == 'FTS':
            sqlqry = """SELECT uprn, parent_uprn, usrn, geo_single_address_label FROM %s.%s WHERE %s @@ plainto_tsquery('english', '%s')
            OR LIMIT 100;"""%(self.postgisschema, self.postgistable, self.postgiscolumn, self.searchtext)

        elif self.searchmethod == 'LIKE':
            sqlqry = "SELECT uprn, parent_addressable_uprn, rm_udprn, address FROM %s.%s WHERE %s LIKE '%s%' LIMIT 100;"%(self.postgisschema, self.postgistable, self.postgiscolumn, self.searchEdit.text())

        cursor.execute(sqlqry)

        data = cursor.fetchall()

        totalrows = len(data)
        totalcolumns = 4

        i = 1
        j = 0

        self.resultsTable.setRowCount(totalrows)
        self.resultsTable.setColumnCount(4)
        self.resultsTable.setSortingEnabled(False)
        self.resultsTable.setHorizontalHeaderLabels(['UPRN', 'Parent UPRN','RM UDPRN',  'Address'])

        for i, row in enumerate(data):
            #QMessageBox.about(self, "My message box", str(row))
            for j, col in enumerate(row):
                try:
                    self.resultsTable.setItem(i, j, QtGui.QTableWidgetItem(str(col)))

                except:
                    unicode = col.encode('utf-8')
                    self.resultsTable.setItem(i, j, QtGui.QTableWidgetItem(str(unicode)))

        self.resultsTable.resizeColumnsToContents()


    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()