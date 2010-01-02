# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uCuvenSelect.ui'
#
# Created: Sat Jan  2 00:55:17 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uCuvenSelect(object):
    def setupUi(self, uCuvenSelect):
        uCuvenSelect.setObjectName("uCuvenSelect")
        uCuvenSelect.resize(363, 382)
        font = QtGui.QFont()
        font.setFamily("Nimbus Sans l")
        font.setPointSize(12)
        uCuvenSelect.setFont(font)
        self.vboxlayout = QtGui.QVBoxLayout(uCuvenSelect)
        self.vboxlayout.setObjectName("vboxlayout")
        self.wGroupSelection = QtGui.QGroupBox(uCuvenSelect)
        self.wGroupSelection.setObjectName("wGroupSelection")
        self.hboxlayout = QtGui.QHBoxLayout(self.wGroupSelection)
        self.hboxlayout.setObjectName("hboxlayout")
        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.wCust = QtGui.QRadioButton(self.wGroupSelection)
        self.wCust.setChecked(True)
        self.wCust.setObjectName("wCust")
        self.vboxlayout1.addWidget(self.wCust)
        self.wVend = QtGui.QRadioButton(self.wGroupSelection)
        self.wVend.setObjectName("wVend")
        self.vboxlayout1.addWidget(self.wVend)
        self.wActive = QtGui.QCheckBox(self.wGroupSelection)
        self.wActive.setChecked(True)
        self.wActive.setObjectName("wActive")
        self.vboxlayout1.addWidget(self.wActive)
        self.wOpenOnly = QtGui.QCheckBox(self.wGroupSelection)
        self.wOpenOnly.setObjectName("wOpenOnly")
        self.vboxlayout1.addWidget(self.wOpenOnly)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.vboxlayout.addWidget(self.wGroupSelection)
        self.wGroupDetails = QtGui.QGroupBox(uCuvenSelect)
        self.wGroupDetails.setObjectName("wGroupDetails")
        self.hboxlayout1 = QtGui.QHBoxLayout(self.wGroupDetails)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.wDetSum = QtGui.QRadioButton(self.wGroupDetails)
        self.wDetSum.setChecked(True)
        self.wDetSum.setObjectName("wDetSum")
        self.vboxlayout2.addWidget(self.wDetSum)
        self.wDetOpen = QtGui.QRadioButton(self.wGroupDetails)
        self.wDetOpen.setObjectName("wDetOpen")
        self.vboxlayout2.addWidget(self.wDetOpen)
        self.wDetAll = QtGui.QRadioButton(self.wGroupDetails)
        self.wDetAll.setObjectName("wDetAll")
        self.vboxlayout2.addWidget(self.wDetAll)
        self.hboxlayout1.addLayout(self.vboxlayout2)
        self.vboxlayout.addWidget(self.wGroupDetails)
        spacerItem = QtGui.QSpacerItem(20, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")
        spacerItem1 = QtGui.QSpacerItem(50, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem1)
        self.wCancel = QtGui.QPushButton(uCuvenSelect)
        self.wCancel.setAutoDefault(False)
        self.wCancel.setObjectName("wCancel")
        self.hboxlayout2.addWidget(self.wCancel)
        self.wPick = QtGui.QPushButton(uCuvenSelect)
        self.wPick.setAutoDefault(False)
        self.wPick.setObjectName("wPick")
        self.hboxlayout2.addWidget(self.wPick)
        self.wOK = QtGui.QPushButton(uCuvenSelect)
        self.wOK.setAutoDefault(False)
        self.wOK.setObjectName("wOK")
        self.hboxlayout2.addWidget(self.wOK)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(uCuvenSelect)
        QtCore.QMetaObject.connectSlotsByName(uCuvenSelect)

    def retranslateUi(self, uCuvenSelect):
        uCuvenSelect.setWindowTitle(QtGui.QApplication.translate("uCuvenSelect", "Select customers/vendors", None, QtGui.QApplication.UnicodeUTF8))
        self.wGroupSelection.setTitle(QtGui.QApplication.translate("uCuvenSelect", "Selection", None, QtGui.QApplication.UnicodeUTF8))
        self.wCust.setText(QtGui.QApplication.translate("uCuvenSelect", "Customers", None, QtGui.QApplication.UnicodeUTF8))
        self.wVend.setText(QtGui.QApplication.translate("uCuvenSelect", "Vendors", None, QtGui.QApplication.UnicodeUTF8))
        self.wActive.setText(QtGui.QApplication.translate("uCuvenSelect", "Only active", None, QtGui.QApplication.UnicodeUTF8))
        self.wOpenOnly.setText(QtGui.QApplication.translate("uCuvenSelect", "Only with open lots", None, QtGui.QApplication.UnicodeUTF8))
        self.wGroupDetails.setTitle(QtGui.QApplication.translate("uCuvenSelect", "Details", None, QtGui.QApplication.UnicodeUTF8))
        self.wDetSum.setText(QtGui.QApplication.translate("uCuvenSelect", "Summary", None, QtGui.QApplication.UnicodeUTF8))
        self.wDetOpen.setText(QtGui.QApplication.translate("uCuvenSelect", "Transactions of open lots only", None, QtGui.QApplication.UnicodeUTF8))
        self.wDetAll.setText(QtGui.QApplication.translate("uCuvenSelect", "All transactions", None, QtGui.QApplication.UnicodeUTF8))
        self.wCancel.setText(QtGui.QApplication.translate("uCuvenSelect", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.wPick.setText(QtGui.QApplication.translate("uCuvenSelect", "Pick from list", None, QtGui.QApplication.UnicodeUTF8))
        self.wOK.setText(QtGui.QApplication.translate("uCuvenSelect", "OK", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uCuvenSelect = QtGui.QDialog()
    ui = Ui_uCuvenSelect()
    ui.setupUi(uCuvenSelect)
    uCuvenSelect.show()
    sys.exit(app.exec_())

