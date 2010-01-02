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
from PyQt4 import QtCore, QtGui
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
    VatCol= 4


class TabItemNumber(QTableItem):
    """Table item class for the account number column. Sets up a
    field validator to only accept max 4 digit input
     """
    def __init__(self, table, text):
        """Set up the cell item.<br>
        'table': The table object<br>
        'text': Initial text of the cell<br>
        """
        QTableItem.__init__(self, table, QTableItem.OnTyping, text)
        self.setReplaceable(0) # else our reItem will disappear again
        self.align= Qt.AlignLeft|Qt.AlignVCenter
        self.re= QRegExp(r"^\d\d\d\d$") # and the regexp
        self.acc= None


    def createEditor(self):
        """This function is called when we begin a account numer edit.
        Uses the standard line editor, the table view port from parent.
        """
        self.editor= QLineEdit(self.text(), self.table.viewport())
        # Use a regular expression validator
        self.val= QRegExpValidator(self.re, None)
        self.editor.setValidator(self.val)
        return self.editor


class TabItemName(QTableItem):
    """Table item class for the account name cells. Sets up a grep
    for account names.
    """
    def __init__(self, table, text):
        """Set up the cell item.<br>
        'table': The table object<br>
        'text': Initial text of the cell<br>
        """
        QTableItem.__init__(self, table, QTableItem.OnTyping, text)
        self.setReplaceable(0) # else our reItem will disappear again
        self.align= Qt.AlignLeft|Qt.AlignVCenter
        self.acc= None


    def createEditor(self):
        """This function is called when we begin a account name cell edit.
        Uses the standard line editor, the table view port from parent.
        Sets up slots:<br>
        'slotValueChanged': When the editor content changes (user keying)<br>
        'lostFocus': When user moves to an other field (edit fin)
        """
        self.editor= QLineEdit(self.text(), self.table().viewport())
        QObject.connect(self.editor,
                        SIGNAL("textChanged(const QString &)"),
                        self.slotValueChanged)
        QObject.connect(self.editor, SIGNAL("lostFocus()"),
                        self.lostFocus) 
        self._nameGrep= Model.Grep.Grep(self.table().accountL, 'name',
                                            'len(i._num) < 4')
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



class TabItemMoney(QTableItem):
    """Table item class for the amount fields. Sets up a field validator
    which allows digits, possibly separated with the decimal separator.
    Right-adjusts result when finsished editing even if decimal sparator
    is not '.'
    """
    def __init__(self, table, text):
        """Set up the cell item.<br>
        'table': The table object<br>
        'text': Initial text of the cell<br>
        """
        QTableItem.__init__(self, table, QTableItem.OnTyping, text)
        self.setReplaceable(0) # else our reItem will disappear again
        self.align= Qt.AlignRight|Qt.AlignVCenter
        self.re= QRegExp(r"^\d*(%s\d\d)?$"%Model.Global.getDecSep())


    def createEditor(self):
        """This function is called when we begin a amount cell edit.
        Uses the standard line editor, the table view port from parent.
        """
        self.editor= QLineEdit(self.text(), self.table().viewport())
        # Use a regular expression validator
        self.val= QRegExpValidator(self.re, None)
        self.editor.setValidator(self.val)
        return self.editor

    def paint(self, painter, colGroup, rect, selected):
        """Use this Paint instead of the  QTableItem.Paint. This painter
        knows how to right align numbers with decimal separator !='.'
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

###################
        
class SplitRow(object):
    """
    Keeps track of each row in a SplitTable
    impoertant varaiables:<br>
    'row':  The table row<br>
    'split': A possible Split assosciated with the row<br>
    'accObj': A possible account object associated with the row<br>
    """
    accL= None # account list
    vatL= None # vat list
    table= None # the parent table
    
    def __init__(self, row, split= None):
        """
        Creates a SplitRow instance. The table is extended if too small
        for the given row.<br>
        'row: ' The row of the table<br>
        'split: ' Fills in the table row with text derived from this split
        
        """
        object.__init__(self)
        self.split= split
        self.row= row
        self.accObj= None
        if row >= SplitRow.table.numRows():
            SplitRow.table.setNumRows(row + 1)
        self.numItem= TabItemNumber(SplitRow.table, '')
        SplitRow.table.setItem(self.row, C.NumCol, self.numItem)
        self.nameItem= TabItemName(SplitRow.table, '')
        SplitRow.table.setItem(self.row, C.NameCol, self.nameItem)
        self.DebitItem= TabItemMoney(SplitRow.table, '')
        SplitRow.table.setItem(self.row, C.DebitCol, self.DebitItem)
        self.CreditItem= TabItemMoney(SplitRow.table, '')
        SplitRow.table.setItem(self.row, C.CreditCol, self.CreditItem)
        if split:
            if split.account:
                accO= SplitRow.accL.getById(split.account)
                self.accObj= accO
                SplitRow.table.blockSignals(1)
                SplitRow.table.setText(self.row, C.NumCol, accO.num)
                SplitRow.table.setText(self.row, C.NameCol, accO.name)
                SplitRow.table.blockSignals(0)
            mon= Model.Global.intToMoney(split.amount)
            if split.side == 'D':
                SplitRow.table.setText(self.row, C.DebitCol, mon)
                SplitRow.table.setText(self.row, C.CreditCol, '')
            else:
                SplitRow.table.setText(self.row, C.CreditCol, mon)
                SplitRow.table.setText(self.row, C.DebitCol, '')
            SplitRow.table.setText(self.row, C.VatCol, split.vat)

    def updateFields(self, split):
        """
        Derives field text from the supplied split and insert them
        into the table row
        """
        if split.account:
            print "split.account: ", split.account
            accO= SplitRow.accL.getById(split.account)
            self.accObj= accO

            SplitRow.table.setText(self.row, C.NumCol, accO.num)
            w= SplitRow.table.cellWidget(self.row, C.NumCol)
            if w: w.setText(accO.num)

            SplitRow.table.setText(self.row, C.NameCol, accO.name)
            w= SplitRow.table.cellWidget(self.row, C.NameCol)
            if w: w.setText(accO.name)

        mon= Model.Global.intToMoney(split.amount)
        if split.side == 'D':
            SplitRow.table.setText(self.row, C.DebitCol, mon)
            w= SplitRow.table.cellWidget(self.row, C.DebitCol)
            if w: w.setText(mon)

            SplitRow.table.setText(self.row, C.CreditCol, '')
            w= SplitRow.table.cellWidget(self.row, C.CreditCol)
            if w: w.setText('')
        else:
            SplitRow.table.setText(self.row, C.CreditCol, mon)
            w= SplitRow.table.cellWidget(self.row, C.CreditCol)
            if w: w.setText(mon)

            SplitRow.table.setText(self.row, C.DebitCol, '')
            w= SplitRow.table.cellWidget(self.row, C.DebitCol)
            if w: w.setText('')
        SplitRow.table.setText(self.row, C.VatCol, split.vat)
        

    def setAmount(self, side, intAmount):
        """
        Inserts the amount into the debit or credit field.<br>
        'intAmount': The amount in integer format
        """
        amnt= Model.Global.intToMoney(intAmount)
        if side == 'D': col= C.DebitCol
        else: col= C.CreditCol
        self.table.setText(self.row, col, amnt)
        w= SplitRow.table.cellWidget(self.row, col)
        if w: w.setText(amnt)
        
    def getAmount(self):
        """
        Return the integer amount of the debit+credit fields. Assumes
        one field is empty
        """
        mc= self.table.text(self.row, C.CreditCol)
        md= self.table.text(self.row, C.DebitCol)
        a= Model.Global.moneyToInt(mc) + Model.Global.moneyToInt(md)
        return a

        
    def isUsed(self):
        """
        Returns 1 if the table row is not empty. Do not consider the
        VAT-field.
        """
        table= SplitRow.table
        if table.text(self.row, C.NumCol) or \
              table.text(self.row, C.NameCol) or \
              table.text(self.row, C.DebitCol) or \
              table.text(self.row, C.CreditCol):
            return 1
        else: return 0

    def makeSplitFromTableRow(self, so, line):
        """
        Makes a split-object from texts extracted from the table row<br>
        'so': The source object this will belong to<br>
        'line': The line numer, not neccessarily equal to row+1
        """
        table= SplitRow.table
        num= str(table.text(self.row, C.NumCol)) #Account number
        if not num or len(num)==0: return None
        #If we edit, the split may be an old or a new one
        spl= self.split
        if not spl:
            spl= Model.Split.Split() # must make a new one
        spl.source= so.id 
        spl.account= SplitRow.accL.getByNum(num).id
        ad= str(table.text(self.row, C.DebitCol)) # debit amount
        ac= str(table.text(self.row, C.CreditCol)) # credit amount
        if len(ad)>0:
            spl.side= 'D'
            spl.amount= Model.Global.moneyToInt(ad)
        else:                    
            spl.side= 'C'
            spl.amount= Model.Global.moneyToInt(ac)
        spl.line= line
        spl.vat= str(table.text(self.row, C.VatCol)) # credit amount
        return spl

    def wipe(self):
        """
        Blanks all fields of the table row, also removes the
        associated split and account object.
        """
        for col in range(0,self.table.numCols()):
            self.table.setText(self.row, col, QString(''))
        self.split= None
        self.accO= None
        SplitRow.table.item(self.row, C.DebitCol).setEnabled(1)
        SplitRow.table.item(self.row, C.CreditCol).setEnabled(1)

###########################
        
class SplitTable(QTable):
    """SourceTable widget, one line for each split of the source.
    """
    def __init__(self, parent= None, name = None, fl = 0):
        """Set up of the table.
        """
        QTable.__init__(self, parent, 'table')

        self.parent= parent
        self.setNumRows(0)
        self.setNumCols(5)
        h= self.horizontalHeader()
        nt= self.tr('Number')
        h.setLabel(C.NumCol, nt)
        h.setLabel(C.NameCol, self.tr('Name'))
        h.setLabel(C.DebitCol, self.tr('Debit'))
        h.setLabel(C.CreditCol, self.tr('Credit'))
        h.setLabel(C.VatCol, '')
        v= self.verticalHeader()
        v.hide()
        fm= self.fontMetrics() # Get from a global setting instead?
        w1= fm.width('900.000.000.000')
        w2= fm.width(str(nt)+'0')
        w3= fm.width('00')
        self.setLeftMargin(0)
        self.setColumnWidth(C.NumCol, w2)
        self.setColumnWidth(C.DebitCol, w1)
        self.setColumnWidth(C.CreditCol, w1)
        self.setColumnStretchable(C.NameCol, 1)
        self.setColumnWidth(C.VatCol, w3)
        self.setColumnReadOnly(C.VatCol, 1)

        self.setGeometry(QRect(10,10,451,231))
        self.setSelectionMode(QTable.SingleRow)
        self.setHScrollBarMode(QScrollView.AlwaysOff)
        self.connect(self,SIGNAL("valueChanged(int, int)"),
                     self.slotCellCh)
        self.splitRows= []  # an array for all splitRows of the table
        SplitRow.table= self
        SplitRow.accL= Model.Books.getList('account')
        SplitRow.vatL= Model.Books.getList('vat')
        self.vatL= SplitRow.vatL
        self.accountL= SplitRow.accL

        self.accRound= Model.Global.getAccRound()

        row= self.whereToAppendRow()
        sr= SplitRow(row)
        self.splitRows.append(sr)

    def getLastRow(self):
        """
        Returns the number of the last used row of the table
        """
        row= -1
        sr= None
        for sr in self.splitRows:
            if sr.row > row:
                row= sr.row
                srr= sr
        return sr

    def whereToAppendRow(self):
        """
        Finds the first free row of the table
        """
        if len(self.splitRows) == 0: return 0
        sr= self.getLastRow()
        if sr.isUsed() == 0: return sr.row
        return sr.row + 1
    
    def setParent(self, parent):
        """Method to set the parent property. This function is obsolete<br>
        'parent': The source dialogue object
        """
        self.parent= parent

    def getSplits(self, so):
        """Returns a list of splits made from the current table content.<br>
        'so': The source object the list will belong to
        """
        self.checkVat()
        self.clearSelection()
        line= 0
        srList= [] 
        for r in self.splitRows:
            spl= r.makeSplitFromTableRow(so, line)
            if spl:
                srList.append(spl)
                line=line+1
        return srList
            
    def setVat(self, row, vat):
        """Set the table VAT-code for this row.<br>
        'row': The row this is about, int
        'vat': The VAT-code, 1 char
        """
        self.setText(row, C.VatCol, str(vat))


    def appendSplitRow(self, split= None):
        """
        Ensure that enough rows are available and insert
        table items into each cell of the first free  row.<br>
        'split': Optional split object to save with this row
        """
        row= self.whereToAppendRow()
        sr= self.getSplitRowByRow(row)
        if not sr:
            sr= SplitRow(row, split)
            self.splitRows.append(sr)
        if split:
            sr.updateFields(split)
            sr.split= split
            sr.accObj= self.accountL.getById(split.account)

    def makeRoundingSplit(self):
        """
        Fills in a row with rounding account info and amount into the current
        row (usually the last). However, if the account number of the current
        row is not blank, only the amount is inserted. In both cases the
        amount is the current difference between debit and credit.<br>
        returns 'int(0)' if OK, 'int(1) if rounding account is missing.
        """
        
        diff= self.calcBalance()
        if diff == 0: return 0
        if diff > 0: side= 'D'
        else: side= 'C'
        row= self.currentRow()
        sr= self.getSplitRowByRow(row)
        if not sr.isUsed():  # insert a rounding split there
            spl= Model.Split.Split()
            spl.amount= abs(diff)
            spl.vat= ' '
            spl.side= side
            accNum= self.accRound
            acc= self.accountL.getByNum(accNum)
            if not acc: # error, missing rounding account
                return 1
            spl.account= acc.id
            sr.updateFields(spl)
            self.appendSplitRow() # add a new blank row below
            
        else: # number and name present, just insert amount
            print "round insert amount only "
            sr.setAmount(side, abs(diff))
        return 0

    def wipeAll(self):
        """Clear all fields of the table, prepare row 0 and update
        the balance field.
        """
        for sr in self.splitRows:
            self.removeRow(sr.row)
        self.splitRows= []
        self.appendSplitRow()
        self.parent.setBalance()


    def wipeSelectedRow(self):
        """Clear all fields of the selected row.
        """
        row= self.currentRow()
        sr= self.getSplitRowByRow(row)
        sr.wipe()
        self.parent.setBalance()

    def setAccount(self, row, acc):
        """Save the account object in the table row item.<br>
        'row': The table row, int<br>
        'acc': The Account object
        """
        self.setText(row, C.NumCol, acc.num)
        self.setText(row, C.NameCol, acc.name)
        for r in self.splitRows:
            if r.row==row:
                r.accObj= acc
                return
        
    def getAccount(self, row):
        """Return the Account object saved for this row.<br>
        'row': The row number, int<br>
        'return': The Account object saved with the row.
        """
        sr= self.getSplitRowByRow(row)
        if sr:
            return sr.accObj
        return None

    def getSplitRowByRow(self, row):
        """
        Finds the splitRow object of the row<br>
        'row': The row to seach for
        """
        for r in self.splitRows:
            if r.row == row:
                return r
        return None

    def getCuvenAmount(self, type):
        """Finds the split table line where the account number
        corresponds to a customer or vendor transaction account.<br>
        'type': char indicating customer or vendor: 'C'|'V'
        'return': the integer format amount found
        """
        if type == 'V': accNum= Model.Global.getAccVendor()
        else: accNum= Model.Global.getAccCustomer()

        for sr in self.splitRows:
            num= self.text(sr.row, C.NumCol)
            if num == accNum:
                return sr.getAmount()
        return None


    def isSeleted_Cuven(self):
        """Check if a split table row's account number
        corresponds to a customer or vendor transaction account.<br>
        'return': yes: 1, no: 0
        """
        vAcc= Model.Global.getAccVendor()
        cAcc= Model.Global.getAccCustomer()
        row= self.currentRow()
        if str(self.text(row, C.NumCol)) == vAcc: return 1
        if str(self.text(row, C.NumCol)) == cAcc: return 1
        return 0
        
    def calcBalance(self):
        """Calculates the signed sum of all split amounts.<br>
        'return': The balance, int format
        """
        c= 0
        d= 0
        for sr in self.splitRows:
            ci= int(Model.Global.moneyToInt(self.text(sr.row, C.CreditCol)))
            di= int(Model.Global.moneyToInt(self.text(sr.row, C.DebitCol)))
            c= c + ci
            d= d + di
        return c-d

    def setDefaultVat(self, acc):
        """Set the combo selection to the index given by
        the account's default VAT property.<br>
        'acc': The Account object.
        """
        if acc: self.parent.wVatCombo.setCurrentItem(int(acc.defVat))


    def getSplitAmount(self, row):
        """Get the amount of a table row.<br>
        'row': The row number, int<br>
        'return': Tuple of amount and column number,
        amount in money format, blank if zero
        """
        col= C.DebitCol 
        rA= string.strip(str(self.text(row, col)))
        if len(rA) == 0:
            col= C.CreditCol
            rA= string.strip(str(self.text(row, col)))
        return (rA, col)

    def calculateVat(self, sr):
        """Calculates the VAT, inserts a new
        split into the table and updates the balance field.<br>
        'sr': SplitRow object to base the calculation on.<br>
        TODO: make a split and update table by update function
        """
        a, col= self.getSplitAmount(sr.row) # get amount and side
        if a == '' : return
        amount= Model.Global.moneyToInt(a)
        vatCode= self.parent.wVatCombo.currentItem()
        self.setVat(sr.row, vatCode)
        vatObj= self.vatL.getByCode('%1d'%vatCode) 
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
                   self.tr("The VAT-account does not exist") + '(%s)'%acc)
            return
        accName= accObj.name
        newAmountS= Model.Global.intToMoney(newAmount)# Blank if zero
        vatAmountS= Model.Global.intToMoney(vatAmount)# Blank if zero
        self.setText(sr.row, col, newAmountS)
        w= self.cellWidget(sr.row, col)
        if w: w.setText(newAmountS)

        row2= self.whereToAppendRow()
        sr2= SplitRow(row2)
        self.splitRows.append(sr2)
        self.setText(row2, C.NumCol, acc)
        self.setText(row2, C.NameCol, accName)
        self.setText(row2, col, vatAmountS)
        self.setVat(row2, ' ')
        try:
            self.setAccount(row2, accObj)
        except Control.Global.MissingField: # CHIDEP
            print 'SourceTable. Missing field row ', sr.row
            pass


    def checkVat(self):
        aArr= {}
        for v in self.vatL: 
            if v.vatAccount: aArr[v.vatAccount]= 0
            
        for s in self.splitRows:
            print "row %d "%s.row
            if not s.split: continue
            print "Vatkode split, %d <%s> %d"%(s.row,s.split.vat, s.split.amount)
            if len(s.split.vat) > 0 and s.split.vat != ' ':
                v= self.vatL.getByCode(s.split.vat)
                rate= float(v.vatRate)
                am= int((s.split.amount * rate + 0.5)/100.0)
                if s.split.side=='D': am= -am
                aArr[v.vatAccount]= aArr[v.vatAccount] + am
            num= s.accObj.num
            if aArr.has_key(num):
                am= s.split.amount
                if s.split.side=='C': am= -am
                aArr[num]= aArr[num] + am
            for k in aArr.keys():
                print ("%s %d"%(k, aArr[k]))
        print "Checking VAT "
        for k in aArr.keys():
            if aArr[k] != 0:
                print "split error %s %s"%(k,
                                           Model.Global.intToMoney(aArr[k]))
        
        print "Fin checking"



        
##################        
#   Slots for Split table signals
        

    def slotCellCh(self, row, col):
        """This function is called when a table cell's value change.
        Called after field editing over.<br>
        'row': Row number, int, supplied with signal<br>
        'col': Column number, int, supplied with signal
        """
        #Choose the appropriate function
        if col == C.NumCol: self.numberCellChanged(row, col)
        elif col == C.NameCol: self.nameCellChanged(row, col)
        else: self.amountCellChanged(row, col)

    def numberCellChanged(self, row, col):
        """Handles changes in the account number cell. Finds account object
        and inserts account name into table row<br>
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
                  self.tr("This account does not exist"))
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
        acc= self.getAccount(row)
        if not acc: return
        self.setDefaultVat(acc)
        self.blockSignals(1)
        self.setText(row, C.NumCol, acc.num)
        self.setText(row, C.NameCol, acc.name)
        self.blockSignals(0)

    def amountCellChanged(self, row, col):
        """Handle changes in one of the amount cells. Formats the amount
        and updates the amount field of the table. Experimentally also
        disables the other amount cell. Calculate and insert VAT row if
        VAT-field is set.
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
            print "widget: ", w
            if w: w.setText(m)
        if col == C.DebitCol: # disable the credit cell
            self.item(row, C.CreditCol).setEnabled(0)
            if self.text(row, C.DebitCol).isEmpty(): 
                self.item(row, C.CreditCol).setEnabled(1)
        if col == C.CreditCol: # disable the debit cell
            self.item(row, C.DebitCol).setEnabled(0)
            if self.text(row, C.CreditCol).isEmpty(): 
                self.item(row, C.DebitCol).setEnabled(1)


        # Shall we produce a VAT split?
        code= self.parent.wVatCombo.currentItem()
        if  self.vatL[code].vatRate != None:
            self.calculateVat(self.getSplitRowByRow(row))

        row= self.whereToAppendRow()
        sr= SplitRow(row)
        self.splitRows.append(sr)

        self.parent.setBalance()
        
        # TODO: The current cell is set to column 1, not 0. fix this bug.<br>
        # Bug cause: API not understood, PyQt implementation bug
        
        self.setCurrentCell(row, 0)
        self.blockSignals(0)

    def accInject(self, a):
        """Called by an external signal wanting to inject an account object
        into this dialogue.<br>
        'a': The account object to inject
        """
        self.setActiveWindow() # get focus back
        row= self.currentRow()
        self.setAccount(row, a)
        self.setDefaultVat(a)
        self.setCurrentCell(row, C.DebitCol)
        self.clearSelection()
