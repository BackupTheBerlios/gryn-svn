
from qt import *
import Control.uSourceVat
import Model.Global
import Model.Util

class SourceVat(Control.uSourceVat.uSourceVat):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        Control.uSourceVat.uSourceVat.__init__(self,parent,name,modal,fl)

        co= Model.Global.getClientObject()
        print co
        periods= int(co.periodes)
        print 'periods: ', periods
        for i in range(0, periods):
            print 'inserting ', i
            self.wPeriod.insertItem(str(i+1))

        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)
        self.connect(self.wOK,SIGNAL("clicked()"),self.slotOK)

    def slotOK(self):
        source= Model.Util.vatTransfer(int(str(self.wPeriod.currentText())), 0)
        print 'Generated source number ', source
        self.done(1)

    def slotCancel(self):
        print 'Cancelled'
        self.done(0)
