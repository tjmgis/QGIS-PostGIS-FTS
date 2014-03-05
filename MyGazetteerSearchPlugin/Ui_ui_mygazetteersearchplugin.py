# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\tjmartin\.qgis\python\plugins\MyGazetteerSearchPlugin\ui_mygazetteersearchplugin.ui'
#
# Created: Tue Sep 24 14:14:16 2013
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MyGazetteerSearchPlugin(object):
    def setupUi(self, MyGazetteerSearchPlugin):
        MyGazetteerSearchPlugin.setObjectName(_fromUtf8("MyGazetteerSearchPlugin"))
        MyGazetteerSearchPlugin.resize(477, 411)
        self.title = QtGui.QLabel(MyGazetteerSearchPlugin)
        self.title.setGeometry(QtCore.QRect(190, 20, 141, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.title.setFont(font)
        self.title.setObjectName(_fromUtf8("title"))
        self.searchLabel = QtGui.QLabel(MyGazetteerSearchPlugin)
        self.searchLabel.setGeometry(QtCore.QRect(80, 60, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.searchLabel.setFont(font)
        self.searchLabel.setObjectName(_fromUtf8("searchLabel"))
        self.searchText = QtGui.QLineEdit(MyGazetteerSearchPlugin)
        self.searchText.setGeometry(QtCore.QRect(170, 60, 171, 20))
        self.searchText.setObjectName(_fromUtf8("searchText"))
        self.resultsLabel = QtGui.QLabel(MyGazetteerSearchPlugin)
        self.resultsLabel.setGeometry(QtCore.QRect(20, 97, 46, 13))
        self.resultsLabel.setObjectName(_fromUtf8("resultsLabel"))
        self.cancelButton = QtGui.QPushButton(MyGazetteerSearchPlugin)
        self.cancelButton.setGeometry(QtCore.QRect(390, 370, 75, 23))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.tableWidget = QtGui.QTableWidget(MyGazetteerSearchPlugin)
        self.tableWidget.setGeometry(QtCore.QRect(10, 120, 451, 241))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.retranslateUi(MyGazetteerSearchPlugin)
        QtCore.QMetaObject.connectSlotsByName(MyGazetteerSearchPlugin)

    def retranslateUi(self, MyGazetteerSearchPlugin):
        MyGazetteerSearchPlugin.setWindowTitle(_translate("MyGazetteerSearchPlugin", "MyGazetteerSearchPlugin", None))
        self.title.setText(_translate("MyGazetteerSearchPlugin", "Find a Location", None))
        self.searchLabel.setText(_translate("MyGazetteerSearchPlugin", "Search For:", None))
        self.resultsLabel.setText(_translate("MyGazetteerSearchPlugin", "Results", None))
        self.cancelButton.setText(_translate("MyGazetteerSearchPlugin", "Close", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MyGazetteerSearchPlugin = QtGui.QDialog()
    ui = Ui_MyGazetteerSearchPlugin()
    ui.setupUi(MyGazetteerSearchPlugin)
    MyGazetteerSearchPlugin.show()
    sys.exit(app.exec_())

