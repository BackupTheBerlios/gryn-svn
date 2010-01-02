# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uListSelect.ui'
#
# Created: Sat Jan  2 00:54:57 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uListSelect(object):
    def setupUi(self, uListSelect):
        uListSelect.setObjectName("uListSelect")
        uListSelect.resize(261, 579)
        font = QtGui.QFont()
        font.setFamily("Adobe Helvetica")
        font.setPointSize(12)
        uListSelect.setFont(font)
        self.vboxlayout = QtGui.QVBoxLayout(uListSelect)
        self.vboxlayout.setObjectName("vboxlayout")
        self.sTable = QtGui.QTableWidget(uListSelect)
        self.sTable.setObjectName("sTable")
        self.sTable.setColumnCount(0)
        self.sTable.setRowCount(0)
        self.vboxlayout.addWidget(self.sTable)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.wAll = QtGui.QPushButton(uListSelect)
        self.wAll.setAutoDefault(False)
        self.wAll.setDefault(False)
        self.wAll.setObjectName("wAll")
        self.hboxlayout.addWidget(self.wAll)
        spacerItem = QtGui.QSpacerItem(51, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.wInvert = QtGui.QPushButton(uListSelect)
        self.wInvert.setAutoDefault(False)
        self.wInvert.setObjectName("wInvert")
        self.hboxlayout.addWidget(self.wInvert)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        spacerItem1 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.wOK = QtGui.QPushButton(uListSelect)
        self.wOK.setAutoDefault(False)
        self.wOK.setObjectName("wOK")
        self.hboxlayout1.addWidget(self.wOK)
        self.wCancel = QtGui.QPushButton(uListSelect)
        self.wCancel.setAutoDefault(False)
        self.wCancel.setObjectName("wCancel")
        self.hboxlayout1.addWidget(self.wCancel)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(uListSelect)
        QtCore.QObject.connect(self.wCancel, QtCore.SIGNAL("clicked()"), uListSelect.slotCancel)
        QtCore.QObject.connect(self.wOK, QtCore.SIGNAL("clicked()"), uListSelect.slotOk)
        QtCore.QMetaObject.connectSlotsByName(uListSelect)

    def retranslateUi(self, uListSelect):
        uListSelect.setWindowTitle(QtGui.QApplication.translate("uListSelect", "Select one", None, QtGui.QApplication.UnicodeUTF8))
        self.wAll.setText(QtGui.QApplication.translate("uListSelect", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.wInvert.setText(QtGui.QApplication.translate("uListSelect", "Invert", None, QtGui.QApplication.UnicodeUTF8))
        self.wOK.setText(QtGui.QApplication.translate("uListSelect", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.wCancel.setText(QtGui.QApplication.translate("uListSelect", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uListSelect = QtGui.QDialog()
    ui = Ui_uListSelect()
    ui.setupUi(uListSelect)
    uListSelect.show()
    sys.exit(app.exec_())

