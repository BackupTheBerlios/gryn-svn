""" $Id$<br>
Dialogue to find sources that match one or more search criteria:
Date range, source reference range, split amount range and
split account number.
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
import string
import Control.uSourceFind
import Control.Global
import Model.Books
import Model.Global


class Prop(object):
    """Collects search-properties for one source.
    """
    def __init__(self, source, splitL, accountL):
        """Collect properties from the source and its splits.<br>
        'source': The source object<br>
        'splitL': The list of splits<br>
        'accountL': The list of accounts
        """
        self.source= source
        self.num= int(source.ref)
        self.date= source.date
        self.amounts= []
        self.accounts= []
        splits= splitL.getBySource(source.id)
        for i in splits:
            self.amounts.append(i.amount)
            self.accounts.append(int(accountL.getById(i.account).num))
            

class SourceFind(Control.uSourceFind.uSourceFind):
    """Dialogue to set up searc criteria.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up dialogue.
        """
        Control.uSourceFind.uSourceFind.__init__(self,parent,name,modal,fl)
        self.sprop= [] # List of Prop-instances, one for each source
        self.found= [] # List of found sources that match
        if not name:
            self.setName("SourceFind")
        self.sourceL= Model.Books.getList('source')
        self.accountL= Model.Books.getList('account')
        self.splitL= Model.Books.getList('split')
        # Build the sprop list
        for i in self.sourceL:
            if i.deleted == 'Y': continue
            self.sprop.append(Prop(i, self.splitL, self.accountL))

        # Set the date spin boxes to the first and last day of year 
        y= int(Model.Global.getClientYear())
        Control.Global.dateFieldInit(self.wDateFrom, QDate(y, 1, 1))
        Control.Global.dateFieldInit(self.wDateTo, QDate(y, 12, 31))

        # Set regexp for the ref range fields, allow only digits
        self.numVal= QRegExpValidator(QRegExp(QString(r'^\d+')), None)
        self.wNumFrom.setValidator(self.numVal)
        self.wNumTo.setValidator(self.numVal)

        # Set regexp for the account range fields. Allow only four digits
        self.accountVal= QRegExpValidator(QRegExp(QString( r"^\d\d\d\d$")),
                                          None)
        self.wAccountFrom.setValidator(self.accountVal)
        self.wAccountTo.setValidator(self.accountVal)

        # Set regexp for amount range, allow digits optionally followed
        # by decimal separator and up to two digits
        self.moneyVal= QRegExpValidator(QRegExp(QString(
            r"^\d*(%s\d\d)?$"%Model.Global.getDecSep())), None)
        self.wAmountFrom.setValidator(self.moneyVal)
        self.wAmountTo.setValidator(self.moneyVal)

        self.connect(self.wSearch,SIGNAL("clicked()"),self.slotSearch)
        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)

        self.connect(self.wFindNumber, SIGNAL('toggled(bool)'),
                     self.slotFindNumber)
        self.connect(self.wFindDate, SIGNAL('toggled(bool)'),
                     self.slotFindDate)
        self.connect(self.wFindAmount, SIGNAL('toggled(bool)'),
                     self.slotFindAmount)
        self.connect(self.wFindAccount, SIGNAL('toggled(bool)'),
                     self.slotFindAccount)

        self.connect(self.wAmountFrom, SIGNAL('lostFocus()'),
                     self.slotAmountFrom)
        self.connect(self.wAmountTo, SIGNAL('lostFocus()'),
                     self.slotAmountTo)

    def slotFindNumber(self, st):
        """Called when the ref check box changes state
        """
        if st != 0: self.wNumFrom.setFocus()

    def slotFindDate(self, st):
        """Called when the date check box changes state
        """
        if st != 0: self.wDateFrom.setFocus()

    def slotFindAccount(self, st):
        """Called when the account check box changes state
        """
        if st != 0: self.wAccountFrom.setFocus()

    def slotFindAmount(self, st):
        """Called when the amount check box changes state
        """
        if st != 0: self.wAmountFrom.setFocus()

    def slotAmountFrom(self):
        """Called when amount from field loses focus. Reformats field
        """
        m= Model.Global.moneyReformat(str(self.wAmountFrom.text()))
        self.wAmountFrom.setText(m)

    def slotAmountTo(self):
        """Called when amount to field loses focus. Reformats field
        """
        print 'slotAmountTo'
        m= Model.Global.moneyReformat(str(self.wAmountTo.text()))
        self.wAmountTo.setText(m)
        
    def slotSearch(self):
        """Called when user clicks search button. Search for matching
        sources.
        """
        listS= None
        sAccount= None
        sAmount= None
        ss= [] # list of search criteria for the splits (amount and account)
        if self.wFindAmount.isChecked() != 0: #search for amount range
            sAmount= '(sp.amounts[i] >= %s and sp.amounts[i] <= %s)'%(
                self.wAmountFrom.text(), self.wAmountTo.text())
            ss.append(sAmount)

        if self.wFindAccount.isChecked() != 0: # search for account range
            sAccount= '(sp.accounts[i] >= %s and sp.accounts[i] <= %s)'%(
                self.wAccountFrom.text(), self.wAccountTo.text())
            ss.append(sAccount)

        s= string.join(ss, ' and ')
        if len(ss) > 0:
            listS= []
            # search the sources and append matches to listS
            for sp in self.sprop:
                for i in range(0, len(sp.accounts)):
                    if eval(s): #TODO: compile the expression first
                        listS.append(sp)
                        break
        else:
            listS= self.sprop
        # we now have a list of potential objects for further search 

        ss= []
        # make search criterium for source ref number
        if self.wFindNumber.isChecked() != 0:
            s='(i.num >= %s and i.num <= %s)'%(self.wNumFrom.text(),
                                             self.wNumTo.text())
            ss.append(s)
        # make search criterium for the source date
        if self.wFindDate.isChecked() != 0:
            sep= Model.Global.getDateSep()
            d1= self.wDateFrom.date()
            s1= str(d1.toString('yyyy%sMM%sdd'%(sep, sep)))
            d2= self.wDateTo.date()            
            s2= str(d2.toString('yyyy%sMM%sdd'%(sep, sep)))
            s='(i.date >= %s and i.date <= %s)'%(s1, s2)
            ss.append(s)
        s= string.join(ss, ' and ')

        if len(ss) == 0: # We only wanted to search on split properties
            self.found= listS
        else: #search source properties and save matches
            for i in listS:
                if eval(s):
                    self.found.append(i)
        # Make a list of source objects of the found matches
        sFound= []
        for i in self.found: sFound.append(i.source)
        if len(sFound) == 0:
            QMessageBox.information(self, Model.Global.getAppName(),
                  str(self.tr("Found no source to fit the criterium.\n"))+
                  str(self.tr("Try an other criterium or cancel.")))
            return
        # Save the found source objects in the global listSelected
        Control.Global.setListSelected(sFound)
        self.done(1)


    def slotCancel(self):
        """Close dialogue"""
        self.done(0)


