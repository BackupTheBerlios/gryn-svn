# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uClientOpen.ui'
#
# Created: Fri Feb 11 21:19:58 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uClientOpen(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uClientOpen")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)
        self.setFocusPolicy(QDialog.TabFocus)

        uClientOpenLayout = QGridLayout(self,1,1,11,6,"uClientOpenLayout")
        spacer28 = QSpacerItem(20,16,QSizePolicy.Minimum,QSizePolicy.Expanding)
        uClientOpenLayout.addItem(spacer28,3,1)

        self.textLabel5 = QLabel(self,"textLabel5")

        uClientOpenLayout.addWidget(self.textLabel5,4,0)

        self.TextLabel1 = QLabel(self,"TextLabel1")
        self.TextLabel1.setTextFormat(QLabel.AutoText)
        self.TextLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        uClientOpenLayout.addWidget(self.TextLabel1,0,0)

        self.clients = QComboBox(0,self,"clients")
        self.clients.setEditable(0)

        uClientOpenLayout.addWidget(self.clients,0,1)

        layout28 = QHBoxLayout(None,0,6,"layout28")
        spacer17 = QSpacerItem(110,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout28.addItem(spacer17)

        self.pbOpen = QPushButton(self,"pbOpen")
        self.pbOpen.setAutoDefault(0)
        layout28.addWidget(self.pbOpen)

        self.pbCancel = QPushButton(self,"pbCancel")
        self.pbCancel.setAutoDefault(0)
        layout28.addWidget(self.pbCancel)

        uClientOpenLayout.addLayout(layout28,4,1)

        self.languageChange()

        self.resize(QSize(418,149).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.pbOpen,SIGNAL("clicked()"),self.slotOpen)
        self.connect(self.pbCancel,SIGNAL("clicked()"),self.slotCancel)

        self.setTabOrder(self.clients,self.pbOpen)
        self.setTabOrder(self.pbOpen,self.pbCancel)

        self.TextLabel1.setBuddy(self.clients)


    def languageChange(self):
        self.setCaption(self.__tr("Open client"))
        self.textLabel5.setText(QString.null)
        self.TextLabel1.setText(self.__tr("Client name"))
        self.pbOpen.setText(self.__tr("Open"))
        self.pbOpen.setAccel(QString.null)
        self.pbCancel.setText(self.__tr("Cancel"))
        self.pbCancel.setAccel(QString.null)


    def slotCancel(self):
        print "uClientOpen.slotCancel(): Not implemented yet"

    def slotOpen(self):
        print "uClientOpen.slotOpen(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("uClientOpen",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uClientOpen()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
