# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uTimeFrameSelect.ui'
#
# Created: Sat Jan  2 00:55:09 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uTimeFrameSelect(object):
    def setupUi(self, uTimeFrameSelect):
        uTimeFrameSelect.setObjectName("uTimeFrameSelect")
        uTimeFrameSelect.resize(272, 197)
        font = QtGui.QFont()
        font.setFamily("Adobe Helvetica")
        font.setPointSize(12)
        uTimeFrameSelect.setFont(font)
        self.vboxlayout = QtGui.QVBoxLayout(uTimeFrameSelect)
        self.vboxlayout.setObjectName("vboxlayout")
        self.wFrame = QtGui.QGroupBox(uTimeFrameSelect)
        self.wFrame.setObjectName("wFrame")
        self.vboxlayout1 = QtGui.QVBoxLayout(self.wFrame)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.rPeriode = QtGui.QRadioButton(self.wFrame)
        self.rPeriode.setObjectName("rPeriode")
        self.hboxlayout.addWidget(self.rPeriode)
        self.wPeriode = QtGui.QComboBox(self.wFrame)
        self.wPeriode.setObjectName("wPeriode")
        self.hboxlayout.addWidget(self.wPeriode)
        self.vboxlayout1.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.rDate = QtGui.QRadioButton(self.wFrame)
        self.rDate.setObjectName("rDate")
        self.hboxlayout1.addWidget(self.rDate)
        self.wDateFrom = DateEdit(self.wFrame)
        self.wDateFrom.setObjectName("wDateFrom")
        self.hboxlayout1.addWidget(self.wDateFrom)
        self.wDateTo = DateEdit(self.wFrame)
        font = QtGui.QFont()
        font.setFamily("Adobe Helvetica")
        font.setPointSize(12)
        self.wDateTo.setFont(font)
        self.wDateTo.setObjectName("wDateTo")
        self.hboxlayout1.addWidget(self.wDateTo)
        self.vboxlayout1.addLayout(self.hboxlayout1)
        self.rAll = QtGui.QRadioButton(self.wFrame)
        self.rAll.setObjectName("rAll")
        self.vboxlayout1.addWidget(self.rAll)
        self.vboxlayout.addWidget(self.wFrame)
        spacerItem = QtGui.QSpacerItem(20, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")
        spacerItem1 = QtGui.QSpacerItem(51, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)
        self.wOk = QtGui.QPushButton(uTimeFrameSelect)
        self.wOk.setObjectName("wOk")
        self.hboxlayout2.addWidget(self.wOk)
        self.wCancel = QtGui.QPushButton(uTimeFrameSelect)
        self.wCancel.setObjectName("wCancel")
        self.hboxlayout2.addWidget(self.wCancel)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(uTimeFrameSelect)
        QtCore.QMetaObject.connectSlotsByName(uTimeFrameSelect)

    def retranslateUi(self, uTimeFrameSelect):
        uTimeFrameSelect.setWindowTitle(QtGui.QApplication.translate("uTimeFrameSelect", "Select ledger entry periode", None, QtGui.QApplication.UnicodeUTF8))
        self.wFrame.setTitle(QtGui.QApplication.translate("uTimeFrameSelect", "Date frame", None, QtGui.QApplication.UnicodeUTF8))
        self.rPeriode.setText(QtGui.QApplication.translate("uTimeFrameSelect", "Periode", None, QtGui.QApplication.UnicodeUTF8))
        self.rAll.setText(QtGui.QApplication.translate("uTimeFrameSelect", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.wOk.setText(QtGui.QApplication.translate("uTimeFrameSelect", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.wCancel.setText(QtGui.QApplication.translate("uTimeFrameSelect", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

from dateedit import DateEdit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uTimeFrameSelect = QtGui.QDialog()
    ui = Ui_uTimeFrameSelect()
    ui.setupUi(uTimeFrameSelect)
    uTimeFrameSelect.show()
    sys.exit(app.exec_())

