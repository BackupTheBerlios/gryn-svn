from qt import *
import Control.uCuvenSelect
import Model.Books


class CuvenSelect(Control.uCuvenSelect.uCuvenSelect):

    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        Control.uCuvenSelect.uCuvenSelect.__init__(self,parent,name,modal,fl)

        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)
        self.connect(self.wOK,SIGNAL("clicked()"),self.slotOK)
        self.connect(self.wPick,SIGNAL("clicked()"),self.slotPick)

    def fromForm(self):
        L=[]
        rawL= Model.Books.getList('cuven')
        if len(rawL) < 1:
            QMessageBox.information(self, Model.Global.getAppName(),
                self.tr("No customer/vendor found"))
            return None, ''
        
        if self.wCust.isChecked(): # remove vendors
            L.append(Model.Cuven.CuvenList())
            L[-1].fixup(0)
            for i in rawL:
                if i.type=='C': L[-1].append(i)
        else: # remove customers
            L.append(Model.Cuven.CuvenList())
            L[-1].fixup(0)
            for i in rawL:
                if i.type=='V': L[-1].append(i)

        # Now, do any further filtering
        lotL= Model.Books.getList('lot')
        if self.wActive.isChecked():
            L.append(Model.Cuven.CuvenList())
            L[-1].fixup(0)
            for i in L[-2]:
                if L[-2].isUsed(i) != 0:
                    L[-1].append(i)
        if self.wOpenOnly.isChecked():
            L.append(Model.Cuven.CuvenList())
            L[-1].fixup(0)
            for i in L[-2]:
                f= lotL.getOpenByCuven(i.id)
                if len(f): L[-1].append(i)

        # How detailed a report do we want?
        if self.wDetSum.isChecked():
            fmt= 'summary'
        elif self.wDetOpen.isChecked():
            fmt= 'open'
        else:
            fmt= 'all'
        return (L[-1], fmt)
    
    def slotCancel(self):
        self.done(0)

    def slotOK(self):
        L, format= self.fromForm()
        if not L: self.done(0)
        if len(L) < 1 :
            QMessageBox.information(self, Model.Global.getAppName(),
                str(self.tr(
                "Found no customer/vendor to fit the criterium."))+'\n'+
                str(self.tr("Try an other criterium or cancel.")))
            self.done(0)
            return
        cuvens= [(format,'default')] + L
        # We are now supposed to return a list of one or more cuven objects
        # OK, save the list in global listSelected
        Control.Global.setListSelected(cuvens)
        self.done(1)

    def slotPick(self):
        L, format= self.fromForm()
        
        if self.wCust.isChecked():
            c= Control.ListSelect.CustomerSelect(self, L, 1)
        else:
            c= Control.ListSelect.VendorSelect(self, L, 1)
        c.show()
        r= c.exec_loop()
        if r != 0:
            l=  [(format,'default')] + Control.Global.getListSelected()
            Control.Global.setListSelected(l)
            self.done(1)        
