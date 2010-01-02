# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uVat.ui'
#
# Created: Sat Jan  2 00:55:19 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uVat(object):
    def setupUi(self, uVat):
        uVat.setObjectName("uVat")
        uVat.resize(458, 282)
        self.vboxlayout = QtGui.QVBoxLayout(uVat)
        self.vboxlayout.setObjectName("vboxlayout")
        self.wTable = QtGui.QTableWidget(uVat)
        self.wTable.setObjectName("wTable")
        self.wTable.setColumnCount(0)
        self.wTable.setRowCount(0)
        self.vboxlayout.addWidget(self.wTable)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.wSave = QtGui.QPushButton(uVat)
        self.wSave.setDefault(False)
        self.wSave.setObjectName("wSave")
        self.hboxlayout.addWidget(self.wSave)
        self.wCancel = QtGui.QPushButton(uVat)
        self.wCancel.setAutoDefault(False)
        self.wCancel.setObjectName("wCancel")
        self.hboxlayout.addWidget(self.wCancel)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(uVat)
        QtCore.QMetaObject.connectSlotsByName(uVat)

    def retranslateUi(self, uVat):
        uVat.setWindowTitle(QtGui.QApplication.translate("uVat", "uVat", None, QtGui.QApplication.UnicodeUTF8))
        self.wSave.setText(QtGui.QApplication.translate("uVat", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.wCancel.setText(QtGui.QApplication.translate("uVat", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uVat = QtGui.QDialog()
    ui = Ui_uVat()
    ui.setupUi(uVat)
    uVat.show()
    sys.exit(app.exec_())

