# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uQueue.ui'
#
# Created: Fri Feb 11 21:20:00 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from qttable import QTable


class uQueue(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uQueue")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uQueueLayout = QVBoxLayout(self,11,6,"uQueueLayout")

        self.wTable = QTable(self,"wTable")
        self.wTable.setSizePolicy(QSizePolicy(7,7,0,232,self.wTable.sizePolicy().hasHeightForWidth()))
        self.wTable.setNumRows(3)
        self.wTable.setNumCols(3)
        self.wTable.setReadOnly(1)
        self.wTable.setSelectionMode(QTable.NoSelection)
        uQueueLayout.addWidget(self.wTable)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        spacer2 = QSpacerItem(221,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer2)

        self.wOK = QPushButton(self,"wOK")
        self.wOK.setAutoDefault(0)
        layout2.addWidget(self.wOK)
        uQueueLayout.addLayout(layout2)

        self.languageChange()

        self.resize(QSize(600,223).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(QString.null)
        self.wOK.setText(self.__tr("OK"))


    def __tr(self,s,c = None):
        return qApp.translate("uQueue",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uQueue()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
