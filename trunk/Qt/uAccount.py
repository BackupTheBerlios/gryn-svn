# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uAccount.ui'
#
# Created: Fri Feb 11 21:19:59 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uAccount(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uAccount")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)


        LayoutWidget = QWidget(self,"layout17")
        LayoutWidget.setGeometry(QRect(13,15,495,188))
        layout17 = QVBoxLayout(LayoutWidget,11,6,"layout17")

        layout15 = QGridLayout(None,1,1,0,6,"layout15")

        self.wBudgetLabel = QLabel(LayoutWidget,"wBudgetLabel")
        self.wBudgetLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout15.addWidget(self.wBudgetLabel,3,0)

        layout14 = QHBoxLayout(None,0,6,"layout14")

        self.wAccName = QLineEdit(LayoutWidget,"wAccName")
        layout14.addWidget(self.wAccName)

        self.wLineMode = QLabel(LayoutWidget,"wLineMode")
        self.wLineMode.setEnabled(1)
        self.wLineMode.setMaximumSize(QSize(16,16))
        self.wLineMode.setScaledContents(0)
        layout14.addWidget(self.wLineMode)

        layout15.addLayout(layout14,1,1)

        layout37 = QHBoxLayout(None,0,6,"layout37")

        self.wBudget = QLineEdit(LayoutWidget,"wBudget")
        self.wBudget.setMinimumSize(QSize(50,0))
        layout37.addWidget(self.wBudget)
        spacer56 = QSpacerItem(280,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout37.addItem(spacer56)

        layout15.addLayout(layout37,3,1)

        self.textLabel1 = QLabel(LayoutWidget,"textLabel1")
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout15.addWidget(self.textLabel1,0,0)

        self.wVatLabel = QLabel(LayoutWidget,"wVatLabel")
        self.wVatLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout15.addWidget(self.wVatLabel,2,0)

        self.textLabel1_2 = QLabel(LayoutWidget,"textLabel1_2")
        self.textLabel1_2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout15.addWidget(self.textLabel1_2,1,0)

        layout11 = QHBoxLayout(None,0,6,"layout11")

        self.wVat = QComboBox(0,LayoutWidget,"wVat")
        layout11.addWidget(self.wVat)
        spacer18 = QSpacerItem(211,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout11.addItem(spacer18)

        layout15.addLayout(layout11,2,1)

        layout10 = QHBoxLayout(None,0,6,"layout10")

        self.wAccNum = QLineEdit(LayoutWidget,"wAccNum")
        self.wAccNum.setMinimumSize(QSize(50,0))
        layout10.addWidget(self.wAccNum)
        spacer17 = QSpacerItem(280,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout10.addItem(spacer17)

        layout15.addLayout(layout10,0,1)
        layout17.addLayout(layout15)
        spacer20 = QSpacerItem(20,30,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout17.addItem(spacer20)

        layout9 = QHBoxLayout(None,0,6,"layout9")
        spacer19 = QSpacerItem(91,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout9.addItem(spacer19)

        self.wSave = QPushButton(LayoutWidget,"wSave")
        self.wSave.setAutoDefault(0)
        layout9.addWidget(self.wSave)

        self.wNew = QPushButton(LayoutWidget,"wNew")
        self.wNew.setAutoDefault(0)
        layout9.addWidget(self.wNew)

        self.wCancel = QPushButton(LayoutWidget,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout9.addWidget(self.wCancel)
        layout17.addLayout(layout9)

        self.languageChange()

        self.resize(QSize(512,228).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Account"))
        self.wBudgetLabel.setText(self.__tr("Budget"))
        self.textLabel1.setText(self.__tr("Account number"))
        self.wVatLabel.setText(self.__tr("Default VAT"))
        self.textLabel1_2.setText(self.__tr("Account name"))
        self.wSave.setText(self.__tr("Save"))
        self.wNew.setText(self.__tr("New"))
        self.wCancel.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("uAccount",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uAccount()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
