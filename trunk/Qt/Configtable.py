""" # $Id$<br>
Generates a configuration parameter dialog of arbitrary number of
label/edit field pairs.
"""
#    This file is a part of the gryn/Qdough accounting program
#    Copyright (C) 2003-2005  Odd  Arild Olsen
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version. 
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#    The top level file LICENSE holds the verbatim copy of this license.


from qt import *

#This class is a dialog with OK and Cancel buttons
#widgets is a compiled string which sets up the label/field pairs

class Configtable(QDialog):


    def __init__(self, dict, enable, parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self)
        if enable != 0:
            self.setCaption(self.__tr("Edit user accessible properties"))
        else:
            self.setCaption(self.__tr("View all properties"))
        if not name:
            self.setName("Configtable")

        widgets= ''
        i= 0
        keys= dict.keys()
        keys.sort()
        for k in keys:
            val= dict[k]
            widgets= widgets + self.AddPar(k, val[1], val[0], i)
            i= i+1
        c= compile(widgets, 'widgets', 'exec')

        self.fields= [] # Stores the fields set up by widgets


        ConfigtableLayout = QVBoxLayout(self,11,6,"ConfigtableLayout")
        
        #The layout can be set to 0 rows, apparently updates when rows added
        layout1 = QGridLayout(None,0,0,0,6,"layout1")

        exec widgets

        ConfigtableLayout.addLayout(layout1)
        spacer1 = QSpacerItem(20,66,QSizePolicy.Minimum,QSizePolicy.Expanding)
        ConfigtableLayout.addItem(spacer1)

        layout2 = QHBoxLayout(None,0,6,"layout2")
        spacer2 = QSpacerItem(101,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer2)

        self.wPbOK = QPushButton(self,"wPbOK")
        layout2.addWidget(self.wPbOK)

        self.wPbCancel = QPushButton(self,"wPbCancel")
        layout2.addWidget(self.wPbCancel)
        ConfigtableLayout.addLayout(layout2)

        self.languageChange()

        for i in self.fields:
            i[1].setEnabled(enable)
        if enable == 0:
            self.wPbCancel.setText(self.__tr('Exit'))
            self.wPbOK.hide()

        self.resize(QSize(411,189).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.wPbOK,SIGNAL("clicked()"),self.slotOK)
        self.connect(self.wPbCancel,SIGNAL("clicked()"),self.slotCancel)


    def languageChange(self):
        self.wPbOK.setText(self.__tr("Save"))
        self.wPbCancel.setText(self.__tr("Cancel"))


    def slotOK(self):
        self.res= {}
        for i in self.fields:
            key= i[0]
            val= str(i[1].text())
            text= str(i[2]) 
            self.res[key]= (val, text)

        self.done(1)

    def getResult(self):
        return self.res

    def slotCancel(self):
        self.res= []
        self.done(0)

    def __tr(self,s,c = None):
        return qApp.translate("Configtable",s,c)


    def AddPar(self, key, text, value, row):
        """ Returns a compilable string which sets up the widgets for one pair
        of label and line edit field.<br>
        'key': a dictionary key for this parameter<br>
        'text': the text that goes into the tool tip of the line  edit<br>
        'value': The initial value, goes into the line edit field<br>
        'row': The row of the grid layout for this field pair. Start at 0.<br>
        """
        """
        Usage example:
        pars is a dictionary with value tuple (text, value)
        keys= pars.keys()
        keys.sort()
        widgets= ''
        i= 0
        for k in keys:
            val= pars[k]
            widgets= widgets + AddPar(k, val[0], val[1], i)
            i= i+1
        c= compile(widgets, 'widgets', 'exec')
        w = Configtable(c)
        """

        row1= str(row+1)
        s1= 'self.wLab%s = QLabel(self,"wLab%s")\n'%(row1, row1) 
        s2= 'self.wLab%s.setText("%s")\n'%(row1, key) 
        s3= 'layout1.addWidget(self.wLab%s,%s,0)\n'%(row1,str(row)) 
        s4= 'self.wEdit%s = QLineEdit(self,"wEdit%s")\n'%(row1, row1)
        s5= 'self.wEdit%s.setText("%s")\n'%(row1, value)
        s6= 'QToolTip.add(self.wEdit%s, "%s")\n'%(row1, text)
        s7= 'layout1.addWidget(self.wEdit%s,%s,1)\n'%(row1, row)
        s8= 'self.fields.append(("%s",self.wEdit%s, "%s"))\n'%(
            key, row1, text) 
        return s1+s2+s3+s4+s5+s6+s7+s8



import sys

if __name__ == "__main__":

    pars= {'p1':('parameter 1 er en veldig presis sak', '123'),
           'p2':('par2', '234')}
    
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Configtable(pars)
    w.setCaption("Setter parametre")
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
    f=w.getResult()
    print "pars: ", pars
    if len(f) > 0:
        print "Resultat:"
        for i in f:
            pars[i[0]]= (pars[i[0]][0], i[1])
        print pars

