# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uAccountImport.ui'
#
# Created: Fri Feb 11 21:19:58 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *


class uAccountImport(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uAccountImport")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        self.setFont(f)


        LayoutWidget = QWidget(self,"layout18")
        LayoutWidget.setGeometry(QRect(11,126,518,29))
        layout18 = QHBoxLayout(LayoutWidget,11,6,"layout18")
        spacer37 = QSpacerItem(281,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout18.addItem(spacer37)

        self.imprt = QPushButton(LayoutWidget,"imprt")
        layout18.addWidget(self.imprt)

        self.cancel = QPushButton(LayoutWidget,"cancel")
        layout18.addWidget(self.cancel)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setGeometry(QRect(12,12,160,27))
        self.textLabel1.setTextFormat(QLabel.PlainText)
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.browse = QPushButton(self,"browse")
        self.browse.setGeometry(QRect(488,12,40,27))

        self.lineEdit10 = QLineEdit(self,"lineEdit10")
        self.lineEdit10.setEnabled(0)
        self.lineEdit10.setGeometry(QRect(180,10,281,31))

        self.languageChange()

        self.resize(QSize(540,166).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.browse,SIGNAL("clicked()"),self.slotBrowse)
        self.connect(self.imprt,SIGNAL("clicked()"),self.slotImport)
        self.connect(self.cancel,SIGNAL("clicked()"),self.slotCancel)


    def languageChange(self):
        self.setCaption(self.__tr("Import account plan"))
        self.imprt.setText(self.__tr("Import"))
        self.cancel.setText(self.__tr("Cancel"))
        self.textLabel1.setText(self.__tr("Read plan from text file"))
        self.browse.setText(self.__tr("..."))


    def slotBrowse(self):
        print "uAccountImport.slotBrowse(): Not implemented yet"

    def slotCancel(self):
        print "uAccountImport.slotCancel(): Not implemented yet"

    def slotImport(self):
        print "uAccountImport.slotImport(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("uAccountImport",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uAccountImport()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
