# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uClientOpen.ui'
#
# Created: Sat Jan  2 00:54:46 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uClientOpen(object):
    def setupUi(self, uClientOpen):
        uClientOpen.setObjectName("uClientOpen")
        uClientOpen.resize(418, 149)
        font = QtGui.QFont()
        font.setFamily("Adobe Helvetica")
        font.setPointSize(12)
        uClientOpen.setFont(font)
        uClientOpen.setFocusPolicy(QtCore.Qt.TabFocus)
        self.gridlayout = QtGui.QGridLayout(uClientOpen)
        self.gridlayout.setObjectName("gridlayout")
        spacerItem = QtGui.QSpacerItem(20, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem, 3, 1, 1, 1)
        self.textLabel5 = QtGui.QLabel(uClientOpen)
        self.textLabel5.setWordWrap(False)
        self.textLabel5.setObjectName("textLabel5")
        self.gridlayout.addWidget(self.textLabel5, 4, 0, 1, 1)
        self.TextLabel1 = QtGui.QLabel(uClientOpen)
        self.TextLabel1.setTextFormat(QtCore.Qt.AutoText)
        self.TextLabel1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.TextLabel1.setWordWrap(False)
        self.TextLabel1.setObjectName("TextLabel1")
        self.gridlayout.addWidget(self.TextLabel1, 0, 0, 1, 1)
        self.clients = QtGui.QComboBox(uClientOpen)
        self.clients.setEditable(False)
        self.clients.setObjectName("clients")
        self.gridlayout.addWidget(self.clients, 0, 1, 1, 1)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem1 = QtGui.QSpacerItem(110, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.pbOpen = QtGui.QPushButton(uClientOpen)
        self.pbOpen.setAutoDefault(False)
        self.pbOpen.setObjectName("pbOpen")
        self.hboxlayout.addWidget(self.pbOpen)
        self.pbCancel = QtGui.QPushButton(uClientOpen)
        self.pbCancel.setAutoDefault(False)
        self.pbCancel.setObjectName("pbCancel")
        self.hboxlayout.addWidget(self.pbCancel)
        self.gridlayout.addLayout(self.hboxlayout, 4, 1, 1, 1)
        self.TextLabel1.setBuddy(self.clients)

        self.retranslateUi(uClientOpen)
        QtCore.QObject.connect(self.pbOpen, QtCore.SIGNAL("clicked()"), uClientOpen.slotOpen)
        QtCore.QObject.connect(self.pbCancel, QtCore.SIGNAL("clicked()"), uClientOpen.slotCancel)
        QtCore.QMetaObject.connectSlotsByName(uClientOpen)
        uClientOpen.setTabOrder(self.clients, self.pbOpen)
        uClientOpen.setTabOrder(self.pbOpen, self.pbCancel)

    def retranslateUi(self, uClientOpen):
        uClientOpen.setWindowTitle(QtGui.QApplication.translate("uClientOpen", "Open client", None, QtGui.QApplication.UnicodeUTF8))
        self.TextLabel1.setText(QtGui.QApplication.translate("uClientOpen", "Client name", None, QtGui.QApplication.UnicodeUTF8))
        self.pbOpen.setText(QtGui.QApplication.translate("uClientOpen", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.pbCancel.setText(QtGui.QApplication.translate("uClientOpen", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uClientOpen = QtGui.QDialog()
    ui = Ui_uClientOpen()
    ui.setupUi(uClientOpen)
    uClientOpen.show()
    sys.exit(app.exec_())

