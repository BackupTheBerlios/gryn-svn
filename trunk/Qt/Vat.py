# $Id$

# While this works, this dialog should be moved to new client and
# transfer to new year. These are the only occations when a change of
# VAT properties is reasonable. If errors are later detected: edit the
# data base directly (call the consultant)

import sys
import string
from qt import *
from qttable import QTable
import uVat
import Model.Books
import Model.Exceptions

class Vat(uVat.uVat):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        uVat.uVat.__init__(self,parent,name,modal,fl)

        self.setCaption(self.tr("VAT account assignments"))
        self.wTable.setNumCols(4)
        fm= self.fontMetrics() 
        w1= fm.width('0'*10)
        for i in range(1,4): 
            self.wTable.setColumnWidth(i, w1)
        self.wTable.setColumnStretchable(0, 1)

        for i in range(0, 10):
            self.wTable.setRowStretchable(i, 1)

        qh= self.wTable.horizontalHeader()
        qh.setLabel(0, self.tr("Vat name"))
        qh.setLabel(1, self.tr("Rate"))
        qh.setLabel(2, self.tr("Account"))
        qh.setLabel(3, self.tr("Sales acc"))
        vh= self.wTable.verticalHeader()
        for i in range(0,10):
            vh.setLabel(i, str(i))

        self.vatL= Model.Books.getList('vat')
        self.cpL= Model.Vat.VatList()
        for v in self.vatL: self.cpL.append(v.copyOfVat())
        print "cpL: "
        for v in self.cpL:
            print "   ", v

        self.drawTable(self.vatL)
        self.connect(self.wSave,SIGNAL("clicked()"),self.saveSlot)
        self.connect(self.wCancel,SIGNAL("clicked()"),self.cancelSlot)



    def languageChange(self):
        self.wSave.setText(self.tr("Save"))
        self.wCancel.setText(self.tr("Cancel"))


    def saveSlot(self):
        r= self.wTable.currentRow()
        c= self.wTable.currentColumn()
        ed= self.wTable.cellWidget(r, c)
        if ed: # we are editing a cell, capture text
            self.wTable.setText(r, c, ed.text())

        #copy from form and create new obj if not excisting
        for r in range(0, 10):
            v= self.cpL.getByCode("%1d"%r)
            if not v:
                v= Model.Vat.Vat()
                self.cpL.append(v)
                v.vatCode= "%1d"%r
            v.vatName=string.strip(str(self.wTable.text(r, 0)))
            v.vatRate=string.strip(str(self.wTable.text(r, 1)))
            v.vatAccount= string.strip(str(self.wTable.text(r, 2))) 
            v.salesAccount= string.strip(str(self.wTable.text(r, 3)))

        #mark unused objects
        for v in self.cpL:
            if len(v.vatName) < 1:
                v.vatCode= None

        #delete unused objects from list
        sL= self.cpL[:]
        for v in sL:
            if not v.vatCode:
                self.cpL.remove(v)
        #remove unused from vatL
        #BUG:we should allow the delete iff this code is not used in the ledger
        for v in self.vatL:
            if not self.cpL.getByCode(v.vatCode):
                print "Delete vatL: ", v
                self.vatL.deleteEntry(v)
        #update those remaining
        for v in self.cpL:
            c= self.vatL.getByCode(v.vatCode)
            if c:
                v._id= c.id #cheat a little (v.id=  sets the id to None)
            self.vatL.saveEntry(v)
            
        self.done(0)

    def cancelSlot(self):
        self.done(1)


    def drawTable(self, vatL):
        for v in vatL:
            r= int(v.vatCode)
            self.wTable.setText(r, 0, v.vatName)
            if v.vatRate: s= v.vatRate
            else: s= '0'
            self.wTable.setText(r, 1, s)
            
            if v.vatAccount: s= v.vatAccount
            else: s= ''
            self.wTable.setText(r, 2, s)
            
            if v.salesAccount: s= v.salesAccount
            else: s= ''
            self.wTable.setText(r, 3, s)


if __name__ == "__main__":
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Vat()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
