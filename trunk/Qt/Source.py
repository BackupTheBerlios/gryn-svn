""" $Id$<br>
Dialogue to create and maintain sources.
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


import sys
import string
from qt import *
from qttable import QTable, QTableItem
import Control.uSource
import Model.Source
import Model.Split
import Model.Global
import Model.Grep
import Model.Lot
import Model.LotEntry
from   Control.SourceTable import C
import Control.Global
import Control.RuleAssign
import Control.ListSelect

Debug= sys.stderr.write


#############################
#
# Base class for Source
#

class Source(Control.uSource.uSource):
    """The Source base class for showing the dialogue.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue. The split table is of classSourceTable
        """
        Control.uSource.uSource.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Source")

        # wTable is a table of splits
        self.wTable.setParent(self)    
        self.wTable.setNumRows(1)
        self.wTable.setNumCols(4)
        h= self.wTable.horizontalHeader()
        nt= self.tr('Number')
        h.setLabel(C.NumCol, nt)
        h.setLabel(C.NameCol, self.tr('Name'))
        h.setLabel(C.DebitCol, self.tr('Debit'))
        h.setLabel(C.CreditCol, self.tr('Credit'))
        v= self.wTable.verticalHeader()
        v.hide()
        fm= self.fontMetrics() # Get from a global setting instead?
        w1= fm.width('900.000.000.000')
        w2= fm.width(str(nt)+'0')
        self.wTable.setLeftMargin(0)
        self.wTable.setColumnWidth(C.NumCol, w2)
        self.wTable.setColumnWidth(C.DebitCol, w1)
        self.wTable.setColumnWidth(C.CreditCol, w1)
        self.wTable.setColumnStretchable(C.NameCol, 1)
        self.wBalance.setMinimumWidth(w1+w1)
        self.wBalance.setMaximumWidth(w1+w1)

        # wLotTable is a list of lots used when cuven given
        self.wLotTable.setNumRows(5)
        self.wLotTable.setNumCols(5)
        v= self.wLotTable.verticalHeader()
        v.hide()
        self.wLotTable.setLeftMargin(0)
        self.wLotTable.setEnabled(0) # enable only if cuven selected
        h= self.wLotTable.horizontalHeader()
        h.setLabel(0, self.tr('Ref'))
        h.setLabel(1, self.tr('Date'))
        h.setLabel(2, self.tr('Caption'))
        h.setLabel(3, self.tr('Amount'))
        h.setLabel(4, self.tr('Remaining'))
        self.wLotTable.setColumnStretchable(2, 1)
        self.wLotTable.setColumnWidth(0, fm.width('12345'))
        self.wLotTable.setColumnWidth(3, w1)
        self.wLotTable.setColumnWidth(4, w1)
        self.wLotTable.setSelectionMode(QTable.NoSelection)

        #Get all the lists we need
        self._accountL= Model.Books.getList('account')
        self._splitL= Model.Books.getList('split')
        self._sourceL= Model.Books.getList('source')
        self._cuvenL= Model.Books.getList('cuven')
        self._lotL= Model.Books.getList('lot')
        self._lotEntryL= Model.Books.getList('lotentry')
        self._ruleL= Model.Books.getList('rule')
        self._vatL= Model.Books.getList('vat')
        Control.Global.dateFieldInit(self.wDate)

        print "Cuven list: "
        for c in self._cuvenL: print c

        # init the VAT combo items
        self.wVatCombo.clear()
        for v in self._vatL:
            self.wVatCombo.insertItem(v.vatName) #assume list sorted by vatCode

        # init the rule combo items
        self.wRule.setEditable(1)
        self.wRule.setAutoCompletion(1) # grep from beginning of rule name
        self.wRule.clear()
        for r in self._ruleL:
            self.wRule.insertItem(r.name)
        self.wRule.setInsertionPolicy(self.wRule.NoInsertion)
        self.wRule.clearEdit()
        if len(self._ruleL) == 0:
            self.wRule.insertItem(self.tr('No rules available'))
            self.wRule.setEnabled(0)
        self.wResc.setEnabled(0)
        
        QObject.connect(parent,PYSIGNAL('accountSelected'),
                        self.wTable.accInject)

        # The following signals are injected from other windows
        QObject.connect(parent,PYSIGNAL('customerSelected'), self.cuvenInject)
        QObject.connect(parent,PYSIGNAL('vendorSelected'), self.cuvenInject)
        QObject.connect(parent, PYSIGNAL('sourceSelected'), self.sourceInject)

        # Called when the cuven field text changes, call the grepper
        self.connect(self.wCuven, SIGNAL('textChanged(const QString &)'),
                        self.cuvenGrep)

        self.connect(self.wCuven, SIGNAL('lostFocus()'),
                        self.cuvenRetHit)
        self.connect(self.wClear,SIGNAL("clicked()"),self.slotClear)
        self.connect(self.wRound,SIGNAL("clicked()"),self.slotRound)
        self.connect(self.wPrev,SIGNAL("clicked()"),self.slotPrev)
        self.connect(self.wNext,SIGNAL("clicked()"),self.slotNext)
        self.connect(self.wSave,SIGNAL("clicked()"),self.slotSave)
        self.connect(self.wExit,SIGNAL("clicked()"),self.slotExit)
        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)
        self.connect(self.wResc,SIGNAL("clicked()"),self.slotResc)
        self.connect(self.wLotTable,
               SIGNAL("clicked(int,int,int,const QPoint&)"), self.slotLot)
        self.connect(self.wVatCombo, SIGNAL("activated(int)"),
                     self.slotCombo)

        # Some Source per instance properties
        self._prevLen= 0
        self._lot= None
        self._lotEntry= None
        self._rescAmount= 0
        self._rescSide= ' '
        self._rescAcc= None
        self._cuven= None
        self._cuvenGrep= Model.Grep.Grep(self._cuvenL, 'name')

        self.cuvenLabel= self.wCuvenLabel.text()
        self._cuvenLots= None

    def fromSourceToWidget(self, so):
        """Makes a copy ('self._source') of the supplied source object and
        sets field values according to the source object properties.<br>
        'so': Source object.
        """
        self._source= so.copyOfSource() # Consistently operate on copies
        splits=[] # The list of splits of this source
        # Get all splits of this source
        ssplits= self._splitL.getBySource(self._source.id)
        for i in ssplits:
            splits.append(i.copyOfSplit())
        
        self.wNum.setText(self._source.ref)
        ds= string.split(self._source.date, Model.Global.getDateSep())
        ymd= QDate(int(ds[0]), int(ds[1]), int(ds[2]))
        self.wDate.setDate(ymd)

        # Get the customer/vendor of this source, if exists
        self._cuven= self._cuvenL.getBySource(self._source.id)
        if self._cuven:
            self.lotTableFill(self._cuven)
            self.wCuven.setText(self._cuven.name)
            self._lotEntry= self._lotEntryL.getBySource(self._source.id)
            self._rescSide= self._lotEntry.side
            self._lot= self._lotL.getById(self._lotEntry.lot)
        else: self.wCuven.setText(QString(''))

        # Get the text describing this transaction
        self.wCaption.setText(self._source.text)

        # And fill in the split table
        t= self.wTable
        for i in splits:
            t.insertSplit(i)
        self.wBalance.setText('')# assumes the splits are balanced
        
    def save(self, so):
        """Saves a source.<br>
        'so': The source object to save
        """
        # The reference
        so.ref= str(self.wNum.text())

        # Date
        d= self.wDate.date()
        so.date= str(Control.Global.strFromQdate(d))

        #Text
        so.text= str(self.wCaption.text())
        so.amount= '0'
        so.deleted= 'N'
        # Save the source, and implicitly get the id set if a new source
        #TODO: start database transaction here
        self._sourceL.saveEntry(so)

        # Now, save the splits
        rows= self.wTable.numRows()
        self.wTable.clearSelection()
        line= 0
        for r in range(0, rows):
            num= str(self.wTable.text(r, C.NumCol)) #Account number
            if len(num)==0: continue
            #If we edit the split may be an old or a new
            p= self.wTable.getRowSplit(r) # get the split object
            if not p:  p= Model.Split.Split() # must make a new one
            p.source= so.id 
            p.account= self._accountL.getByNum(num).id
            ad= str(self.wTable.text(r, C.DebitCol)) # debit amount
            ac= str(self.wTable.text(r, C.CreditCol)) # credit amount
            if len(ad)>0:
                p.side= 'D'
                p.amount= Model.Global.moneyToInt(ad)
            else:                    
                p.side= 'C'
                p.amount= Model.Global.moneyToInt(ac)
            p.line= line
            line= line + 1
            #p.vat= self.wTable.getVat(r) if we want to use this field some day
            p.vat= ' '
            self._splitL.saveEntry(p)
            print p
        print 'splits saved'

        # Save lot/lot entry    
        if self._cuven:
            print "self._cuven: ", self._cuven
            cuvRow= self.getRescLine() # find the cust/Vend line in table
            self._rescAmount= Model.Global.moneyToInt(
                self.wTable.getTableAmount(cuvRow)[0])
            if not self._lot:
                QMessageBox.critical(self, Model.Global.getAppName(),
                 str(self.tr("You must either select an item from the\n")) +
                 str(self.tr("lot table (for invoice payment or\n")) +
                 str(self.tr("click the resc button for a new invoice")))
            print "source save lot: ", self._lot
            if not self._lot.id: # a new lot
                self._lot.cuven= self._cuven.id
                self._lot.sourceTxt= so.text
                self._lot.sourceDate= so.date
                self._lot.sourceRef= so.ref
                self._lot.sourceAmount= self._rescAmount
                print "source save created lot: ", self._lot
            self._lotL.saveEntry(self._lot)
            
            print 'lotentry A: ', self._lotEntry
            if not self._lotEntry.lot: self._lotEntry.lot= self._lot.id 
            self._lotEntry.source= so.id
            print 'lotentry B: ', self._lotEntry
            if len(self._rescSide)<1 or self._rescSide[0] not in 'CD': #CHIDEP
                print "rescSide undefined %s"%self._rescSide
            self._lotEntry.amount= self._rescAmount
            self._lotEntry.side= self._rescSide
            self._lotEntry.year= Model.Global.getClientYear()
            self._lotEntryL.saveEntry(self._lotEntry)
            print 'lot: ', self._lot
            print 'lotentry: ', self._lotEntry
        #TODO: end transaction here

    def slotSave(self):
        """Called when user cliks Save, left to subclasses to implement.
        """
        pass

    def slotCombo(self, a):
        print "Combo activated ", a
        
    def sourceInject(self, s):
        """Called when a source is injected into the dialogue.<br>
        's': The injected Source object. Comes with the signal
        """
        self.clearSomeFields()
        self.fromSourceToWidget(s)


    def clearSomeFields(self):
        """Prepare for a new source entry.
        """
        self.blockSignals(1)
        self.wCuven.setText('')
        self.wRule.setCurrentItem(0)
        self.wNum.setText(self._sourceL.getNewRef())
        self.wCuvenLabel.setText(self.cuvenLabel)

        for row in range(0, self.wLotTable.numRows()):
            for col in range(0, self.wLotTable.numCols()):
                self.wLotTable.setText(row, col, "")
        self.wLotTable.setEnabled(0)
        self.wCaption.setText('')
        self.wBalance.setText('')
        self.wSave.setEnabled(0)
        self._cuven= None
        self._lot= None
        self._cuvenLots= None

    def setBalance(self):
        """Set the split sum to the balance field. Enable
        Save if balance is zero.
        """
        bal= self.wTable.calcBalance() # bal is int
        if bal > 0: al=QLabel.AlignLeft
        else: al= QLabel.AlignRight
        self.wBalance.setAlignment(QLabel.AlignVCenter | al)
        aBal= abs(bal)
        self.wBalance.setText(Model.Global.intToMoneyZ(aBal))
        if bal != 0:
            self.wSave.setEnabled(0)
        else:
            self.wSave.setEnabled(1)

#####  Slots for dialog buttons

    def slotClear(self):
        """Clear the content of the selected split.
        """
        print "Source.slotClear()"
        for row in range(0, self.wTable.numRows()):
            if self.wTable.isRowSelected(row):
                if self.isRescLine(row):
                    self._lot= None
                    self._lotEntry= None
                break
        self.wTable.wipeSelectedRow()

    def slotExit(self):
        """Exit this dialog.
        """
        self.done(0)

    def slotRound(self):
        """Makes a split for the rounding account. If account name
        of the last split row is not blank, only the amount field is
        changed.
        """
        last= self.wTable.numRows()-1
        diff= self.wTable.calcBalance()
        if diff != 0:
            if diff > 0: col= C.DebitCol
            else: col= C.CreditCol
            accNum= Model.Global.getAccRound()
            acc= self._accountL.getByNum(accNum)
            if self.wTable.text(last, C.NumCol).isEmpty():
                if not acc:
                    QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('Please create the rounding account first'))
                    return
                self.wTable.setText(last, C.NumCol, acc.num)
                self.wTable.setText(last, C.NameCol, acc.name)
            print "diff, last, col: ", diff, last, col
            w= self.wTable.cellWidget(last, col)
            if w: # we must write to the widget, a QLineEdit
                w.setText(Model.Global.intToMoney(abs(diff)))
            else: # we can write directly to the cell
                self.wTable.setText(last, col,
                                    Model.Global.intToMoney(abs(diff)))
        self.setBalance()


    def slotPrev(self):
        """Called when user clicks on Previous button. Left to
        subclass to implement
        """
        pass

    def slotNext(self):
        """Called when user clicks on Next button. Left to
        subclass to implement
        """
        pass

    def slotCancel(self):
        """Exits this dialogue.
        """
        self.done(0)

#### Slots for cuven-field

    def cuvenInject(self, a):
        """Called from external signal when injecting
        a customer or vendor object into the source.<br>
        'a': the cuven object entering by the signal.
        """
        if a:
            self.wCuven.blockSignals(1)
            self.wCuven.setText(a.name)
            self.wCuven.blockSignals(0)
            self._cuven= a
        self.setActiveWindow()

    def cuvenGrep(self, stxt):
        """Grep for customer/vendor name. Called for each
        character typed into the cuven-field.<br>
        'stxt': The current cuven field text
        """
        txt= str(stxt)
        s, gLen= self._cuvenGrep.grepInput(txt)
        if gLen >= 0: # A unique match not found
            #self.wCuven.blockSignals(1)
            #self.wCuven.setText(s)
            #self.wCuven.setCursorPosition(gLen)
            self._cuven= None
            #self.wCuven.blockSignals(0)
        else: # One match
            self._cuven= s # s is a cuven object instance
            self.wCuven.blockSignals(1)
            self.wCuven.setText(s.name)
            self.wCuven.blockSignals(0)
            if s.type == 'C':
                self.wCuvenLabel.setText(self.tr('Customer'))
            else:
                self.wCuvenLabel.setText(self.tr('Vendor'))
 
    def cuvenRetHit(self):
        """Slot called when cuven field lose focus.
        """
        print "cuvenRetHit self._cuven: ", self._cuven
        sn= string.strip(str(self.wCuven.text()))
        if len(sn) == 0: return # empty name
        if not self._cuven: #Unique match not found, get first in list
            self._cuven= self._cuvenGrep.getFirstMatch()
        if not self._cuven: # We had no match at all
            QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('Unknown customer/vendor'))
            return
        self.wCuven.blockSignals(1)
        self.wCuven.setText(self._cuven.name)
        self.wCuven.blockSignals(0)
        if self._cuven.type == 'C':
            self.wCuvenLabel.setText(self.tr('Customer'))
        else:
            self.wCuvenLabel.setText(self.tr('Vendor'))
        self.wResc.setEnabled(1)
        self.lotTableFill(self._cuven)
        self.wLotTable.setEnabled(1)
        
####### Slots for Rule combobox

    def slotRuleActivated(self, a):
        """Called when a rule of the rule combo chosen.<br>
        'a': The index of the chosen rule.
        """
        rule= self._ruleL[a] # look up the rule object
        splits= Model.Split.SplitList() # A split list for generated splits

        # Dialogue to let user assign values to the rule parametres
        c= Control.RuleAssign.RuleAssign(self, rule, splits)
        # Where the generated splits will fall down
        self.connect(c, PYSIGNAL('splits'), self.slotRuleSplits)
        c.show()
        ret= c.exec_loop()
        if ret != 0: # Rule was executed, set default text in field
            self.wCaption.setText(rule.text)

    def slotRuleSplits(self, retCode, splits):
        """This function called after a rule execution.<br>
        'retCode': Result of execution, 'E': error, 1 char string<br>
        'splits': List of generated splits if 'retCode'!='E'
        """
        if retCode == 'E':
            QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('An error occurred while executing rule code'))
            return
        self.wTable.wipeAll() # Clear the split table
        for i in splits: # and fill with the generated splits
            i.account= int(i.account)
            self.wTable.insertSplit(i)

##### Lots

    def slotLot(self, row, a2, a3, a4):
        """Slot called when user clicks in the list of available lots. Will
        create split text and insert the remaining balance into the split.
        """
        lot=(a2, a3, a4) #served for pychecker
        if self._cuven is None: # False alarm
            #self._lot= None
            #self._lotEntry= None
            return
        if not self.wTable.text(0, 0).isEmpty(): return #another false try

        if self._cuven.type == 'C': # We have a customer
            accNum= Model.Global.getAccCustomer()
            self._rescSide= 'C' #used when saving lotentries
            col= C.CreditCol
        else: # no, we have a vendor
            accNum= Model.Global.getAccVendor()
            col= C.DebitCol
            self._rescSide= 'D' #used when saving lotentries
        lot= self._cuvenLots[row]
        print "Clicked on lot: ", lot
        acc= self._accountL.getByNum(accNum)
        if not acc:
            QMessageBox.information(self, Model.Global.getAppName(),
                self.tr('Please create the sales/bought account first'))
            return
        self.wVatCombo.setCurrentItem(0) # we don't want any VAT here
        self.wTable.setText(0, C.NumCol, accNum)
        self.wTable.setText(0, C.NameCol, acc.name)
        self.wTable.setText(0, col, Model.Global.intToMoney(abs(lot.sum)))
        self._lot= self._lotL.getById(lot.id) # Get the relevant lot
        if not self._lotEntry:
            self._lotEntry= Model.LotEntry.LotEntry() # prep a new entry
        self.wTable.setNumRows(2) # Make a row for the next split
        self.wTable.insertItems(1)
        # disable resc button?
        self.setBalance()
        


    def slotResc(self):
        """Slot called when the Resc button clicked. Make a new Lot
        and lotentry.
        """
        if self._cuven is None: # False alarm
            #self._lot= None
            #self._lotEntry= None
            return
        self.setBalance()
        if self.wBalance.text().isEmpty(): return
        if self._cuven.type == 'C': # We have a customer
            accNum= Model.Global.getAccCustomer()
            col= C.DebitCol
            self._rescSide= 'D' #used when saving lotentries
        else: # We have a vendor here
            accNum= Model.Global.getAccVendor()
            col= C.CreditCol
            self._rescSide= 'C' #used when saving lotentries
        acc= self._accountL.getByNum(accNum)
        if not acc:
            QMessageBox.information(self, Model.Global.getAppName(),
                self.tr('Please create the sales/bought account first'))
            return
        last= self.wTable.numRows()-1 # last row in split table
        self.wTable.setText(last, C.NumCol, acc.num)
        self.wTable.setText(last, C.NameCol, acc.name)
        print "SlotResc self._lot: ", self._lot
        print "SlotResc self._lotentry: ", self._lot
        if not self._lot: self._lot= Model.Lot.Lot()
        if not self._lotEntry: self._lotEntry= Model.LotEntry.LotEntry()
        print "SlotResc self._lot 2: ", self._lot
        print "SlotResc self._lotentry 2: ", self._lot
        diff= self.wBalance.text()
        self.wTable.setText(last, col, diff)
        self.setBalance()
        

    def getRescLine(self):
        """Finds the split table line where the account number
        corresponds to a customer or vendor transaction account.<br>
        'return': row number, int. None if not found
        """
        if self._cuven.type == 'V': rAcc= Model.Global.getAccVendor()
        else: rAcc= Model.Global.getAccCustomer()
        for row in range(0, self.wTable.numRows()):
            if str(self.wTable.text(row, C.NumCol)) == rAcc:
                return row
        return None

    def isRescLine(self, row):
        """Check if a split table row's account number
        corresponds to a customer or vendor transaction account.<br>
        'return': yes: 1, no: 0, -1 row not found
        """
        if row >= self.wTable.numRows(): return -1
        vAcc= Model.Global.getAccVendor()
        cAcc= Model.Global.getAccCustomer()
        if str(self.wTable.text(row, C.NumCol)) == vAcc: return 1
        if str(self.wTable.text(row, C.NumCol)) == cAcc: return 1
        return 0

    def lotTableFill(self, cuven):
        self._cuvenLots= self._lotL.getOpenByCuven(cuven.id)
        row= 0
        t= self.wLotTable
        for i in self._cuvenLots:
            t.setNumRows(row+1)
            t.setText(row, 0, i.sourceRef)
            t.setText(row, 1, i.sourceDate)
            t.setText(row, 2, i.sourceTxt)
            t.setText(row, 3, Model.Global.intToMoney(i.sourceAmount))
            t.setText(row, 4, Model.Global.intToMoney(abs(i.sum)))
            row= row+1


#####################
#
# SourceNew class
#

class SourceNew(Source):
    """Dialogue for entering new sources.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue.
        """
        Source.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr("New Source"))
        self.wNum.setText(self._sourceL.getNewRef()) # get next ref number
        self.wNext.setEnabled(0)
        self.wPrev.setEnabled(0)
        self.wNext.hide()
        self.wPrev.hide()
        self._cuven= None
        self.connect(self.wRule,SIGNAL("activated(int)"),
                     self.slotRuleActivated)

    def slotSave(self):
        """Save the source.
        """
        so= Model.Source.Source() # We need a new object
        self.save(so) #then get the properties filled in and saved
        self.clearSomeFields() # and make ready for the next source
        self.wTable.wipeAll()
        
    def sourceInject(self, s):
        """Called from an external signal.
        Fill in the source form with properties from an other
        dialogue. Useful for using an existing source as a template.<br>
        's': The source object to inject, follows the signal.
        """
        print "sourceInject"
        if not self.isVisible(): return
        print "Injecting"
        ca= Model.Global.getAccCustomer()
        va= Model.Global.getAccVendor()
        self.clearSomeFields()
        cS= s.copyOfSource()
        self.fromSourceToWidget(cS)
        self._source.id= None # because this is a new source object
        # clear all table's split objects
        self.wTable.removeRowSplits()
        # Then remove all table entries
        #TODO: Use a smarter procedure
        rows= self.wTable.numRows()
        delRows= []
        for row in range(0, rows):
            acc= str(self.wTable.text(row, C.NumCol))
            if  acc == ca or acc == va: delRows.append(row)
        delRows.reverse()
        for row in delRows:
            self.wTable.removeRow(row)
        self.wNum.setText(self._sourceL.getNewRef())# Fill in the ref for this

#######################
#
# SourceEdit class
#

class SourceEdit(Source):
    """Dialogue to edit a source.
    """
    def __init__(self, parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue.
        """
        Source.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr("Edit Source"))
        viewList= Control.Global.getListSelected()
        so= viewList[0]
        self.fromSourceToWidget(so) # Make a copy and fill in fields
        self.wNext.setEnabled(0)
        self.wPrev.setEnabled(0)
        self.wNext.hide()
        self.wPrev.hide()
        
    def slotSave(self):
        """Save the source.
        """
        self.save(self._source)
        self.done(0)


########################
#
# SourceView class
#

class SourceView(Source):
    """Dialogue for source views.
    """
    def __init__(self, parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue. A list of selected source objects
        are stored in the global listSelected tuple.
        """
        Source.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr("View Source"))
        self._viewList= Control.Global.getListSelected()
        self._pos= len(self._viewList) -1 # Show the last source 
        self.fromSourceToWidget(self._viewList[self._pos])
        #Disable several buttons
        self.wClear.setEnabled(0)
        self.wSave.setEnabled(0)
        self.wRound.setEnabled(0)
        self.wNext.setEnabled(0)
        self.wResc.setEnabled(0)
        self.numGrep= None#Model.Grep.Grep()
        if len(self._viewList)==1:
            self.wPrev.setEnabled(0)
            self.wNext.setEnabled(0)
            
    def slotNext(self):
        """Show the next from the list of selected sources.
        """
        if (self._pos + 1) < len(self._viewList):
            self._pos= self._pos+1
            self.wTable.wipeAll()
            self.fromSourceToWidget(self._viewList[self._pos])
        self.checkLimits()
        
    def slotPrev(self):
        """Show the previous from the list of selected sources.
        """
        if self._pos > 0 :
            self._pos= self._pos-1
            self.wTable.wipeAll()
            self.fromSourceToWidget(self._viewList[self._pos])
        self.checkLimits()

    def checkLimits(self):
        """Enables the 'Next' and 'Prev' buttons when at the first and last
        element of the selected source list.
        """
        if self._pos > 0:
            self.wPrev.setEnabled(1)
        else:
            self.wPrev.setEnabled(0)
        if self._pos+1 < len(self._viewList):
            self.wNext.setEnabled(1)
        else:
            self.wNext.setEnabled(0)
            

####################
#
# SourceDelete class
#

class SourceDelete(Source):
    """Dialogue to delete sources.
    """
    def __init__(self, parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue. The source object to delete is stored
        in the global listSelected.
        """
        Source.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr("Delete Source"))
        self._viewList= Control.Global.getListSelected()
        so= self._viewList[0]
        self.fromSourceToWidget(so)
        # set up buttons
        self.wSave.setText(self.tr('Delete'))
        self.wClear.setEnabled(0)
        self.wSave.setEnabled(1)
        self.wRound.setEnabled(0)
        self.wResc.setEnabled(0)
        self.wPrev.setEnabled(0)
        self.wNext.setEnabled(0)
        self.wPrev.hide()
        self.wNext.hide()

    def slotSave(self):
        """This slot acts as a delete here: delete the source
        """
        # first, delete the source object or mark as deleted if not the
        # last source
        sid= self._source.id
        self._sourceL.deleteEntry(self._source)
        #in any case delete the splits
        spl= self._splitL.getBySource(sid)
        for s in spl:
            self._splitL.deleteEntry(s)
        # and at last possibly lot and lotentry
        lotEnt= self._lotEntryL.getBySource(sid)
        if lotEnt: # we have a lot entry
            self._lotEntryL.deleteEntry(lotEnt) # so, delete it
            lot= lotEnt.lot # when we have a lotentry we must also have a lot
            lotEnts= self._lotEntryL.getByLot(lot)# find all entries of the lot
            if len(lotEnts) == 0: # we removed our lotentry, so now empty
                tLot= self._lotL.getById(lot) # we can delete the lot ...
                self._lotL.deleteEntry(tLot)  # since no lotentries any more
        self.done(0)

