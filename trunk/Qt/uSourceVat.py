# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uSourceVat.ui'
#
# Created: Fri Feb 11 21:20:00 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uSourceVat(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uSourceVat")


        uSourceVatLayout = QVBoxLayout(self,11,6,"uSourceVatLayout")

        layout1 = QHBoxLayout(None,0,6,"layout1")

        self.textLabel1 = QLabel(self,"textLabel1")
        layout1.addWidget(self.textLabel1)

        self.wPeriod = QComboBox(0,self,"wPeriod")
        layout1.addWidget(self.wPeriod)
        uSourceVatLayout.addLayout(layout1)
        spacer3 = QSpacerItem(20,31,QSizePolicy.Minimum,QSizePolicy.Expanding)
        uSourceVatLayout.addItem(spacer3)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        spacer1 = QSpacerItem(41,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer1)

        self.wCancel = QPushButton(self,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout2.addWidget(self.wCancel)

        self.wOK = QPushButton(self,"wOK")
        layout2.addWidget(self.wOK)
        uSourceVatLayout.addLayout(layout2)

        self.languageChange()

        self.resize(QSize(287,144).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("VAT transfer"))
        self.textLabel1.setText(self.__tr("Period to transfer"))
        self.wCancel.setText(self.__tr("Cancel"))
        self.wOK.setText(self.__tr("OK"))


    def __tr(self,s,c = None):
        return qApp.translate("uSourceVat",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uSourceVat()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
