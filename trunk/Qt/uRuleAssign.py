# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uRuleAssign.ui'
#
# Created: Fri Feb 11 21:20:00 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from qttable import QTable


class uRuleAssign(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uRuleAssign")

        self.setSizePolicy(QSizePolicy(5,7,0,0,self.sizePolicy().hasHeightForWidth()))
        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uRuleAssignLayout = QVBoxLayout(self,11,6,"uRuleAssignLayout")

        self.textLabel6 = QLabel(self,"textLabel6")
        textLabel6_font = QFont(self.textLabel6.font())
        self.textLabel6.setFont(textLabel6_font)
        uRuleAssignLayout.addWidget(self.textLabel6)

        self.wTable = QTable(self,"wTable")
        self.wTable.setSizePolicy(QSizePolicy(7,0,0,0,self.wTable.sizePolicy().hasHeightForWidth()))
        wTable_font = QFont(self.wTable.font())
        self.wTable.setFont(wTable_font)
        self.wTable.setVScrollBarMode(QTable.AlwaysOff)
        self.wTable.setHScrollBarMode(QTable.AlwaysOff)
        self.wTable.setNumRows(5)
        self.wTable.setNumCols(1)
        self.wTable.setSelectionMode(QTable.NoSelection)
        uRuleAssignLayout.addWidget(self.wTable)
        spacer14 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        uRuleAssignLayout.addItem(spacer14)

        layout19 = QHBoxLayout(None,0,6,"layout19")
        spacer13 = QSpacerItem(31,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout19.addItem(spacer13)

        self.wOK = QPushButton(self,"wOK")
        self.wOK.setAutoDefault(0)
        self.wOK.setDefault(0)
        layout19.addWidget(self.wOK)

        self.wCancel = QPushButton(self,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout19.addWidget(self.wCancel)
        uRuleAssignLayout.addLayout(layout19)

        self.languageChange()

        self.resize(QSize(202,215).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(QString.null)
        self.textLabel6.setText(self.__tr("Assign values"))
        self.wOK.setText(self.__tr("OK"))
        self.wCancel.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("uRuleAssign",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uRuleAssign()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
