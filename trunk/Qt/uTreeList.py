# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uTreeList.ui'
#
# Created: Sat Jan  2 00:54:53 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uTreeList(object):
    def setupUi(self, uTreeList):
        uTreeList.setObjectName("uTreeList")
        uTreeList.resize(262, 538)
        font = QtGui.QFont()
        font.setFamily("Adobe Helvetica")
        font.setPointSize(12)
        uTreeList.setFont(font)
        self.vboxlayout = QtGui.QVBoxLayout(uTreeList)
        self.vboxlayout.setObjectName("vboxlayout")
        self.treeWidget = QtGui.QTreeWidget(uTreeList)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.vboxlayout.addWidget(self.treeWidget)
        self.showHow = QtGui.QCheckBox(uTreeList)
        self.showHow.setObjectName("showHow")
        self.vboxlayout.addWidget(self.showHow)

        self.retranslateUi(uTreeList)
        QtCore.QMetaObject.connectSlotsByName(uTreeList)

    def retranslateUi(self, uTreeList):
        pass


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uTreeList = QtGui.QDialog()
    ui = Ui_uTreeList()
    ui.setupUi(uTreeList)
    uTreeList.show()
    sys.exit(app.exec_())

