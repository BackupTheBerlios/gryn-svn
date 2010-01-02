# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uSourceVat.ui'
#
# Created: Sat Jan  2 00:55:07 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uSourceVat(object):
    def setupUi(self, uSourceVat):
        uSourceVat.setObjectName("uSourceVat")
        uSourceVat.resize(287, 144)
        self.vboxlayout = QtGui.QVBoxLayout(uSourceVat)
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.textLabel1 = QtGui.QLabel(uSourceVat)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName("textLabel1")
        self.hboxlayout.addWidget(self.textLabel1)
        self.wPeriod = QtGui.QComboBox(uSourceVat)
        self.wPeriod.setObjectName("wPeriod")
        self.hboxlayout.addWidget(self.wPeriod)
        self.vboxlayout.addLayout(self.hboxlayout)
        spacerItem = QtGui.QSpacerItem(20, 31, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        spacerItem1 = QtGui.QSpacerItem(41, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.wCancel = QtGui.QPushButton(uSourceVat)
        self.wCancel.setAutoDefault(False)
        self.wCancel.setObjectName("wCancel")
        self.hboxlayout1.addWidget(self.wCancel)
        self.wOK = QtGui.QPushButton(uSourceVat)
        self.wOK.setObjectName("wOK")
        self.hboxlayout1.addWidget(self.wOK)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(uSourceVat)
        QtCore.QMetaObject.connectSlotsByName(uSourceVat)

    def retranslateUi(self, uSourceVat):
        uSourceVat.setWindowTitle(QtGui.QApplication.translate("uSourceVat", "VAT transfer", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("uSourceVat", "Period to transfer", None, QtGui.QApplication.UnicodeUTF8))
        self.wCancel.setText(QtGui.QApplication.translate("uSourceVat", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.wOK.setText(QtGui.QApplication.translate("uSourceVat", "OK", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uSourceVat = QtGui.QDialog()
    ui = Ui_uSourceVat()
    ui.setupUi(uSourceVat)
    uSourceVat.show()
    sys.exit(app.exec_())

