# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uSourceFind.ui'
#
# Created: Fri Feb 11 21:19:59 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uSourceFind(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uSourceFind")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uSourceFindLayout = QVBoxLayout(self,11,6,"uSourceFindLayout")

        layout2 = QGridLayout(None,1,1,0,6,"layout2")

        self.wAccountFrom = QLineEdit(self,"wAccountFrom")

        layout2.addWidget(self.wAccountFrom,4,1)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")
        self.textLabel1_2.setAlignment(QLabel.AlignCenter)

        layout2.addWidget(self.textLabel1_2,0,2)

        self.wDateTo = QDateEdit(self,"wDateTo")

        layout2.addWidget(self.wDateTo,2,2)

        self.textLabel2 = QLabel(self,"textLabel2")

        layout2.addWidget(self.textLabel2,0,0)

        self.wFindAmount = QCheckBox(self,"wFindAmount")

        layout2.addWidget(self.wFindAmount,3,0)

        self.wDateFrom = QDateEdit(self,"wDateFrom")

        layout2.addWidget(self.wDateFrom,2,1)

        self.wNumTo = QLineEdit(self,"wNumTo")

        layout2.addWidget(self.wNumTo,1,2)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setAlignment(QLabel.AlignCenter)

        layout2.addWidget(self.textLabel1,0,1)

        self.wAccountTo = QLineEdit(self,"wAccountTo")

        layout2.addWidget(self.wAccountTo,4,2)

        self.wAmountFrom = QLineEdit(self,"wAmountFrom")

        layout2.addWidget(self.wAmountFrom,3,1)

        self.wNumFrom = QLineEdit(self,"wNumFrom")

        layout2.addWidget(self.wNumFrom,1,1)

        self.wFindDate = QCheckBox(self,"wFindDate")

        layout2.addWidget(self.wFindDate,2,0)

        self.wFindAccount = QCheckBox(self,"wFindAccount")

        layout2.addWidget(self.wFindAccount,4,0)

        self.wAmountTo = QLineEdit(self,"wAmountTo")

        layout2.addWidget(self.wAmountTo,3,2)

        self.wFindNumber = QCheckBox(self,"wFindNumber")

        layout2.addWidget(self.wFindNumber,1,0)
        uSourceFindLayout.addLayout(layout2)
        spacer5 = QSpacerItem(20,31,QSizePolicy.Minimum,QSizePolicy.Expanding)
        uSourceFindLayout.addItem(spacer5)

        layout3 = QHBoxLayout(None,0,6,"layout3")
        spacer4 = QSpacerItem(201,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout3.addItem(spacer4)

        self.wSearch = QPushButton(self,"wSearch")
        self.wSearch.setAutoDefault(0)
        layout3.addWidget(self.wSearch)

        self.wCancel = QPushButton(self,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout3.addWidget(self.wCancel)
        uSourceFindLayout.addLayout(layout3)

        self.languageChange()

        self.resize(QSize(311,210).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.wFindNumber,self.wNumFrom)
        self.setTabOrder(self.wNumFrom,self.wNumTo)
        self.setTabOrder(self.wNumTo,self.wFindDate)
        self.setTabOrder(self.wFindDate,self.wDateFrom)
        self.setTabOrder(self.wDateFrom,self.wDateTo)
        self.setTabOrder(self.wDateTo,self.wFindAmount)
        self.setTabOrder(self.wFindAmount,self.wAmountFrom)
        self.setTabOrder(self.wAmountFrom,self.wAmountTo)
        self.setTabOrder(self.wAmountTo,self.wFindAccount)
        self.setTabOrder(self.wFindAccount,self.wAccountFrom)
        self.setTabOrder(self.wAccountFrom,self.wAccountTo)
        self.setTabOrder(self.wAccountTo,self.wSearch)
        self.setTabOrder(self.wSearch,self.wCancel)


    def languageChange(self):
        self.setCaption(self.__tr("Find source"))
        self.textLabel1_2.setText(self.__tr("To"))
        self.textLabel2.setText(self.__tr("Search criterium"))
        self.wFindAmount.setText(self.__tr("Amount"))
        self.textLabel1.setText(self.__tr("From"))
        self.wFindDate.setText(self.__tr("Date"))
        self.wFindAccount.setText(self.__tr("Account"))
        self.wFindNumber.setText(self.__tr("Number"))
        self.wSearch.setText(self.__tr("Search"))
        self.wCancel.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("uSourceFind",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uSourceFind()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
