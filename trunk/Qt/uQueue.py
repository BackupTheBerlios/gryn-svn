# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uQueue.ui'
#
# Created: Sat Jan  2 00:55:15 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uQueue(object):
    def setupUi(self, uQueue):
        uQueue.setObjectName("uQueue")
        uQueue.resize(600, 223)
        font = QtGui.QFont()
        font.setFamily("Adobe Helvetica")
        font.setPointSize(12)
        uQueue.setFont(font)
        self.vboxlayout = QtGui.QVBoxLayout(uQueue)
        self.vboxlayout.setObjectName("vboxlayout")
        self.wTableet = QtGui.QTableWidget(uQueue)
        self.wTableet.setObjectName("wTableet")
        self.wTableet.setColumnCount(0)
        self.wTableet.setRowCount(0)
        self.vboxlayout.addWidget(self.wTableet)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(221, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.wOK = QtGui.QPushButton(uQueue)
        self.wOK.setAutoDefault(False)
        self.wOK.setObjectName("wOK")
        self.hboxlayout.addWidget(self.wOK)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(uQueue)
        QtCore.QMetaObject.connectSlotsByName(uQueue)

    def retranslateUi(self, uQueue):
        self.wOK.setText(QtGui.QApplication.translate("uQueue", "OK", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uQueue = QtGui.QDialog()
    ui = Ui_uQueue()
    ui.setupUi(uQueue)
    uQueue.show()
    sys.exit(app.exec_())

