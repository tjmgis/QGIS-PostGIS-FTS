# -*- coding: utf-8 -*-

"""
Module implementing MyGazetteerSearchPluginDialog.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sqlite3
import os
import sys


from qgis.core import *
from qgis.gui import *

from Ui_ui_mygazetteersearchplugin import Ui_MyGazetteerSearchPlugin

class MyGazetteerSearchPluginDialog(QDialog, Ui_MyGazetteerSearchPlugin):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("QString")
    def on_searchText_textEdited(self, p0):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        #self.resultsList.clear()
        #self.tableView.clear()
        self.searchItem = self.searchText.text()
        self.search()
        
    
    @pyqtSignature("QTableWidgetItem*")
    def on_resultsList_itemClicked(self, item):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        
        #result = str(item.text())
        #QMessageBox.about(self, "My message box", "%s")%(result)
        
        
        QMessageBox.about(self, "My message box", "%s")%(item)
        
       
    
    @pyqtSignature("")
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
        
    def search(self):
        
        #conn = sqlite3.connect("C:\\Projects\\QGIS Plugin Workshop\\short_gaz.sqlite")
       # cur = conn.cursor()
        #sqlqry = "SELECT name, eastings, northings FROM lookup WHERE name LIKE '%s' LIMIT 100;"%("%"+self.searchItem+"%")
        #sqlqry = "SELECT name FROM lookup"
        #try:
            #c = cur.execute(sqlqry)
           # data = c.fetchall()            
            #for i in data:
                
                #self.resultsList.addItem(i[0])
        conn = sqlite3.connect("C:\\Projects\\QGIS Plugin Workshop\\short_gaz.sqlite")
        cursor = conn.cursor()
        
        sqlqry = "SELECT name, eastings, northings FROM lookup WHERE name LIKE '%s' LIMIT 100;"%("%"+self.searchItem+"%")
        cursor.execute(sqlqry)
        
        data = cursor.fetchall()
        
        totalrows = len(data)
        totalcolumns = 3
        
        i = 1
        j = 0
        
        self.tableWidget.setRowCount(totalrows)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setHorizontalHeaderLabels(['Location', 'Easting',  'Northing'])
        
        #for i in range(totalrows):
            #for j in range(totalcolumns):
               # item = QTableWidgetItem('%s%s' % (i, j))
                #self.tableWidget.setItem(i, j, item)
        for i, row in enumerate(data):
            #QMessageBox.about(self, "My message box", str(row))
            for j, col in enumerate(row):
                try:
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(col)))
                    
                except:
                    unicode = col.encode('utf-8')
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(unicode)))
                    
                #item = QTableWidgetItem(col)
                
                #QMessageBox.about(self, "My message box", "Item is:%s, i is: %s, j is: %s"%(col,  i,  j))
            
                
                
        #except sqlite3.Error, e:
    
            #QMessageBox.about(self, "My message box", "wrong")
            
       
        
        
    
