# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uTreeList.ui'
#
# Created: Fri Feb 11 21:19:58 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uTreeList(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uTreeList")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uTreeListLayout = QVBoxLayout(self,11,6,"uTreeListLayout")

        self.accountList = QListView(self,"accountList")
        self.accountList.addColumn(self.__tr("Column 1"))
        self.accountList.setSizePolicy(QSizePolicy(7,7,0,232,self.accountList.sizePolicy().hasHeightForWidth()))
        self.accountList.setLineWidth(1)
        self.accountList.setMargin(0)
        self.accountList.setMidLineWidth(1)
        uTreeListLayout.addWidget(self.accountList)

        self.showHow = QCheckBox(self,"showHow")
        uTreeListLayout.addWidget(self.showHow)

        self.languageChange()

        self.resize(QSize(262,538).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(QString.null)
        self.accountList.header().setLabel(0,self.__tr("Column 1"))
        self.accountList.clear()
        item = QListViewItem(self.accountList,None)
        item.setText(0,self.__tr("New Item"))

        self.showHow.setText(QString.null)


    def __tr(self,s,c = None):
        return qApp.translate("uTreeList",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uTreeList()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
