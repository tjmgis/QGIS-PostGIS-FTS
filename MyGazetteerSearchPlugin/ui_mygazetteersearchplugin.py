# -*- coding: utf-8 -*-

"""
Module implementing MyGazetteerSearchPluginDialog.
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sqlite3
import os
import sys
import time


from qgis.core import *
from qgis.gui import *
from qgis.utils import *

import urllib

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
    def on_searchText_textChanged(self, p0):
        """
        Slot documentation goes here.
        """
        self.searchItem = self.searchText.text()
        self.search()
    
    @pyqtSignature("")
    def on_cancelButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.close()
    
    @pyqtSignature("int, int")
    def on_tableWidget_cellClicked(self, row, column):
        """
        Slot documentation goes here.
        """
        
        rownumber = row
        columnnumber = column
        
        location = self.tableWidget.item(rownumber,  0).text()
        x = self.tableWidget.item(rownumber, 2).text()
        y = self.tableWidget.item(rownumber,  3).text()
        
        mapx = float(x)
        mapy = float(y)
        
        fields = [QgsField("Location Name", QVariant.String) ]
        
        self.pinLayer =  QgsVectorLayer("Point?crs=epsg:27700&field=id:integer&field=Location:string(120)&index=yes",  location,  "memory")
        QgsMapLayerRegistry.instance().addMapLayer(self.pinLayer)
        
        symbols = self.pinLayer.rendererV2().symbols()
        symbol = symbols[0]
        symbol.setColor(QColor.fromRgb(255, 0, 0))
        iface.mapCanvas().refresh() 
        iface.legendInterface().refreshLayerSymbology(self.pinLayer)
        
        # add a feature
        feature = QgsFeature()
        feature.addAttribute(0,1)
        feature.addAttribute(1,location)
        feature.setGeometry( QgsGeometry.fromPoint(QgsPoint(mapx, mapy)) )
        
        self.pinLayer.startEditing()
        #feature.setAttributes([1, "Hello"])
        
        self.pinLayer.addFeature(feature, True)
        self.pinLayer.commitChanges()
        
        iface.mapCanvas().setExtent(QgsRectangle(mapx,mapy,mapx,mapy))
        iface.mapCanvas().zoomScale(10000)
        iface.mapCanvas().refresh()
        
        self.close()
        
        
        
       
        
        
    def search(self):
        #conn = sqlite3.connect("C:\\Projects\\QGIS Plugin Workshop\\short_gaz.sqlite")
        
        self.sqlite_path = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "python/plugins/mygazetteersearchplugin/Lookup/" + "lookup2.sqlite"
        
        try:
        
            conn = sqlite3.connect(str(self.sqlite_path))
            cursor = conn.cursor()
            
            sqlqry = "SELECT location, locality, eastings, northings FROM lookup WHERE location LIKE '%s' LIMIT 100;"%("%"+self.searchItem+"%")
            
            cursor.execute(sqlqry)
            
            data = cursor.fetchall()
            
            totalrows = len(data)
            totalcolumns = 4
            
            i = 1
            j = 0
            
            self.tableWidget.setRowCount(totalrows)
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setSortingEnabled(False)
            self.tableWidget.setHorizontalHeaderLabels(['Location', 'Locality','Easting',  'Northing'])
            
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
        
        except sqlite3.Error,  e:
            QMessageBox.information(self, "HTTP Error", "Unable to download file")
        
