# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uAccountImport.ui'
#
# Created: Sat Jan  2 00:54:51 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_uAccountImport(object):
    def setupUi(self, uAccountImport):
        uAccountImport.setObjectName("uAccountImport")
        uAccountImport.resize(540, 166)
        font = QtGui.QFont()
        font.setFamily("Adobe Helvetica")
        uAccountImport.setFont(font)
        self.layout18 = QtGui.QWidget(uAccountImport)
        self.layout18.setGeometry(QtCore.QRect(11, 126, 518, 29))
        self.layout18.setObjectName("layout18")
        self.hboxlayout = QtGui.QHBoxLayout(self.layout18)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(281, 21, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.imprt = QtGui.QPushButton(self.layout18)
        self.imprt.setObjectName("imprt")
        self.hboxlayout.addWidget(self.imprt)
        self.cancel = QtGui.QPushButton(self.layout18)
        self.cancel.setObjectName("cancel")
        self.hboxlayout.addWidget(self.cancel)
        self.textLabel1 = QtGui.QLabel(uAccountImport)
        self.textLabel1.setGeometry(QtCore.QRect(12, 12, 160, 27))
        self.textLabel1.setTextFormat(QtCore.Qt.PlainText)
        self.textLabel1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.textLabel1.setWordWrap(False)
        self.textLabel1.setObjectName("textLabel1")
        self.browse = QtGui.QPushButton(uAccountImport)
        self.browse.setGeometry(QtCore.QRect(488, 12, 40, 27))
        self.browse.setObjectName("browse")
        self.lineEdit10 = QtGui.QLineEdit(uAccountImport)
        self.lineEdit10.setEnabled(False)
        self.lineEdit10.setGeometry(QtCore.QRect(180, 10, 281, 31))
        self.lineEdit10.setObjectName("lineEdit10")

        self.retranslateUi(uAccountImport)
        QtCore.QObject.connect(self.browse, QtCore.SIGNAL("clicked()"), uAccountImport.slotBrowse)
        QtCore.QObject.connect(self.imprt, QtCore.SIGNAL("clicked()"), uAccountImport.slotImport)
        QtCore.QObject.connect(self.cancel, QtCore.SIGNAL("clicked()"), uAccountImport.slotCancel)
        QtCore.QMetaObject.connectSlotsByName(uAccountImport)

    def retranslateUi(self, uAccountImport):
        uAccountImport.setWindowTitle(QtGui.QApplication.translate("uAccountImport", "Import account plan", None, QtGui.QApplication.UnicodeUTF8))
        self.imprt.setText(QtGui.QApplication.translate("uAccountImport", "Import", None, QtGui.QApplication.UnicodeUTF8))
        self.cancel.setText(QtGui.QApplication.translate("uAccountImport", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.textLabel1.setText(QtGui.QApplication.translate("uAccountImport", "Read plan from text file", None, QtGui.QApplication.UnicodeUTF8))
        self.browse.setText(QtGui.QApplication.translate("uAccountImport", "...", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    uAccountImport = QtGui.QDialog()
    ui = Ui_uAccountImport()
    ui.setupUi(uAccountImport)
    uAccountImport.show()
    sys.exit(app.exec_())

