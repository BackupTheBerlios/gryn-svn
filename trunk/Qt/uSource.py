# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uSource.ui'
#
# Created: Sun Mar 13 20:40:01 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from qttable import QTable
from SplitTable import SplitTable


class uSource(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uSource")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uSourceLayout = QVBoxLayout(self,11,6,"uSourceLayout")

        layout10 = QGridLayout(None,1,1,0,6,"layout10")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout10.addWidget(self.textLabel1,4,0)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout10.addWidget(self.textLabel3,0,0)

        layout18 = QHBoxLayout(None,0,6,"layout18")

        self.wDate = QDateEdit(self,"wDate")
        self.wDate.setMinimumSize(QSize(90,0))
        self.wDate.setDate(QDate(2000,1,1))
        self.wDate.setAutoAdvance(1)
        self.wDate.setMaxValue(QDate(2000,12,31))
        self.wDate.setMinValue(QDate(1920,1,1))
        layout18.addWidget(self.wDate)
        spacer19 = QSpacerItem(180,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout18.addItem(spacer19)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout18.addWidget(self.textLabel2)

        self.wNum = QLabel(self,"wNum")
        self.wNum.setSizePolicy(QSizePolicy(0,5,0,0,self.wNum.sizePolicy().hasHeightForWidth()))
        self.wNum.setMinimumSize(QSize(100,0))
        self.wNum.setFrameShape(QLabel.StyledPanel)
        self.wNum.setFrameShadow(QLabel.Sunken)
        layout18.addWidget(self.wNum)

        layout10.addLayout(layout18,0,1)

        self.wCuvenLabel = QLabel(self,"wCuvenLabel")
        self.wCuvenLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout10.addWidget(self.wCuvenLabel,1,0)

        layout7 = QHBoxLayout(None,0,6,"layout7")

        self.wRule = QComboBox(0,self,"wRule")
        self.wRule.setSizePolicy(QSizePolicy(1,0,232,0,self.wRule.sizePolicy().hasHeightForWidth()))
        self.wRule.setMinimumSize(QSize(270,0))
        layout7.addWidget(self.wRule)

        layout10.addLayout(layout7,3,1)

        layout9 = QHBoxLayout(None,0,6,"layout9")

        self.wLotTable = QTable(self,"wLotTable")
        self.wLotTable.setEnabled(0)
        self.wLotTable.setMaximumSize(QSize(32767,55))
        self.wLotTable.setResizePolicy(QTable.Manual)
        self.wLotTable.setHScrollBarMode(QTable.AlwaysOff)
        self.wLotTable.setNumRows(3)
        self.wLotTable.setNumCols(5)
        self.wLotTable.setReadOnly(1)
        self.wLotTable.setSelectionMode(QTable.Single)
        layout9.addWidget(self.wLotTable)

        layout10.addLayout(layout9,4,1)

        self.textLabel17 = QLabel(self,"textLabel17")
        self.textLabel17.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout10.addWidget(self.textLabel17,3,0)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout10.addWidget(self.textLabel4,2,0)

        self.wCuven = QLineEdit(self,"wCuven")

        layout10.addWidget(self.wCuven,1,1)

        layout8 = QHBoxLayout(None,0,6,"layout8")

        self.wCaption = QLineEdit(self,"wCaption")
        self.wCaption.setSizePolicy(QSizePolicy(7,0,100,0,self.wCaption.sizePolicy().hasHeightForWidth()))
        layout8.addWidget(self.wCaption)

        self.wAutoCapt = QCheckBox(self,"wAutoCapt")
        self.wAutoCapt.setEnabled(0)
        layout8.addWidget(self.wAutoCapt)

        layout10.addLayout(layout8,2,1)
        uSourceLayout.addLayout(layout10)

        layout31 = QHBoxLayout(None,0,6,"layout31")
        spacer18_2 = QSpacerItem(220,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout31.addItem(spacer18_2)

        self.wVatCombo = QComboBox(0,self,"wVatCombo")
        self.wVatCombo.setDuplicatesEnabled(0)
        layout31.addWidget(self.wVatCombo)

        self.wNetGrossGr = QButtonGroup(self,"wNetGrossGr")
        self.wNetGrossGr.setMinimumSize(QSize(0,50))
        self.wNetGrossGr.setFrameShape(QButtonGroup.NoFrame)

        self.wNet = QRadioButton(self.wNetGrossGr,"wNet")
        self.wNet.setGeometry(QRect(10,10,80,30))
        self.wNet.setSizePolicy(QSizePolicy(3,0,0,0,self.wNet.sizePolicy().hasHeightForWidth()))
        self.wNet.setChecked(1)

        self.wGross = QRadioButton(self.wNetGrossGr,"wGross")
        self.wGross.setGeometry(QRect(100,10,60,30))
        self.wGross.setSizePolicy(QSizePolicy(3,0,0,0,self.wGross.sizePolicy().hasHeightForWidth()))
        layout31.addWidget(self.wNetGrossGr)
        uSourceLayout.addLayout(layout31)

        self.wTable = SplitTable(self,"wTable")
        self.wTable.setMinimumSize(QSize(100,150))
        uSourceLayout.addWidget(self.wTable)

        layout23 = QHBoxLayout(None,0,6,"layout23")

        self.wClear = QPushButton(self,"wClear")
        self.wClear.setAutoDefault(0)
        layout23.addWidget(self.wClear)
        spacer22 = QSpacerItem(100,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout23.addItem(spacer22)

        self.wResc = QPushButton(self,"wResc")
        self.wResc.setAutoDefault(0)
        layout23.addWidget(self.wResc)

        self.wRound = QPushButton(self,"wRound")
        self.wRound.setAutoDefault(0)
        layout23.addWidget(self.wRound)

        self.wBalance = QLabel(self,"wBalance")
        self.wBalance.setSizePolicy(QSizePolicy(0,5,0,0,self.wBalance.sizePolicy().hasHeightForWidth()))
        self.wBalance.setMinimumSize(QSize(200,0))
        self.wBalance.setMaximumSize(QSize(200,32767))
        self.wBalance.setFrameShape(QLabel.StyledPanel)
        self.wBalance.setFrameShadow(QLabel.Sunken)
        layout23.addWidget(self.wBalance)
        uSourceLayout.addLayout(layout23)
        spacer18 = QSpacerItem(20,20,QSizePolicy.Minimum,QSizePolicy.Fixed)
        uSourceLayout.addItem(spacer18)

        layout7_2 = QHBoxLayout(None,0,6,"layout7_2")

        self.wPrev = QPushButton(self,"wPrev")
        self.wPrev.setAutoDefault(0)
        layout7_2.addWidget(self.wPrev)

        self.wNext = QPushButton(self,"wNext")
        self.wNext.setAutoDefault(0)
        layout7_2.addWidget(self.wNext)
        spacer23 = QSpacerItem(90,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7_2.addItem(spacer23)

        self.wSave = QPushButton(self,"wSave")
        self.wSave.setAutoDefault(0)
        layout7_2.addWidget(self.wSave)
        spacer24 = QSpacerItem(90,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7_2.addItem(spacer24)

        self.wExit = QPushButton(self,"wExit")
        self.wExit.setAutoDefault(0)
        layout7_2.addWidget(self.wExit)

        self.wCancel = QPushButton(self,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout7_2.addWidget(self.wCancel)
        uSourceLayout.addLayout(layout7_2)

        self.languageChange()

        self.resize(QSize(596,506).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.wDate,self.wCuven)
        self.setTabOrder(self.wCuven,self.wCaption)
        self.setTabOrder(self.wCaption,self.wRule)
        self.setTabOrder(self.wRule,self.wLotTable)
        self.setTabOrder(self.wLotTable,self.wRound)
        self.setTabOrder(self.wRound,self.wSave)
        self.setTabOrder(self.wSave,self.wAutoCapt)
        self.setTabOrder(self.wAutoCapt,self.wVatCombo)
        self.setTabOrder(self.wVatCombo,self.wNet)
        self.setTabOrder(self.wNet,self.wGross)
        self.setTabOrder(self.wGross,self.wClear)
        self.setTabOrder(self.wClear,self.wResc)
        self.setTabOrder(self.wResc,self.wPrev)
        self.setTabOrder(self.wPrev,self.wNext)
        self.setTabOrder(self.wNext,self.wExit)
        self.setTabOrder(self.wExit,self.wCancel)


    def languageChange(self):
        self.setCaption(self.__tr("Source"))
        self.textLabel1.setText(self.__tr("Lot"))
        self.textLabel3.setText(self.__tr("Date"))
        self.textLabel2.setText(self.__tr("Ref number"))
        self.wNum.setText(QString.null)
        self.wCuvenLabel.setText(self.__tr("Customer/Vendor"))
        self.textLabel17.setText(self.__tr("Rule"))
        self.textLabel4.setText(self.__tr("Caption"))
        self.wAutoCapt.setText(self.__tr("Auto"))
        self.wNetGrossGr.setTitle(QString.null)
        self.wNet.setText(self.__tr("Net"))
        self.wGross.setText(self.__tr("Gross"))
        self.wClear.setText(self.__tr("Clear"))
        self.wResc.setText(self.__tr("Rescontro"))
        self.wRound.setText(self.__tr("Round"))
        self.wBalance.setText(QString.null)
        self.wPrev.setText(self.__tr("Prev"))
        self.wNext.setText(self.__tr("Next"))
        self.wSave.setText(self.__tr("Save"))
        self.wExit.setText(self.__tr("Exit"))
        self.wCancel.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("uSource",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uSource()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
