# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uCuvenSelect.ui'
#
# Created: Fri Feb 11 21:20:00 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uCuvenSelect(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uCuvenSelect")

        f = QFont(self.font())
        f.setFamily("Nimbus Sans l")
        f.setPointSize(12)
        self.setFont(f)

        uCuvenSelectLayout = QVBoxLayout(self,11,6,"uCuvenSelectLayout")

        self.wGroupSelection = QButtonGroup(self,"wGroupSelection")
        self.wGroupSelection.setColumnLayout(0,Qt.Vertical)
        self.wGroupSelection.layout().setSpacing(6)
        self.wGroupSelection.layout().setMargin(11)
        wGroupSelectionLayout = QHBoxLayout(self.wGroupSelection.layout())
        wGroupSelectionLayout.setAlignment(Qt.AlignTop)

        layout6 = QVBoxLayout(None,0,6,"layout6")

        self.wCust = QRadioButton(self.wGroupSelection,"wCust")
        self.wCust.setChecked(1)
        layout6.addWidget(self.wCust)

        self.wVend = QRadioButton(self.wGroupSelection,"wVend")
        layout6.addWidget(self.wVend)

        self.wActive = QCheckBox(self.wGroupSelection,"wActive")
        self.wActive.setChecked(1)
        layout6.addWidget(self.wActive)

        self.wOpenOnly = QCheckBox(self.wGroupSelection,"wOpenOnly")
        layout6.addWidget(self.wOpenOnly)
        wGroupSelectionLayout.addLayout(layout6)
        uCuvenSelectLayout.addWidget(self.wGroupSelection)

        self.wGroupDetails = QButtonGroup(self,"wGroupDetails")
        self.wGroupDetails.setColumnLayout(0,Qt.Vertical)
        self.wGroupDetails.layout().setSpacing(6)
        self.wGroupDetails.layout().setMargin(11)
        wGroupDetailsLayout = QHBoxLayout(self.wGroupDetails.layout())
        wGroupDetailsLayout.setAlignment(Qt.AlignTop)

        layout2 = QVBoxLayout(None,0,6,"layout2")

        self.wDetSum = QRadioButton(self.wGroupDetails,"wDetSum")
        self.wDetSum.setChecked(1)
        layout2.addWidget(self.wDetSum)

        self.wDetOpen = QRadioButton(self.wGroupDetails,"wDetOpen")
        layout2.addWidget(self.wDetOpen)

        self.wDetAll = QRadioButton(self.wGroupDetails,"wDetAll")
        layout2.addWidget(self.wDetAll)
        wGroupDetailsLayout.addLayout(layout2)
        uCuvenSelectLayout.addWidget(self.wGroupDetails)
        spacer2 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        uCuvenSelectLayout.addItem(spacer2)

        layout4 = QHBoxLayout(None,0,6,"layout4")
        spacer1 = QSpacerItem(50,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout4.addItem(spacer1)

        self.wCancel = QPushButton(self,"wCancel")
        self.wCancel.setAutoDefault(0)
        layout4.addWidget(self.wCancel)

        self.wPick = QPushButton(self,"wPick")
        self.wPick.setAutoDefault(0)
        layout4.addWidget(self.wPick)

        self.wOK = QPushButton(self,"wOK")
        self.wOK.setAutoDefault(0)
        layout4.addWidget(self.wOK)
        uCuvenSelectLayout.addLayout(layout4)

        self.languageChange()

        self.resize(QSize(363,382).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Select customers/vendors"))
        self.wGroupSelection.setTitle(self.__tr("Selection"))
        self.wCust.setText(self.__tr("Customers"))
        self.wVend.setText(self.__tr("Vendors"))
        self.wActive.setText(self.__tr("Only active"))
        self.wOpenOnly.setText(self.__tr("Only with open lots"))
        self.wGroupDetails.setTitle(self.__tr("Details"))
        self.wDetSum.setText(self.__tr("Summary"))
        self.wDetOpen.setText(self.__tr("Transactions of open lots only"))
        self.wDetAll.setText(self.__tr("All transactions"))
        self.wCancel.setText(self.__tr("Cancel"))
        self.wPick.setText(self.__tr("Pick from list"))
        self.wOK.setText(self.__tr("OK"))


    def slotCancel(self):
        print "uCuvenSelect.slotCancel(): Not implemented yet"

    def slotOK(self):
        print "uCuvenSelect.slotOK(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("uCuvenSelect",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uCuvenSelect()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
