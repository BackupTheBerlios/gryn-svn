""" $Id$<br>
Select sources based on a range of ref numbers, dates, account number
or period.
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


import string
from qt import *
import Control.uSourceSelect
import Control.Global
import Model.Global
import Model.Books

class SourceSelect(Control.uSourceSelect.uSourceSelect):
    """Dialogue to search for sources based on one of several property
    ranges.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up dialogue.
        """
        Control.uSourceSelect.uSourceSelect.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("SourceSelect")
        self._sourceL= Model.Books.getList('source')
        self._accountL= Model.Books.getList('account')
        self._splitL= Model.Books.getList('split')

        self.wbAll.setChecked(1)
        Control.Global.dateFieldInit(self.wDateFrom) # set to today's date
        Control.Global.dateFieldInit(self.wDateTo) # set to today's date

        # init the period combo items
        self._pers= int(Model.Global.getClientObject().periodes)
        for i in range(0, self._pers):
            self.wPeriod.insertItem(str(i+1))

        self.connect(self.wOK,SIGNAL("clicked()"),self.slotOK)
        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)
        self.connect(self.wSourceFrom, SIGNAL('textChanged(const QString &)'),
                                              self.fieldSourceChanged)
        self.connect(self.wSourceTo, SIGNAL('textChanged(const QString &)'),
                                              self.fieldSourceChanged)
        self.connect(self.wAccountFrom, SIGNAL('textChanged(const QString &)'),
                                              self.fieldAccountChanged)
        self.connect(self.wAccountTo, SIGNAL('textChanged(const QString &)'),
                                              self.fieldAccountChanged)
        self.connect(self.wDateFrom, SIGNAL('valueChanged(const QDate &)'),
                                              self.fieldDateChanged)
        self.connect(self.wDateTo, SIGNAL('valueChanged(const QDate &)'),
                                              self.fieldDateChanged)
        self.connect(self.wPeriod, SIGNAL('activated(int)'),
                                              self.fieldPeriodChanged)
        self.connect(self.wbSource, SIGNAL('pressed()'),
                                              self.radioSourcePressed)
        self.connect(self.wbAccount, SIGNAL('pressed()'),
                                              self.radioAccountPressed)
        self.connect(self.wbDate, SIGNAL('pressed()'),
                                              self.radioDatePressed)
        self.connect(self.wbPeriod, SIGNAL('pressed()'),
                                              self.radioPeriodPressed)

    def languageChange(self):
        """Function called by translator.
        """
        self.setCaption(self.tr("Select source"))
        self.wGroup.setTitle(self.tr("Selection criterium"))
        self.wbSource.setText(self.tr("Source"))
        self.wbDate.setText(self.tr("Date"))
        self.wbAccount.setText(self.tr("Account"))
        self.wbPeriod.setText(self.tr("Period"))
        self.textLabel1.setText(self.tr("From"))
        self.textLabel1_2.setText(self.tr("To"))
        self.wbAll.setText(self.tr("All"))
        self.wOK.setText(self.tr("OK"))
        self.wCancel.setText(self.tr("Cancel"))
        self.wShowSplits.setText(self.tr("Show splits"))
        
    def slotOK(self):
        """Called by signal when OK button clicked.
        """
        # do the search based on the radio button state
        sources= []
        if self.wShowSplits.isChecked(): format='showsplits'
        else: format= '   '
        sources.append((format, 'default'))
        if self.wbSource.isChecked() != 0:
            frm= string.strip(str(self.wSourceFrom.text()))
            to= string.strip(str(self.wSourceTo.text()))
            iFrm= int(frm)
            iTo= int(to)
            for i in self._sourceL:
                if int(i.ref) >= iFrm and int(i.ref) <= iTo: sources.append(i)
        elif self.wbAccount.isChecked() != 0:
            frm= string.strip(str(self.wAccountFrom.text()))
            to= string.strip(str(self.wAccountTo.text()))
            for i in self._splitL:
                acc= self._accountL.getById(i.account).num
                if acc >= frm and acc <= to:
                    sources.append(self._sourceL.getById(i.source))
        elif self.wbDate.isChecked() != 0:
            frm= string.strip(str(self.wDateFrom.text()))
            to= string.strip(str(self.wDateTo.text()))
            for i in self._sourceL:
                if i.date >= frm and i.date <= to: sources.append(i)
        elif self.wbPeriod.isChecked() != 0:
            dFrom, dTo= Model.Global.periodeNumToDates(
                int(str(self.wPeriod.currentText())), self._pers)
            for i in self._sourceL:
                if i.date >= dFrom and i.date <= dTo: sources.append(i)
        elif self.wbAll.isChecked() != 0:
            sources= [(format,'default')] + self._sourceL

        # We are now supposed to return a list of one or more source objects
        if len(sources) == 1:
            QMessageBox.information(self, Model.Global.getAppName(),
                                "Found no source to fit the criterium.\n"+
                                "Try an other criterium or cancel.")
            return
        # OK, save the list in global listSelected
        Control.Global.setListSelected(sources)
        self.done(1)

    def slotCancel(self):
        """Close the dialogue without further action.
        """
        self.done(0)

    def fieldSourceChanged(self, s):
        """Called when a source ref field loses focus. Turn on the
        corresponding radio button
        """
        self.wbSource.setChecked(1)
    
    def fieldAccountChanged(self, s):
        """Called when a account field loses focus. Turn on the
        corresponding radio button
        """
        self.wbAccount.setChecked(1)
    
    def fieldDateChanged(self, d):
        """Called when a date spin box loses focus. Turn on the
        corresponding radio button
        """
        self.wbDate.setChecked(1)
    
    def fieldPeriodChanged(self, idx):
        """Called when the period combo loses focus. Turn on the
        corresponding radio button
        """
        self.wbPeriod.setChecked(1)

    def radioSourcePressed(self):
        """Called when source ref number button clicked,
        Set focus on the source ref number field.
        """
        self.wSourceFrom.setFocus()
        

    def radioAccountPressed(self):
        """Called when account number button clicked,
        Set focus on the account number field.
        """
        self.wAccountFrom.setFocus()

    def radioDatePressed(self):
        """Called when date button clicked,
        Set focus on the date spin box.
        """
        self.wDateFrom.setFocus()

    def radioPeriodPressed(self):
        """Called when period button clicked,
        Set focus on the period combo.
        """
        self.wPeriod.setFocus()


