# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uCuven.ui'
#
# Created: Fri Feb 11 21:19:59 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uCuven(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uCuven")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uCuvenLayout = QVBoxLayout(self,11,6,"uCuvenLayout")

        layout14 = QGridLayout(None,1,1,0,6,"layout14")

        self.wGroup = QComboBox(0,self,"wGroup")
        self.wGroup.setEnabled(0)
        self.wGroup.setMinimumSize(QSize(300,0))

        layout14.addWidget(self.wGroup,3,1)

        layout13 = QHBoxLayout(None,0,6,"layout13")

        self.wNumber = QLineEdit(self,"wNumber")
        self.wNumber.setEnabled(0)
        self.wNumber.setMinimumSize(QSize(100,0))
        layout13.addWidget(self.wNumber)
        spacer7 = QSpacerItem(151,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout13.addItem(spacer7)

        layout14.addLayout(layout13,0,1)

        self.wRegno = QLineEdit(self,"wRegno")
        self.wRegno.setMinimumSize(QSize(100,0))

        layout14.addWidget(self.wRegno,2,1)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout14.addWidget(self.textLabel3,1,0)

        self.wName = QLineEdit(self,"wName")
        self.wName.setMinimumSize(QSize(300,0))

        layout14.addWidget(self.wName,1,1)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout14.addWidget(self.textLabel4,0,0)

        self.textLabel5 = QLabel(self,"textLabel5")
        self.textLabel5.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout14.addWidget(self.textLabel5,2,0)

        self.textLabel3_2 = QLabel(self,"textLabel3_2")
        self.textLabel3_2.setEnabled(0)
        self.textLabel3_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout14.addWidget(self.textLabel3_2,3,0)
        uCuvenLayout.addLayout(layout14)
        spacer63 = QSpacerItem(20,30,QSizePolicy.Minimum,QSizePolicy.Expanding)
        uCuvenLayout.addItem(spacer63)

        layout11 = QHBoxLayout(None,0,6,"layout11")
        spacer59 = QSpacerItem(68,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(spacer59)

        self.wSave = QPushButton(self,"wSave")
        self.wSave.setAutoDefault(0)
        layout11.addWidget(self.wSave)

        self.wCancel = QPushButton(self,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout11.addWidget(self.wCancel)
        uCuvenLayout.addLayout(layout11)

        self.languageChange()

        self.resize(QSize(429,213).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.wSave,SIGNAL("clicked()"),self.slotSave)
        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)

        self.setTabOrder(self.wName,self.wRegno)
        self.setTabOrder(self.wRegno,self.wSave)
        self.setTabOrder(self.wSave,self.wCancel)
        self.setTabOrder(self.wCancel,self.wGroup)
        self.setTabOrder(self.wGroup,self.wNumber)


    def languageChange(self):
        self.setCaption(self.__tr("Customers and vendors"))
        self.textLabel3.setText(self.__tr("Name"))
        self.textLabel4.setText(self.__tr("Number"))
        self.textLabel5.setText(self.__tr("Reg number"))
        self.textLabel3_2.setText(self.__tr("Group"))
        self.wSave.setText(self.__tr("Save"))
        self.wCancel.setText(self.__tr("Cancel"))


    def slotSave(self):
        print "uCuven.slotSave(): Not implemented yet"

    def slotCancel(self):
        print "uCuven.slotCancel(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("uCuven",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uCuven()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
