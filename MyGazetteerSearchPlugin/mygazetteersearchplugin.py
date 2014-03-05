# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MyGazetteerSearchPlugin
                                 A QGIS plugin
 A search plugin that queries a local SQLite database
                              -------------------
        begin                : 2013-09-20
        copyright            : (C) 2013 by Tim Martin
        email                : Tim.Martin@ordnancesurvey.co.uk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from ui_mygazetteersearchplugin import MyGazetteerSearchPluginDialog

import urllib2
import sys
import os
import tempfile
import shutil
import zipfile



class MyGazetteerSearchPlugin:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/mygazetteersearchplugin"
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale").toString()[0:2]

        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/mygazetteersearchplugin_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = MyGazetteerSearchPluginDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/mygazetteersearchplugin/search.png"),
            u"Gazetteer Search Plugin", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Gazetteer Search Plugin", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Gazetteer Search Plugin", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        #self.sqlite_path = "C:\\Temp\\data.sqlite"
        self.sqlite_path = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "python/plugins/mygazetteersearchplugin/lookup/" + "lookup2.sqlite"
        if os.path.isfile(self.sqlite_path): 
        # show the dialog
            self.dlg.show()
        # Run the dialog event loop
            result = self.dlg.exec_()
        # See if OK was pressed
            if result == 1:
                # do something useful (delete the line containing pass and
                # substitute with your code)
                pass
        else:
            msg = "Lookup SQLite must be downloaded to use this plugin, do you wish to continue?"
            goahead = QMessageBox.question(self.iface.mainWindow(), "Download Message", msg, QMessageBox.Yes, QMessageBox.No)
            if goahead == QMessageBox.Yes:
                self.download_sqlite()
            else:
                pass
                
    def download_sqlite(self):
        lookup_path = os.path.join(os.path.dirname(__file__), 'Lookup')
        if not os.path.exists(lookup_path):
            os.makedirs(lookup_path)
        url = ("https://s3-eu-west-1.amazonaws.com/osdatabucket/lookup2.zip")
        try:
            print "downloading with urllib2"
            f = urllib2.urlopen(url)
            total_size = int(f.info().getheader('Content-Length').strip())
            downloaded = 0
            CHUNK = 256 * 10240
            dlbar = QProgressBar()
            dlbar.setMinimum(0)
            dlbar.setMaximum(total_size)
            
            zip_temp = tempfile.NamedTemporaryFile(mode='w+b', suffix='.zip', delete=False)
            zip_temp_n = zip_temp.name
            zip_temp.seek(0)
            
            with open(zip_temp_n, "wb") as code:
                while True:
                    dlbar.show()
                    chunk = f.read(CHUNK)
                    downloaded += len(chunk)
                    dlbar.setValue(downloaded)
                    if not chunk:
                        break
                    code.write(chunk)
        
                
        except urllib2.HTTPError, e:
            QMessageBox.information(self.iface.mainWindow(), "HTTP Error", "Unable to download file")
        lookup_zip = zipfile.ZipFile(zip_temp)
        lookup_zip.extractall(lookup_path)
        dlbar.hide()
        zip_temp.close()
        self.run()
        
            
            
            
            
            
            
