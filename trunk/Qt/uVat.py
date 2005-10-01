# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uVat.ui'
#
# Created: Tue May 10 23:00:56 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from qttable import QTable


class uVat(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uVat")


        uVatLayout = QVBoxLayout(self,11,6,"uVatLayout")

        self.wTable = QTable(self,"wTable")
        self.wTable.setSizePolicy(QSizePolicy(7,7,0,0,self.wTable.sizePolicy().hasHeightForWidth()))
        self.wTable.setNumRows(10)
        self.wTable.setNumCols(4)
        uVatLayout.addWidget(self.wTable)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        spacer1 = QSpacerItem(100,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer1)

        self.wSave = QPushButton(self,"wSave")
        self.wSave.setDefault(0)
        layout2.addWidget(self.wSave)

        self.wCancel = QPushButton(self,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout2.addWidget(self.wCancel)
        uVatLayout.addLayout(layout2)

        self.languageChange()

        self.resize(QSize(458,282).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("uVat"))
        self.wSave.setText(self.__tr("Save"))
        self.wCancel.setText(self.__tr("Cancel"))


    def saveSlot(self):
        print "uVat.saveSlot(): Not implemented yet"

    def cancelSlot(self):
        print "uVat.cancelSlot(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("uVat",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uVat()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
