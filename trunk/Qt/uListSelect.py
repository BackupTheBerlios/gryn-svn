# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uListSelect.ui'
#
# Created: Fri Feb 11 21:19:59 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from qttable import QTable


class uListSelect(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uListSelect")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uListSelectLayout = QVBoxLayout(self,11,6,"uListSelectLayout")

        self.sTable = QTable(self,"sTable")
        self.sTable.setNumRows(0)
        self.sTable.setNumCols(0)
        self.sTable.setReadOnly(1)
        self.sTable.setSelectionMode(QTable.Single)
        self.sTable.setFocusStyle(QTable.SpreadSheet)
        uListSelectLayout.addWidget(self.sTable)

        layout30 = QHBoxLayout(None,0,6,"layout30")

        self.wAll = QPushButton(self,"wAll")
        self.wAll.setAutoDefault(0)
        self.wAll.setDefault(0)
        layout30.addWidget(self.wAll)

        self.wInvert = QPushButton(self,"wInvert")
        self.wInvert.setAutoDefault(0)
        layout30.addWidget(self.wInvert)
        spacer27 = QSpacerItem(51,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout30.addItem(spacer27)
        uListSelectLayout.addLayout(layout30)

        layout31 = QHBoxLayout(None,0,6,"layout31")
        spacer1 = QSpacerItem(50,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout31.addItem(spacer1)

        self.wOK = QPushButton(self,"wOK")
        self.wOK.setAutoDefault(0)
        layout31.addWidget(self.wOK)

        self.wCancel = QPushButton(self,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout31.addWidget(self.wCancel)
        uListSelectLayout.addLayout(layout31)

        self.languageChange()

        self.resize(QSize(261,579).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)
        self.connect(self.sTable,SIGNAL("currentChanged(int,int)"),self.slotSelectionChanged)
        self.connect(self.sTable,SIGNAL("clicked(int,int,int,const QPoint&)"),self.slotClicked)
        self.connect(self.wOK,SIGNAL("clicked()"),self.slotOk)


    def languageChange(self):
        self.setCaption(self.__tr("Select one"))
        self.wAll.setText(self.__tr("All"))
        self.wInvert.setText(self.__tr("Invert"))
        self.wOK.setText(self.__tr("OK"))
        self.wCancel.setText(self.__tr("Cancel"))


    def slotSelectionChanged(self,a0,a1):
        print "uListSelect.slotSelectionChanged(int,int): Not implemented yet"

    def slotCancel(self):
        print "uListSelect.slotCancel(): Not implemented yet"

    def slotClicked(self,a0,a1,a2,a3):
        print "uListSelect.slotClicked(int,int,int,const QPoint&): Not implemented yet"

    def slotOk(self):
        print "uListSelect.slotOk(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("uListSelect",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uListSelect()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
