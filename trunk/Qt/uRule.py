# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uRule.ui'
#
# Created: Fri Feb 11 21:20:00 2005
#      by: The PyQt User Interface Compiler (pyuic) 3.13
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from qttable import QTable


class uRule(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("uRule")

        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        uRuleLayout = QVBoxLayout(self,11,6,"uRuleLayout")

        layout9 = QGridLayout(None,1,1,0,6,"layout9")

        self.wTabPost = QTable(self,"wTabPost")
        self.wTabPost.setSizePolicy(QSizePolicy(7,7,100,0,self.wTabPost.sizePolicy().hasHeightForWidth()))
        wTabPost_font = QFont(self.wTabPost.font())
        self.wTabPost.setFont(wTabPost_font)
        self.wTabPost.setNumRows(5)
        self.wTabPost.setNumCols(3)

        layout9.addWidget(self.wTabPost,4,1)

        self.wText = QLineEdit(self,"wText")
        self.wText.setSizePolicy(QSizePolicy(7,0,100,0,self.wText.sizePolicy().hasHeightForWidth()))

        layout9.addWidget(self.wText,1,1)

        self.textLabel5 = QLabel(self,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(5,5,1,0,self.textLabel5.sizePolicy().hasHeightForWidth()))
        self.textLabel5.setAlignment(QLabel.AlignTop | QLabel.AlignLeft)

        layout9.addWidget(self.textLabel5,4,0)

        self.textLabel3 = QLabel(self,"textLabel3")
        self.textLabel3.setSizePolicy(QSizePolicy(5,5,1,0,self.textLabel3.sizePolicy().hasHeightForWidth()))
        self.textLabel3.setAlignment(QLabel.AlignTop | QLabel.AlignLeft)

        layout9.addWidget(self.textLabel3,2,0)

        self.textLabel2 = QLabel(self,"textLabel2")
        self.textLabel2.setSizePolicy(QSizePolicy(5,5,1,0,self.textLabel2.sizePolicy().hasHeightForWidth()))
        self.textLabel2.setAlignment(QLabel.AlignVCenter | QLabel.AlignLeft)

        layout9.addWidget(self.textLabel2,1,0)

        self.textLabel4 = QLabel(self,"textLabel4")
        self.textLabel4.setSizePolicy(QSizePolicy(5,5,1,0,self.textLabel4.sizePolicy().hasHeightForWidth()))
        self.textLabel4.setAlignment(QLabel.AlignTop | QLabel.AlignLeft)

        layout9.addWidget(self.textLabel4,3,0)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(5,5,1,0,self.textLabel1.sizePolicy().hasHeightForWidth()))
        self.textLabel1.setAlignment(QLabel.AlignVCenter | QLabel.AlignLeft)

        layout9.addWidget(self.textLabel1,0,0)

        self.wPrelude = QTextEdit(self,"wPrelude")
        self.wPrelude.setSizePolicy(QSizePolicy(7,7,100,0,self.wPrelude.sizePolicy().hasHeightForWidth()))
        wPrelude_font = QFont(self.wPrelude.font())
        wPrelude_font.setFamily("Adobe Courier")
        self.wPrelude.setFont(wPrelude_font)

        layout9.addWidget(self.wPrelude,3,1)

        self.wPars = QTable(self,"wPars")
        self.wPars.setSizePolicy(QSizePolicy(7,7,100,0,self.wPars.sizePolicy().hasHeightForWidth()))
        wPars_font = QFont(self.wPars.font())
        self.wPars.setFont(wPars_font)
        self.wPars.setNumRows(5)
        self.wPars.setNumCols(2)
        self.wPars.setSelectionMode(QTable.NoSelection)

        layout9.addWidget(self.wPars,2,1)

        self.wName = QLineEdit(self,"wName")
        self.wName.setSizePolicy(QSizePolicy(7,0,100,0,self.wName.sizePolicy().hasHeightForWidth()))

        layout9.addWidget(self.wName,0,1)
        uRuleLayout.addLayout(layout9)
        spacer2 = QSpacerItem(20,33,QSizePolicy.Minimum,QSizePolicy.Expanding)
        uRuleLayout.addItem(spacer2)

        layout8 = QHBoxLayout(None,0,6,"layout8")
        spacer3 = QSpacerItem(81,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout8.addItem(spacer3)

        self.wOK = QPushButton(self,"wOK")
        layout8.addWidget(self.wOK)

        self.wNew = QPushButton(self,"wNew")
        layout8.addWidget(self.wNew)

        self.wExit = QPushButton(self,"wExit")
        layout8.addWidget(self.wExit)
        uRuleLayout.addLayout(layout8)

        self.languageChange()

        self.resize(QSize(432,518).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(QString.null)
        self.textLabel5.setText(self.__tr("Postings"))
        self.textLabel3.setText(self.__tr("Parametres"))
        self.textLabel2.setText(self.__tr("Default text"))
        self.textLabel4.setText(self.__tr("Prelude"))
        self.textLabel1.setText(self.__tr("Rule name"))
        self.wOK.setText(self.__tr("Save"))
        self.wNew.setText(self.__tr("New"))
        self.wExit.setText(self.__tr("Exit"))


    def __tr(self,s,c = None):
        return qApp.translate("uRule",s,c)

if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = uRule()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
