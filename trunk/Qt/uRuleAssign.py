# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uRuleAssign.ui'
#
# Created: Sat Jan  2 00:55:13 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uRuleAssign(object):
    def setupUi(self, uRuleAssign):
        uRuleAssign.setObjectName("uRuleAssign")
        uRuleAssign.resize(327, 368)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(uRuleAssign.sizePolicy().hasHeightForWidth())
        uRuleAssign.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Adobe Helvetica")
        font.setPointSize(12)
        uRuleAssign.setFont(font)
        self.vboxlayout = QtGui.QVBoxLayout(uRuleAssign)
        self.vboxlayout.setObjectName("vboxlayout")
        self.textLabel6 = QtGui.QLabel(uRuleAssign)
        font = QtGui.QFont()
        font.setFamily("Adobe Helvetica")
        font.setPointSize(12)
        self.textLabel6.setFont(font)
        self.textLabel6.setWordWrap(False)
        self.textLabel6.setObjectName("textLabel6")
        self.vboxlayout.addWidget(self.textLabel6)
        self.wTable = QtGui.QTableWidget(uRuleAssign)
        self.wTable.setObjectName("wTable")
        self.wTable.setColumnCount(0)
        self.wTable.setRowCount(0)
        self.vboxlayout.addWidget(self.wTable)
        spacerItem = QtGui.QSpacerItem(20, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vboxlayout.addItem(spacerItem)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem1 = QtGui.QSpacerItem(31, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.wOK = QtGui.QPushButton(uRuleAssign)
        self.wOK.setAutoDefault(False)
        self.wOK.setDefault(False)
        self.wOK.setObjectName("wOK")
        self.hboxlayout.addWidget(self.wOK)
        self.wCancel = QtGui.QPushButton(uRuleAssign)
        self.wCancel.setAutoDefault(False)
        self.wCancel.setObjectName("wCancel")
        self.hboxlayout.addWidget(self.wCancel)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(uRuleAssign)
        QtCore.QMetaObject.connectSlotsByName(uRuleAssign)

    def retranslateUi(self, uRuleAssign):
        self.textLabel6.setText(QtGui.QApplication.translate("uRuleAssign", "Assign values", None, QtGui.QApplication.UnicodeUTF8))
        self.wOK.setText(QtGui.QApplication.translate("uRuleAssign", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.wCancel.setText(QtGui.QApplication.translate("uRuleAssign", "Cancel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uRuleAssign = QtGui.QDialog()
    ui = Ui_uRuleAssign()
    ui.setupUi(uRuleAssign)
    uRuleAssign.show()
    sys.exit(app.exec_())

