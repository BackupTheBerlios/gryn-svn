""" $Id$<br>
This table is used in the Source dialogue. Inherits QTable, fairly hairy.
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
from qttable import QTable, QTableItem
import Model.Global
import Model.Grep
import Model.Books
import Control.Global


class C(object):
    """This class defines some table column number constants.<br>
    'NumCol': The column number for account numbers, int<br>
    'NameCol': The column number for account names, int<br>
    'DebitCol': The column number for debit amounts, int<br>
    'CreditCol': The column number for credit amounts, int
    """
    NumCol= 0
    NameCol= 1
    DebitCol= 2
    CreditCol= 3

class SourceTable(QTable):
    """SourceTable widget, one line for each split of the source.
    """
    def __init__(self, parent= None, name = None, fl = 0):
        """Set up of the table.
        """
        self.parent= (name, fl)
        QTable.__init__(self, parent, 'table')
        self.parent= parent
        self._itemKeeper= [] # a list for all tableitems of the table
        self.setGeometry(QRect(10,10,451,231))
        self.setNumRows(1)
        self.setNumCols(4)
        self.setSelectionMode(QTable.SingleRow)
        self.setHScrollBarMode(QScrollView.AlwaysOff)
        self._splits= {} # a dictionary for all splits of the table, row is key
        self._vat= {} # a dictionary for row-vat codes, row is key
        # regular expressions for the money columns: Any number of
        # digits optionally followed by a decimal separator and up
        # to two digits
        self.reMoney= r"^\d*(%s\d\d)?$"%Model.Global.getDecSep()
        # Regular expression for the account number column: four digits
        self.reAccount= r"^\d\d\d\d$"
        self.connect(self,SIGNAL("valueChanged(int, int)"),
                     self.slotCellCh)
        self.accountL= Model.Books.getList('account')
        self.vatL= Model.Books.getList('vat')
        self.insertItems(0) # Prepare the first row
        
    def setParent(self, parent):
        """Method to set the parent property<br>
        'parent': The source dialogue object
        """
        self.parent= parent

    def setVat(self, row, vat):
        """Save the VAT-code for this row. This will probably not be
        useful<br>
        'row': The row this is about, int
        'vat': The VAT-code, 1 char
        """
        self._vat[row]= vat

    def getVat(self, row):
        """Get the VAT-code for this row.<br>
        'row': The row this is about, int
        'return': The VAT-code, 1 char, space if not set
        """
        try:
            v= self._vat[row]
            return v
        except KeyError:
            return ' '
        
    def setRowSplit(self, row, split):
        """Insert a split into the splits dictionary.<br>
        'row': The row of the split, used as dictionary key<br>
        'split': The split object to insert
        """
        if self._splits.has_key(row):
            if not self._splits[row]:
                print "inserted new split in row %d %s"%(row, split)
                self._splits[row]= split
            else:
                print "do not insert new split in row %d %s"%(row, split)
        else:
            print "inserted new split in row %d %s"%(row, split)
            self._splits[row]= split

    def getRowSplit(self, row):
        """Get the split object of a table row.<br>
        'row': The row of the wanted split<br>
        'return': The split object, None if not found
        """
        try:
            r= self._splits[row]
            return r
        except KeyError:
            return None

    def removeRowSplits(self):
        """Forget all registered splits.
        """
        self._splits= {}
        self._vat= {}

    def insertItems(self, row, split= None):
        """Ensure that enough rows are available and insert
        table items in each cell of the new row.<br>
        'row': The table row to prepare<br>
        'split': Optional split object to save with this row
        """
        self.ensureEnoughRows(row)
        align= Qt.AlignRight|Qt.AlignVCenter

        # insert a TabItemRe object in account number cell
        mi= TabItemRe(self, '', align, self.reAccount) 
        self.setItem(row, C.NumCol, mi)
        self._itemKeeper.append(mi) # keep a reference to the item

        # insert a TabItemRe object in account name cell
        mi= TabItemRe(self, '', Qt.AlignLeft|Qt.AlignVCenter, None, 1)
        self.setItem(row, C.NameCol, mi)
        self._itemKeeper.append(mi)

        # insert a TabItemRe object in the debit cell
        mi= TabItemRe(self, '', align, self.reMoney)
        self.setItem(row, C.DebitCol, mi)
        self._itemKeeper.append(mi)

        # insert a TabItemRe object in the credit cell
        mi= TabItemRe(self, '', align, self.reMoney)
        self.setItem(row, C.CreditCol, mi)
        self._itemKeeper.append(mi)

        # save the split too
        self.setRowSplit(row, split)

    def wipeAll(self):
        """Clear all fields of the table, prepare row 0 and update
        the balance field.
        """
        while self.numRows() > 1:
            self.removeRow(0)
        for col in range(0, self.numCols()): self.clearCell(0, col)
        self.insertItems(0)
        self.parent.setBalance()
        self.removeRowSplits()

    def wipeSelectedRow(self):
        """Clear all fields of the selected row.
        """
        row= self.currentRow()
        self.insertItems(row)
        for col in range(0,4): self.setText(row, col, QString(''))
        
        self.item(row, C.DebitCol).setEnabled(1)
        self.item(row, C.CreditCol).setEnabled(1)
        self.parent.setBalance()
        if self._vat.has_key(row): del self._vat[row]
        try:
            if self._splits.has_key(row): del self._vat[row]
        except KeyError:
           pass 

    def perhapsAppendRow(self, row):
        """Caller needs a row for a new split, append one if neccessary<br>
        'row': The row number we will use, int
        'return': The present number of rows in the table, int
        """
        rows= self.numRows()
        if row==rows-1:
            self.setNumRows(rows+1)
            self.insertItems(rows)
        return self.numRows()
        
    def ensureEnoughRows(self, r):
        """Caller needs a number of rows. Ensure enough rows
        are present.<br>
        'r': Number of rows needed
        """
        rows= self.numRows()
        if r >= rows:
            self.setNumRows(r+1)

    def insertSplit(self, split):
        """Insert a split in its table row.<br>
        'split': The split object. split.line is the row to insert to
        """
        r= int(split.line)
        if self.text(r, C.NumCol).length() != 0: # CHIDEP
            print 'double split in row %d'%r
        self.ensureEnoughRows(r)
        #if not self.item(r, 0):
        self.insertItems(r, split)
        acc= self.accountL.getById(split.account)
        self.setText(r, C.NumCol, acc.num)
        self.setText(r, C.NameCol, acc.name)
        self.setAccount(r, acc)
        if split.side=='D':
            self.setText(r, C.DebitCol, Model.Global.intToMoney(split.amount))
        else:
            self.setText(r, C.CreditCol, Model.Global.intToMoney(split.amount))

    def setAccount(self, row, acc):
        """Save the account object in the table row item.<br>
        'row': The table row, int<br>
        'acc': The Account object
        """
        itm= self.item(row, C.NumCol)
        try:
            itm.acc= acc
            #self.setText(row, C.NumCol, acc.num)
            #self.setText(row, C.NameCol, acc.name)
        except AttributeError: # We forgot to set the item here, CHIDEP
            QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('Missing account field'))
            raise(Control.Global.MissingField(None))


    def getAccount(self, row):
        """Return the Account object saved for this row.<br>
        'row': The row number, int<br>
        'return': The Account object saved with the row.
        """
        itm= self.item(row, C.NumCol)
        return itm.acc

    def calcBalance(self):
        """Calculates the signed sum of all split amounts.<br>
        'return': The balance, int
        """
        c= 0
        d= 0
        rows= self.numRows()
        for row in range(0, rows):
            if not self.item(row, 0): continue
            ci= int(Model.Global.moneyToInt(self.text(row, C.CreditCol)))
            di= int(Model.Global.moneyToInt(self.text(row, C.DebitCol)))
            c= c + ci
            d= d + di
        return c-d

    def setDefaultVat(self, acc):
        """Set the combo selection to the index given by
        the account's default VAT property.<br>
        'acc': The Account object.
        """
        if acc: self.parent.wVatCombo.setCurrentItem(int(acc.defVat))

        
#### Slots for Split table signals
        

    def slotCellCh(self, row, col):
        """This function is called when a table cell's value change.
        Called after field editing over.<br>
        'row': Row number, int, supplied with signal<br>
        'col': Column number, int, supplied with signal
        """
        #Choose the appropriate function
        if col == C.NumCol: self.accountCellChanged(row, col)
        elif col == C.NameCol: self.nameCellChanged(row, col)
        else: self.amountCellChanged(row, col)

    def accountCellChanged(self, row, col):
        """Handles changes in the account number cell.<br>
        'row': The row of the cell, int<br>
        'col': The column of the cell, int
        """
        s= self.text(row, col)
        if s.isEmpty(): return
        if s.length()==4: # We have a valid account number
            acc= self.accountL.getByNum(str(s)) # Get the account object
            if acc:
                self.setAccount(row, acc)
                self.setText(row, C.NameCol, acc.name)
                self.setDefaultVat(acc)
            else: 
                self.setText(row, C.NameCol, '')
                QMessageBox.information(self, Model.Global.getAppName(),
                  self.tr("This account does not exist\n"))
                s= QString('')
                self.setText(row, col, s)
        if s.length()>4: # Illegal, CHIDEP
            self.setText(row, col, s[:4])

    def nameCellChanged(self, row, col):
        """Handle changes in the account name cell, fills in account number
        and name in table row. Assumes the account
        object is already defined (presumeably by the name grepper or by
        explicitly setting of the account number).<br>
        'row': The row of the cell, int<br>
        'col': The column of the cell, int
        """
        acc= col # for pychecker
        acc= self.getAccount(row)
        if not acc: return
        self.setDefaultVat(acc)
        self.blockSignals(1)
        self.setText(row, C.NumCol, acc.num)
        self.setText(row, C.NameCol, acc.name)
        self.blockSignals(0)

    def amountCellChanged(self, row, col):
        """Handle changes in one of the amount cells. Sets 

        """
        if self.text(row, C.NumCol).isEmpty():
            QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('Specify account first'))
            self.parent.setBalance()
            return
        s= self.text(row, col)
        print ' self.text:|%s|'%s
        if s.isEmpty():
            self.blockSignals(0)
            return
        else: # reformat the money amount
            print 'was not empty'
            i= Model.Global.moneyToInt(str(s)) 
            m= Model.Global.intToMoney(i) # blank if zero
            self.setText(row, col, m)
            self.updateCell(row, col)
            w= self.cellWidget(row, col)
            if w: w.setText(m)
        if col == C.DebitCol: # disable the credit cell
            self.item(row, C.CreditCol).setEnabled(0)
            if self.text(row, C.DebitCol).isEmpty(): 
                self.item(row, C.CreditCol).setEnabled(1)
        if col == C.CreditCol: # disable the debit cell
            self.item(row, C.DebitCol).setEnabled(0)
            if self.text(row, C.CreditCol).isEmpty(): 
                self.item(row, C.DebitCol).setEnabled(1)

        #self.setVat(row, "%d"%self.parent.wVatCombo.currentItem())

        # Prepare a new table row if all rows used
        rows= self.numRows()
        if row == rows-1 and self.text(row, col).length() > 0:
            self.ensureEnoughRows(row+1)
            self.insertItems(row+1)
            print 'inserted item at row ', row+1
        # Shall we produce a VAT split?
        code= self.parent.wVatCombo.currentItem()
        if  self.vatL[code].vatRate != None:
            self.calculateVat(row)
        self.parent.setBalance()

        row= 0
        #print 'looping soon from row ', row
        #while not self.text(row, C.DebitCol).isEmpty() or \
        #          not self.text(row, C.CreditCol).isEmpty():
        #    row= row + 1
        #    print 'rowloop: ', row
        #print 'goto row ', row
        #self.setCurrentCell(row, 0)
        #if one amount cell filled in:
        #row= ?
        #self.setCurrentCell(row, C.NumCol)# Go to next row
        # TODO: Find out how to get to the cell in first unused row column 0
        self.blockSignals(0)

    def accInject(self, a):
        """Called by an external signal wanting to inject an account object
        into this dialogue.<br>
        'a': The account object to inject
        """
        self.setActiveWindow() # get focus back
        row= self.currentRow()
        self.setText(row, C.NumCol, a.num)
        self.setText(row, C.NameCol, a.name)
        self.setCurrentCell(row, C.DebitCol)
        self.setAccount(row, a)

    def getTableAmount(self, row):
        """Get the amount of a table row.<br>
        'row': The row number, int<br>
        'return': Tuple of amount and side ('D'||'C'), both strings,
        amount in money format, blank if zero
        """
        col= C.DebitCol 
        rA= string.strip(str(self.text(row, col)))
        if len(rA) == 0:
            col= C.CreditCol
            rA= string.strip(str(self.text(row, col)))
        return (rA, col)

    def calculateVat(self, row):
        """Calculates the VAT, inserts a new
        split into the table and updates the balance field.<br>
        'row': Row to base the calculation on.
        """
        a, col= self.getTableAmount(row) # get amount and side
        if a == '' : return
        amount= Model.Global.moneyToInt(a)
        vatCode= self.parent.wVatCombo.currentItem()
        #self.setVat(row, "%d"%vatCode)
        vatObj= self.vatL.getByCode('%1d'%vatCode) # This object knows all
        rate= vatObj.vatRate
        if not rate: # No vat to do
            return 
        rate= float(rate)
        acc= vatObj.vatAccount
        if self.parent.wNet.isChecked() != 0: # The amount is net value
            vatAmount= int((amount * rate + 0.5)/100.0)
            newAmount= amount
        else: # The amount is gross value (net value + VAT)
            newAmount= int((100.0*amount)/(100.0 + rate) + 0.5)
            vatAmount= amount - newAmount
        # Put the results into the table at row= row+1
        accObj= self.accountL.getByNum(acc)
        if not accObj:
            QMessageBox.information(self, Model.Global.getAppName(),
                   self.tr("The VAT-account %s does not exist"%acc))
            return
        accName= accObj.name
        newAmountS= Model.Global.intToMoney(newAmount)# Blank if zero
        vatAmountS= Model.Global.intToMoney(vatAmount)# Blank if zero
        self.setText(row, col, newAmountS)
        w= self.cellWidget(row, col)
        if w: w.setText(newAmountS)
        self.setText(row+1, C.NumCol, acc)
        self.setText(row+1, C.NameCol, accName)
        self.setText(row+1, col, vatAmountS)
        try:
            self.setAccount(row+1, accObj)
            self.ensureEnoughRows(row+2)
            self.insertItems(row+2)
        except Control.Global.MissingField: # CHIDEP
            print 'SourceTable. Missing field row ', row
            pass


######################
#
# TabItemRe class
#

class TabItemRe(QTableItem):
    """Table item class that can align cell contents, optionally
    grep on cell value and apply a regular expression on editor input.
    Inherits QTableItem.
    """
    def __init__(self, table, text, align, reStr, grep= 0):
        """Set up the cell item.<br>
        'table': The table object<br>
        'text': Initial text of the cell<br>
        'align': Alignment property<br>
        'reStr': Regular expression string<br>
        'grep': Apply grep 1, do not grep 0
        """
        QTableItem.__init__(self, table, QTableItem.OnTyping, text)
        self.setReplaceable(0) # else our reItem will disappear again
        self.align= align # remember the alignment for the painter
        if reStr: self.re= QRegExp(reStr) # and the regexp
        else: self.re= None
        self.grep= grep
        self.acc= None


    def createEditor(self):
        """This function is called when we begin a cell edit.
        Uses the standard line editor, the table view port from parent.
        """
        self.editor= QLineEdit(self.text(), self.table().viewport())
        if self.grep != 0:
            QObject.connect(self.editor,
                           SIGNAL("textChanged(const QString &)"),
                           self.slotValueChanged)
            QObject.connect(self.editor, SIGNAL("lostFocus()"),
                           self.lostFocus) 
            self._nameGrep= Model.Grep.Grep(self.table().accountL, 'name',
                                            'len(i._num) < 4')
        # Use a regular expression validator
        elif self.re:
            self.val= QRegExpValidator(self.re, None)
            self.editor.setValidator(self.val)
        return self.editor


    def slotValueChanged(self, stxt):
        """Called when the editor content changes, ie for each char typed.<br>
        'stxt': Current editor text
        """
        acc= None
        txt= str(stxt)
        # Try to find a matching account name
        s, gLen= self._nameGrep.grepInput(txt)
        e= self.editor
        #t= self.table
        if gLen >= 0: # we have more than one match
            e.blockSignals(1)
            e.setText(s)
            e.setCursorPosition(gLen)
            acc= None
            e.blockSignals(0)
        else: # unique account name found
            e.blockSignals(1)
            e.setText(s.name)
            e.setCursorPosition(gLen)
            e.blockSignals(0)
            acc= s
            row= self.row()
            self.table().setAccount(row, acc) # Fill in number and name

    def lostFocus(self):
        """Get called when cell editing is finished. Fixes the
        account and account name cells.
        """
        # Account number was only set if grep found a unique match
        acc= self.table().getAccount(self.row())
        # if not unique, use the first in the list of matches
        if not acc: acc= self._nameGrep.getFirstMatch() 
        sn= acc.name
        # remove traces from grep
        p= string.find(sn, ':')
        if p >= 0: # use the text following  the colon only
            sn= sn[p+2:]
        self.setText(sn)
        acc.name= sn
        self.table().setAccount(self.row(), acc)
        self.editor= None

    def paint(self, painter, colGroup, rect, selected):
        """Use this Paint instead of the  QTableItem.Paint. This painter
        knows how to right align numbers with decimal separator=','
        """
        w= rect.width()
        h= rect.height()
        # fill with backgroundcolor, rect is table-relative
        # use colorGroup-colors so the table will fit to present theme
        if selected != 0:
            c= colGroup.brush(QColorGroup.Highlight)
        else:
            c= colGroup.brush(QColorGroup.Base)
        painter.fillRect(0, 0, w, h, c)
        # prepare for painting the text
        if selected != 0:
            painter.setPen(colGroup.highlightedText())
        else:
            painter.setPen(colGroup.Text)
        #Draw the text, Don't put the text closer than 2px to the cell limits 
        painter.drawText(2, 0, w-4, h, self.align, self.text())
        # Check the QPainter C++ source to find out how to do word wrap if
        # needed

