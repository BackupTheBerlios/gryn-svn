""" $Id$<br>
This dialogue lets the user specify a date range, used for report generation.
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
import Control.uTimeFrameSelect 
import Control.Global
import Model.Global
import Model.Books 

class TimeFrameSelect(Control.uTimeFrameSelect.uTimeFrameSelect):
    """Base class for the date range class,
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue.
        """
        Control.uTimeFrameSelect.uTimeFrameSelect.__init__(
            self,parent,name,modal,fl)

        if not name:
            self.setName("TimeFrameSelect")

        # Init the periode combo
        self.pers= int(Model.Global.getClientObject().periodes)
        print "client periodes: %d"%self.pers
        for i in range(0, self.pers):
            self.wPeriode.insertItem(QString(str(i+1)))

        #Init the date spin boxes 
        y= int(Model.Global.getClientYear())
        Control.Global.dateFieldInit(self.wDateFrom,  QDate(y, 1, 1))#1. jan
        Control.Global.dateFieldInit(self.wDateTo) # Today
        
        self.connect(self.wOk,SIGNAL("clicked()"),self.slotOk)
        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)
        self.connect(self.rPeriode, SIGNAL('toggled(bool)'),
                     self.slotPeriode)
        self.connect(self.rDate, SIGNAL('toggled(bool)'),
                     self.slotDate)
        self.connect(self.rAll, SIGNAL('toggled(bool)'),
                     self.slotAll)
        self.wPeriode.setEnabled(0)
        self.wDateFrom.setEnabled(0)
        self.wDateTo.setEnabled(0)
        self.rAll.setChecked(1) # select all by default

    def languageChange(self):
        """Called by translator.
        """
        self.setCaption(self.tr("Select date frame"))
        self.wFrame.setTitle(self.tr("Date frame"))
        self.rPeriode.setText(self.tr("Periode"))
        self.rAll.setText(self.tr("All"))
        self.wOk.setText(self.tr("OK"))
        self.wCancel.setText(self.tr("Cancel"))

    def slotPeriode(self, a):
        """Called for Periode radio button state changes.<br>
        'a': New state, if != 0 disable the other input fields.
        """
        if a != 0:
            self.wPeriode.setEnabled(1)
            self.wDateFrom.setEnabled(0)
            self.wDateTo.setEnabled(0)

    def slotDate(self, a):
        """Called for Date radio button state changes.<br>
        'a': New state, if != 0 disable the other input fields.
        """
        if a != 0:
            self.wPeriode.setEnabled(0)
            self.wDateFrom.setEnabled(1)
            self.wDateTo.setEnabled(1)

    def slotAll(self, a):
        """Called for All radio button state changes.<br>
        'a': New state, if != 0 disable the other input fields.
        """
        if a != 0:
            self.wPeriode.setEnabled(0)
            self.wDateFrom.setEnabled(0)
            self.wDateTo.setEnabled(0)


    def slotCancel(self):
        """Close dialogue.
        """
        self.done(0)

    def slotOk(self):
        """Called when user clicks OK-button, Subclass this.
        """
        pass 

class LedgerBalanceSelect(TimeFrameSelect):
    """Date range selector for ledger balance reports.
    """
    def __init__(self, parent= 0, name= None, modal= 0, fl= 0):
        """Set up dialogue.
        """
        TimeFrameSelect.__init__(self, parent, name, modal, fl)
        self.setCaption(self.tr("Select date frame"))

    def slotOk(self):
        """User clicked on OK button. Make a list of sources within date range.
        """
        if self.rPeriode.isChecked() != 0:
            periode= str(self.wPeriode.currentText())
            dFrom, dTo= Model.Global.periodeNumToDates(periode, self.pers)
        elif self.rDate.isChecked() != 0:
            dFrom=Control.Global.strFromQdate(self.wDateFrom.date())
            dTo= Control.Global.strFromQdate(self.wDateTo.date())
        else: # all
            y= Model.Global.getClientYear()
            dFrom= '%s.01.01'%y
            dTo= '%s.12.31'%y
        objectL= []
        #The first entry in the list is special, allows transfer of
        #options and parametres to report generator
        objectL.append(('default','default', dFrom, dTo))
        splitL= Model.Books.getList('split')
        sourceL= Model.Books.getList('source')
        # Collect all sources with dates before and incl  selected to-date
        print "splitlistlen: ", len(splitL)
        print "sourcelistlen: ", len(sourceL)
        for s in splitL:
            print "s in split: ", s
            source= sourceL.getById(s.source)
            print "   source :", source
            if source.deleted == 'Y': continue
            if source.date > dTo: continue
            objectL.append((s, source.date))
                    
        if len(objectL) == 1:
            QMessageBox.information(self, Model.Global.getAppName(),
                str(self.tr("Found no transactions in this date frame.\n"))+
                str(self.tr("Try an other criterium or cancel.")))
            return
        # Save the result in global listSelected 
        Control.Global.setListSelected(objectL)
        self.done(1)

        
            
            
