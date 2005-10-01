# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uClientEditNew.ui'
#
# Created: Thu May 12 00:16:01 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uClientEditNew(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uClientEditNew")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)
        self.setFocusPolicy(QDialog.TabFocus)

        uClientEditNewLayout = QVBoxLayout(self,11,6,"uClientEditNewLayout")

        layout11 = QGridLayout(None,1,1,0,6,"layout11")

        self.clients = QComboBox(0,self,"clients")
        self.clients.setEditable(1)

        layout11.addWidget(self.clients,0,1)

        self.TextLabel2 = QLabel(self,"TextLabel2")
        self.TextLabel2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.TextLabel2,2,0)

        layout10 = QHBoxLayout(None,0,6,"layout10")

        self.accPlan = QComboBox(0,self,"accPlan")
        self.accPlan.setEnabled(1)
        self.accPlan.setInsertionPolicy(QComboBox.NoInsertion)
        self.accPlan.setDuplicatesEnabled(0)
        layout10.addWidget(self.accPlan)
        spacer9 = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout10.addItem(spacer9)

        self.textLabel1_2 = QLabel(self,"textLabel1_2")
        layout10.addWidget(self.textLabel1_2)

        self.vatFile = QComboBox(0,self,"vatFile")
        layout10.addWidget(self.vatFile)

        layout11.addLayout(layout10,4,1)

        self.TextLabel14 = QLabel(self,"TextLabel14")
        self.TextLabel14.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.TextLabel14,4,0)

        layout12 = QHBoxLayout(None,0,6,"layout12")

        self.periodes = QComboBox(0,self,"periodes")
        self.periodes.setInsertionPolicy(QComboBox.NoInsertion)
        self.periodes.setDuplicatesEnabled(0)
        layout12.addWidget(self.periodes)
        spacer12 = QSpacerItem(290,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout12.addItem(spacer12)

        layout11.addLayout(layout12,3,1)
        spacer38 = QSpacerItem(20,30,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout11.addItem(spacer38,6,1)

        layout7 = QHBoxLayout(None,0,6,"layout7")

        self.vat = QCheckBox(self,"vat")
        self.vat.setEnabled(1)
        self.vat.setFocusPolicy(QCheckBox.TabFocus)
        self.vat.setTristate(0)
        layout7.addWidget(self.vat)

        self.budget = QCheckBox(self,"budget")
        layout7.addWidget(self.budget)
        spacer14 = QSpacerItem(57,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7.addItem(spacer14)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setEnabled(0)
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout7.addWidget(self.textLabel1)

        self.dimension = QComboBox(0,self,"dimension")
        self.dimension.setEnabled(0)
        self.dimension.setSizeLimit(6)
        self.dimension.setMaxCount(12)
        self.dimension.setInsertionPolicy(QComboBox.NoInsertion)
        self.dimension.setDuplicatesEnabled(0)
        layout7.addWidget(self.dimension)

        layout11.addLayout(layout7,5,1)

        self.TextLabel5 = QLabel(self,"TextLabel5")
        self.TextLabel5.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.TextLabel5,1,0)

        self.TextLabel1 = QLabel(self,"TextLabel1")
        self.TextLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.TextLabel1,0,0)

        layout16 = QHBoxLayout(None,0,6,"layout16")
        spacer17 = QSpacerItem(171,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout16.addItem(spacer17)

        self.pbSave = QPushButton(self,"pbSave")
        layout16.addWidget(self.pbSave)

        self.pbCancel = QPushButton(self,"pbCancel")
        layout16.addWidget(self.pbCancel)

        layout11.addLayout(layout16,7,1)

        layout9 = QHBoxLayout(None,0,6,"layout9")

        self.regNum = QLineEdit(self,"regNum")
        layout9.addWidget(self.regNum)
        spacer26 = QSpacerItem(211,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout9.addItem(spacer26)

        layout11.addLayout(layout9,1,1)

        self.textLabel3_2 = QLabel(self,"textLabel3_2")

        layout11.addWidget(self.textLabel3_2,5,0)

        self.TextLabel12 = QLabel(self,"TextLabel12")
        self.TextLabel12.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.TextLabel12,3,0)

        layout19 = QHBoxLayout(None,0,6,"layout19")

        self.year = QSpinBox(self,"year")
        self.year.setMaxValue(2010)
        self.year.setMinValue(2000)
        self.year.setValue(2003)
        layout19.addWidget(self.year)
        spacer11 = QSpacerItem(66,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout19.addItem(spacer11)

        self.TextLabel4 = QLabel(self,"TextLabel4")
        self.TextLabel4.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout19.addWidget(self.TextLabel4)

        self.firstEntry = QLineEdit(self,"firstEntry")
        layout19.addWidget(self.firstEntry)

        layout11.addLayout(layout19,2,1)
        uClientEditNewLayout.addLayout(layout11)

        self.textLabel3 = QLabel(self,"textLabel3")
        uClientEditNewLayout.addWidget(self.textLabel3)

        self.languageChange()

        self.resize(QSize(541,279).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pbSave,SIGNAL("clicked()"),self.slotSave)
        self.connect(self.pbCancel,SIGNAL("clicked()"),self.slotCancel)
        self.connect(self.clients,SIGNAL("activated(const QString&)"),self.slotClientSelected)

        self.setTabOrder(self.clients,self.regNum)
        self.setTabOrder(self.regNum,self.firstEntry)
        self.setTabOrder(self.firstEntry,self.periodes)
        self.setTabOrder(self.periodes,self.accPlan)
        self.setTabOrder(self.accPlan,self.budget)
        self.setTabOrder(self.budget,self.dimension)
        self.setTabOrder(self.dimension,self.vat)
        self.setTabOrder(self.vat,self.pbSave)
        self.setTabOrder(self.pbSave,self.pbCancel)

        self.TextLabel2.setBuddy(self.year)
        self.TextLabel14.setBuddy(self.accPlan)
        self.TextLabel1.setBuddy(self.clients)
        self.TextLabel4.setBuddy(self.firstEntry)


    def languageChange(self):
        self.setCaption(self.__tr("Edit client"))
        self.TextLabel2.setText(self.__tr("Year"))
        self.textLabel1_2.setText(self.__tr("VAT file"))
        self.TextLabel14.setText(self.__tr("Account plan"))
        self.vat.setText(self.__tr("VAT"))
        self.budget.setText(self.__tr("Budget"))
        self.budget.setAccel(QString.null)
        self.textLabel1.setText(self.__tr("Dimensions"))
        self.TextLabel5.setText(self.__tr("Reg number"))
        self.TextLabel1.setText(self.__tr("Client name"))
        self.pbSave.setText(self.__tr("Save"))
        self.pbSave.setAccel(QString.null)
        self.pbCancel.setText(self.__tr("Cancel"))
        self.pbCancel.setAccel(QString.null)
        self.textLabel3_2.setText(QString.null)
        self.TextLabel12.setText(self.__tr("Periods a year"))
        self.TextLabel4.setText(self.__tr("First journal entry"))
        self.textLabel3.setText(QString.null)


    def slotSave(self):
        print "uClientEditNew.slotSave(): Not implemented yet"

    def slotCancel(self):
        print "uClientEditNew.slotCancel(): Not implemented yet"

    def slotClientSelected(self,a0):
        print "uClientEditNew.slotClientSelected(const QString&): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("uClientEditNew",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uClientEditNew()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
