# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uSourceSelect.ui'
#
# Created: Fri Feb 11 21:20:00 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uSourceSelect(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uSourceSelect")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uSourceSelectLayout = QVBoxLayout(self,11,6,"uSourceSelectLayout")

        self.wGroup = QButtonGroup(self,"wGroup")
        self.wGroup.setColumnLayout(0,Qt.Vertical)
        self.wGroup.layout().setSpacing(6)
        self.wGroup.layout().setMargin(11)
        wGroupLayout = QGridLayout(self.wGroup.layout())
        wGroupLayout.setAlignment(Qt.AlignTop)
        spacer30 = QSpacerItem(101,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        wGroupLayout.addItem(spacer30,4,2)

        self.wSourceFrom = QLineEdit(self.wGroup,"wSourceFrom")

        wGroupLayout.addWidget(self.wSourceFrom,1,1)

        self.wAccountTo = QLineEdit(self.wGroup,"wAccountTo")

        wGroupLayout.addWidget(self.wAccountTo,3,2)

        self.wSourceTo = QLineEdit(self.wGroup,"wSourceTo")

        wGroupLayout.addWidget(self.wSourceTo,1,2)

        self.wbSource = QRadioButton(self.wGroup,"wbSource")

        wGroupLayout.addWidget(self.wbSource,1,0)

        self.wDateFrom = QDateEdit(self.wGroup,"wDateFrom")

        wGroupLayout.addWidget(self.wDateFrom,2,1)

        self.wDateTo = QDateEdit(self.wGroup,"wDateTo")

        wGroupLayout.addWidget(self.wDateTo,2,2)

        self.wAccountFrom = QLineEdit(self.wGroup,"wAccountFrom")

        wGroupLayout.addWidget(self.wAccountFrom,3,1)

        self.wbDate = QRadioButton(self.wGroup,"wbDate")

        wGroupLayout.addWidget(self.wbDate,2,0)

        self.wbAccount = QRadioButton(self.wGroup,"wbAccount")

        wGroupLayout.addWidget(self.wbAccount,3,0)

        self.wbPeriod = QRadioButton(self.wGroup,"wbPeriod")

        wGroupLayout.addWidget(self.wbPeriod,4,0)

        self.wPeriod = QComboBox(0,self.wGroup,"wPeriod")

        wGroupLayout.addWidget(self.wPeriod,4,1)

        self.textLabel1 = QLabel(self.wGroup,"textLabel1")
        self.textLabel1.setAlignment(QLabel.AlignCenter)

        wGroupLayout.addWidget(self.textLabel1,0,1)

        self.textLabel1_2 = QLabel(self.wGroup,"textLabel1_2")
        self.textLabel1_2.setAlignment(QLabel.AlignCenter)

        wGroupLayout.addWidget(self.textLabel1_2,0,2)
        spacer31 = QSpacerItem(41,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        wGroupLayout.addItem(spacer31,0,0)

        self.wbAll = QRadioButton(self.wGroup,"wbAll")

        wGroupLayout.addWidget(self.wbAll,5,0)
        uSourceSelectLayout.addWidget(self.wGroup)

        self.wShowSplits = QCheckBox(self,"wShowSplits")
        self.wShowSplits.setChecked(1)
        uSourceSelectLayout.addWidget(self.wShowSplits)
        spacer33 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        uSourceSelectLayout.addItem(spacer33)

        layout35 = QHBoxLayout(None,0,6,"layout35")
        spacer32 = QSpacerItem(141,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout35.addItem(spacer32)

        self.wOK = QPushButton(self,"wOK")
        self.wOK.setAutoDefault(0)
        layout35.addWidget(self.wOK)

        self.wCancel = QPushButton(self,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout35.addWidget(self.wCancel)
        uSourceSelectLayout.addLayout(layout35)

        self.languageChange()

        self.resize(QSize(350,287).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.wSourceFrom,self.wSourceTo)
        self.setTabOrder(self.wSourceTo,self.wDateFrom)
        self.setTabOrder(self.wDateFrom,self.wDateTo)
        self.setTabOrder(self.wDateTo,self.wAccountFrom)
        self.setTabOrder(self.wAccountFrom,self.wAccountTo)
        self.setTabOrder(self.wAccountTo,self.wOK)
        self.setTabOrder(self.wOK,self.wCancel)


    def languageChange(self):
        self.setCaption(self.__tr("Select source"))
        self.wGroup.setTitle(self.__tr("Selection criterium"))
        self.wbSource.setText(self.__tr("Source"))
        self.wbDate.setText(self.__tr("Date"))
        self.wbAccount.setText(self.__tr("Account"))
        self.wbPeriod.setText(self.__tr("Period"))
        self.textLabel1.setText(self.__tr("From"))
        self.textLabel1_2.setText(self.__tr("To"))
        self.wbAll.setText(self.__tr("All"))
        self.wShowSplits.setText(self.__tr("Show splits"))
        self.wOK.setText(self.__tr("OK"))
        self.wCancel.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("uSourceSelect",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uSourceSelect()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
