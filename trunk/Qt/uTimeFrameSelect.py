# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uTimeFrameSelect.ui'
#
# Created: Fri Feb 11 21:20:00 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uTimeFrameSelect(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uTimeFrameSelect")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uTimeFrameSelectLayout = QVBoxLayout(self,11,6,"uTimeFrameSelectLayout")

        self.wFrame = QButtonGroup(self,"wFrame")
        self.wFrame.setColumnLayout(0,Qt.Vertical)
        self.wFrame.layout().setSpacing(6)
        self.wFrame.layout().setMargin(11)
        wFrameLayout = QVBoxLayout(self.wFrame.layout())
        wFrameLayout.setAlignment(Qt.AlignTop)

        layout2 = QHBoxLayout(None,0,6,"layout2")

        self.rPeriode = QRadioButton(self.wFrame,"rPeriode")
        layout2.addWidget(self.rPeriode)

        self.wPeriode = QComboBox(0,self.wFrame,"wPeriode")
        layout2.addWidget(self.wPeriode)
        wFrameLayout.addLayout(layout2)

        layout3 = QHBoxLayout(None,0,6,"layout3")

        self.rDate = QRadioButton(self.wFrame,"rDate")
        layout3.addWidget(self.rDate)

        self.wDateFrom = QDateEdit(self.wFrame,"wDateFrom")
        layout3.addWidget(self.wDateFrom)

        self.wDateTo = QDateEdit(self.wFrame,"wDateTo")
        wDateTo_font = QFont(self.wDateTo.font())
        self.wDateTo.setFont(wDateTo_font)
        layout3.addWidget(self.wDateTo)
        wFrameLayout.addLayout(layout3)

        self.rAll = QRadioButton(self.wFrame,"rAll")
        wFrameLayout.addWidget(self.rAll)
        uTimeFrameSelectLayout.addWidget(self.wFrame)
        spacer2 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        uTimeFrameSelectLayout.addItem(spacer2)

        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer1 = QSpacerItem(51,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer1)

        self.wOk = QPushButton(self,"wOk")
        layout1.addWidget(self.wOk)

        self.wCancel = QPushButton(self,"wCancel")
        layout1.addWidget(self.wCancel)
        uTimeFrameSelectLayout.addLayout(layout1)

        self.languageChange()

        self.resize(QSize(266,197).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Select ledger entry periode"))
        self.wFrame.setTitle(self.__tr("Date frame"))
        self.rPeriode.setText(self.__tr("Periode"))
        self.rDate.setText(QString.null)
        self.rAll.setText(self.__tr("All"))
        self.wOk.setText(self.__tr("OK"))
        self.wCancel.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("uTimeFrameSelect",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uTimeFrameSelect()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
