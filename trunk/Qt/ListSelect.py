"""$Id$<br>
List objects in a dialogue and allows the user to select one or more of them.
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
from qttable import QTable
import Model.Books
import Control.Global

#Icon that can be used to mark deleted items (not used now)
_deleted=[
"10 10 2 1",
"# c #ff0000",
". c #ffffff",
"#........#",
".#......#.",
"..#....#..",
"...#..#...",
"....##....",
"....##....",
"...#..#...",
"..#....#..",
".#......#.",
"#........#"]


class ListSelect(QDialog):
    """A dialogue that lists objects in a table
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue
        """
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ListSelect")

        # Maybe take the font properties from Model.Global
        f = QFont(self.font())
        f.setFamily("Adobe Helvetica")
        f.setPointSize(12)
        self.setFont(f)

        ListSelectLayout = QVBoxLayout(self,11,6,"ListSelectLayout")

        self.sTable = MTable(self,"sTable") # MTable defined below
        self.sTable.setNumRows(0)
        self.sTable.setNumCols(0)
        self.sTable.setReadOnly(1)
        self.sTable.setSelectionMode(MTable.SingleRow)
        self.sTable.setFocusStyle(MTable.SpreadSheet)
        self.sTable.selectRow(0)
        ListSelectLayout.addWidget(self.sTable)


        layout30 = QHBoxLayout(None,0,6,"layout30")

        self.wAll = QPushButton(self,"wAll")
        self.wAll.setAutoDefault(0)
        self.wAll.setDefault(0)
        layout30.addWidget(self.wAll)

        self.wInvert = QPushButton(self,"wInvert")
        self.wInvert.setAutoDefault(0)
        layout30.addWidget(self.wInvert)

        spacer = QSpacerItem(51,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout30.addItem(spacer)

        ListSelectLayout.addLayout(layout30)


        layout1 = QHBoxLayout(None,0,6,"layout1")
        spacer = QSpacerItem(121,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout1.addItem(spacer)

        self.wOK = QPushButton(self, "wOK")
        layout1.addWidget(self.wOK)

        self.wCancel = QPushButton(self, "wCancel")
        layout1.addWidget(self.wCancel)

        ListSelectLayout.addLayout(layout1)

        self.languageChange()
        self.resize(QSize(240,480).expandedTo(self.minimumSizeHint()))

        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)

        self.connect(self.sTable,
                     SIGNAL("clicked(int, int, int, const QPoint &)"),
                     self.tableClick)
        
        self.connect(self.wOK, SIGNAL("clicked()"), self.slotOk)
        self.wOK.setEnabled(0)
        self.connect(self.wAll, SIGNAL('clicked()'), self.selectAll)
        self.connect(self.wInvert, SIGNAL('clicked()'), self.invert)
        self._objects= []
        
    def languageChange(self):
        """Called by the translator.
        """
        self.setCaption(self.tr("Select one"))
        self.wCancel.setText(self.tr("Cancel"))
        self.wOK.setText(self.tr("OK"))
        self.wAll.setText(self.tr("All"))
        self.wInvert.setText(self.tr("Invert"))

    def tableClick(self, a0, a1, a2, a3):
        """Called when user clicks the table. Enables the OK-button
        """
        self.wOK.setEnabled(1)

    def slotCancel(self):
        """Returns without a selection. Called when user clicks Cancel.
        """
        Control.Global.setListSelected([])
        self.done(self.Rejected)

    def slotOk(self):
        """Save the selected objects in the global ListSelected.
        """
        r= self.sTable.grabSelected(self._objects)
        if len(r) == 0: return #This cannot happen?
        Control.Global.setListSelected(r)
        self.done(1)

    def selectAll(self):
        """Selects all items. Called from the All button click
        """
        self.sTable.selectAll()
        self.wOK.setEnabled(1)

    def invert(self):
        """Inverts the selection, called from Invert button click.
        """
        self.sTable.invertSelection()

    def hideButtons(self):
        """Hides invert and all buttons when not multiselect
        """
        self.wInvert.hide()
        self.wAll.hide()

class SourceSelect(ListSelect):
    """Subclass to select Source objects
    """
    def __init__(self,parent = None, sourceL= None, multiSel=0):
        """Set up the dialogue.<br>
        'sourceL': List of Source objects to show, use global list if None<br>
        'MultiSel': Enables multiselect if 1, single select if 0
        """
        ListSelect.__init__(self,parent,None,0, 0)
        if multiSel == 0: self.hideButtons()
        self.setCaption(self.tr("Select source"))
        self.resize(QSize(480,480).expandedTo(self.minimumSizeHint()))
        cuvenL= Model.Books.getList('cuven')
        t= self.sTable
        t.setNumCols(4)
        h= t.horizontalHeader()
        nt= self.tr('Number')
        h.setLabel(0, nt)
        h.setLabel(1, self.tr('Date'))
        h.setLabel(2, self.tr('Caption'))
        h.setLabel(3, self.tr('Cust/Vendor'))
        v= t.verticalHeader()
        v.hide()
        fm= self.fontMetrics()
        w1= fm.width('01.02.2003X')
        w2= fm.width(str(nt)+'0')
        t.setLeftMargin(0)
        t.setColumnWidth(0, w2)
        t.setColumnWidth(1, w1)
        t.setColumnStretchable(2, 1)
        t.setColumnStretchable(3, 1)
        if multiSel==0: t.setSelectionMode(MTable.SingleRow)
        else: t.setSelectionMode(MTable.MultiRow)
        if sourceL is None: sourceL= Model.Books.getList('source')

        row= 0
        for i in sourceL:
            t.setNumRows(row+1)
            t.setText(row, 0, i.ref)
            if i.deleted == 'Y':
                t.setPixmap(row, 0, QPixmap(_deleted))
            t.setText(row, 1, i.date)
            t.setText(row, 2, i.text)
            cuven= cuvenL.getBySource(i.id)
            if cuven:
                t.setText(row, 3, '%s'%cuven.name)
            else:
                t.setText(row, 3, '')
            self._objects.append((i, t.item(row, 0)))
            row= row+1

class SourceFindSelect(SourceSelect):
    """Displays a list of found objects. Inherits SourceSelect,
    quite like, but emits a 'source' signal when clicked,
    """
    def __init__(self,parent = None, sourceL= None, multiSel=0):
        """Set up the dialogue.<br>
        'sourceL': List of Source objects to show, use global list if None<br>
        'MultiSel': Enables multiselect if 1, single select if 0
        """
        SourceSelect.__init__(self, parent, sourceL, multiSel)
        self.wOK.setEnabled(1)

    def tableClick(self, row, col, a2, a3):
        """Called by table click, emits signal 'source' with
        the clicked object asparameter.
        """
        r= self.sTable.grabSelected(self._objects)[0]
        print 'selected: ', r
        self.emit(PYSIGNAL("source"),(r,))



class ClientSelect(ListSelect):
    """Dialogue to show a list of clients the user can select from
    """
    def __init__(self, parent = None, clientL= None,  multiSel=0):
        """Set up the dialogue.<br>
        'clientL': List of Client objects to show, use global list if None<br>
        'MultiSel': Enables multiselect if 1, single select if 0
        """
        ListSelect.__init__(self,parent,None, 0, 0)
        if multiSel == 0: self.hideButtons()
        self.setCaption(self.tr("Select client"))
        self.resize(QSize(480, 200).expandedTo(self.minimumSizeHint()))
        t= self.sTable
        t.setNumCols(3)
        h= t.horizontalHeader()
        nt= str(self.tr('Year  '))
        h.setLabel(0, nt)
        h.setLabel(1, self.tr('Client'))
        h.setLabel(2, self.tr('Database'))
        v= t.verticalHeader()
        v.hide()
        fm= self.fontMetrics()
        w2= fm.width('0000000')
        t.setLeftMargin(0)
        t.setColumnWidth(0, w2)
        t.setColumnStretchable(1, 1)
        t.setColumnStretchable(2, 1)
        if multiSel==0: t.setSelectionMode(MTable.SingleRow)
        else: t.setSelectionMode(MTable.MultiRow)
        if clientL is None: clientL= Model.Books.getList('client')
        row= 0
        for i in clientL:
            t.setNumRows(row+1)
            t.setText(row, 0, i.year)
            t.setText(row, 1, i.name)
            t.setText(row, 2, '%s'%Model.Global.makeDbName(i.id))
            self._objects.append((i, t.item(row, 0)))
            row= row+1

class RuleSelect(ListSelect):
    """Dialogue to show a list of rules the user can select from
    """
    def __init__(self, parent = None, ruleL= None,  multiSel=0):
        """Set up the dialogue.<br>
        'ruleL': List of Client objects to show, use global list if None<br>
        'MultiSel': Enables multiselect if 1, single select if 0
        """
        ListSelect.__init__(self,parent,None, 0, 0)
        if multiSel == 0: self.hideButtons()
        self.setCaption(self.tr("Select rule"))
        self.resize(QSize(480, 200).expandedTo(self.minimumSizeHint()))
        t= self.sTable
        t.setNumCols(1)
        t.setLeftMargin(0)
        h= t.horizontalHeader()
        h.setLabel(0, self.tr('Rule'))
        v= t.verticalHeader()
        v.hide()
        t.setColumnStretchable(0, 1)
        if multiSel==0: t.setSelectionMode(MTable.SingleRow)
        else: t.setSelectionMode(MTable.MultiRow)
        if ruleL is None: ruleL= Model.Books.getList('rule')
        row= 0
        for i in ruleL:
            t.setNumRows(row+1)
            t.setText(row, 0, i.name)
            self._objects.append((i, t.item(row, 0)))
            row= row+1

            
class LotSelect(ListSelect):
    """Dialogue to show a list of Lots
    the user can select from.
    """
    def __init__(self, parent = None, lotL= None,  multiSel=0):
        """Set up the dialogue.<br>
        'lotL': List of  Lot objects to show, use global list if None<br>
        'MultiSel': Enables multiselect if 1, single select if 0
        """
        ListSelect.__init__(self,parent,None, 0, 0)
        if multiSel == 0: self.hideButtons()
        self.setCaption(self.tr("Select rescontro entry"))
        self.resize(QSize(480,100).expandedTo(self.minimumSizeHint()))
        t= self.sTable
        t.setNumCols(6)
        h= t.horizontalHeader()
        fm= self.fontMetrics()
        wRef= fm.width('12345 ')
        wDate= fm.width('12-34-56000')
        wMoney= fm.width('123456789,00 ')
        t.setLeftMargin(0)
        t.setColumnWidth(0, wRef)
        t.setColumnWidth(1, wDate)
        t.setColumnStretchable(2, 1)
        t.setColumnWidth(3, wMoney)
        t.setColumnWidth(4, wMoney)

        h.setLabel(0, self.tr('Ref'))
        h.setLabel(1, self.tr('Date'))
        h.setLabel(2, self.tr('Caption'))
        h.setLabel(3, self.tr('Amount'))
        h.setLabel(4, self.tr('Remaining'))
        v= t.verticalHeader()
        v.hide()
        t.hideColumn(5)
        if multiSel==0: t.setSelectionMode(MTable.SingleRow)
        else: t.setSelectionMode(MTable.MultiRow)
        if lotL is None: lotL= Model.Books.getList('lot')
        row= 0
        for i in lotL:
            t.setNumRows(row+1)
            t.setText(row, 0, i[0])
            t.setText(row, 1, i[2])
            t.setText(row, 2, i[1])
            t.setText(row, 3, i[3])
            t.setText(row, 4, i[4])
            t.setText(row, 5, i[5])
            self._objects.append((i, t.item(row, 0)))
            row= row+1


class CuvenSelect(ListSelect):
    """Dialogue to show a list of Cuvens
    the user can select from.
    """
    def __init__(self, parent = None, cuvenL= None,  multiSel=0):
        """Set up the dialogue.<br>
        'cuvenL': List of  Lot objects to show, use global list if None<br>
        'MultiSel': Enables multiselect if 1, single select if 0
        """
        ListSelect.__init__(self,parent,None, 0, 0)
        if multiSel == 0: self.hideButtons()
        self.setCaption(self.tr("Select customer/vendor"))
        self.resize(QSize(480,480).expandedTo(self.minimumSizeHint()))
        t= self.sTable
        t.setNumCols(3)
        h= t.horizontalHeader()
        nt= self.tr('Number  ')
        h.setLabel(0, nt)
        h.setLabel(1, self.tr('Customer/vendor'))
        h.setLabel(2, self.tr('Balance'))
        v= t.verticalHeader()
        v.hide()
        fm= self.fontMetrics()
        w0= fm.width(nt)
        w2= fm.width('00.000.000.00 ')
        t.setLeftMargin(0)
        t.setColumnWidth(0, w0)
        t.setColumnStretchable(1, 1)
        t.setColumnWidth(2, w2)
        if multiSel==0: t.setSelectionMode(MTable.SingleRow)
        else: t.setSelectionMode(MTable.MultiRow)
        if cuvenL is None: cL= Model.Books.getList('cuven')

class CustomerSelect(CuvenSelect):
    """Dialogue to show a list of Customers
    the user can select from.
    """
    def __init__(self, parent = None, custL= None,  multiSel=0):
        """Set up the dialogue.<br>
        'custL': List of  cuven objects to show, use global list if None<br>
        'MultiSel': Enables multiselect if 1, single select if 0
        """
        CuvenSelect.__init__(self,parent, custL, multiSel)
        if multiSel == 0: self.hideButtons()
        self.setCaption(self.tr("Select customer"))
        t= self.sTable
        h= t.horizontalHeader()
        h.setLabel(1, self.tr('Customer'))
        row= 0
        for i in custL:
            if i.type != 'C': continue
            balance= custL.balance(i)
            t.setNumRows(row+1)
            t.setText(row, 0, i.num)
            t.setText(row, 1, i.name)
            if balance != None:
                t.setText(row, 2, Model.Global.intToMoneyZ(balance))
            else:
                t.setText(row, 2, '')                
            self._objects.append((i, t.item(row, 0)))
            row= row+1

class VendorSelect(CuvenSelect):
    """Dialogue to show a list of vendors
    the user can select from.
    """
    def __init__(self, parent = None, vendorL= None,  multiSel=0):
        """Set up the dialogue.<br>
        'cuvenL': List of vendor objects to show, use global list if None<br>
        'MultiSel': Enables multiselect if 1, single select if 0
        """
        CuvenSelect.__init__(self, parent, vendorL, multiSel)
        if multiSel == 0: self.hideButtons()
        self.setCaption(self.tr("Select vendor"))
        t= self.sTable
        h= t.horizontalHeader()
        h.setLabel(1, self.tr('Vendor'))
        row= 0
        for i in vendorL:
            if i.type != 'V': continue
            balance= vendorL.balance(i)
            t.setNumRows(row+1)
            t.setText(row, 0, i.num)
            t.setText(row, 1, i.name)
            if balance != None:
                t.setText(row, 2, Model.Global.intToMoneyZ(balance))
            else:
                t.setText(row, 2, '')                
            self._objects.append((i, t.item(row, 0)))
            row= row+1
        
        
class MTable(QTable):
    """A QTable with some column sort added
    """
    def __init__(self, parent, name):
        """Set up the table, sort direction 0
        """
        QTable.__init__(self, parent, name)
        self._dir=0
        
    def columnClicked(self, col):
        """Called when table column head clicked. Sorts and inverts
        sort direction of this column.<br>
        'col': The column to sort by, supplied with signal
        """
        self.sortColumn(col, self._dir, 1)
        if self._dir==0: self._dir= 1
        else: self._dir= 0

    def selectAll(self):
        """Called when user clicks SelectAll button.
        """
        for r in range(0, self.numRows()):
            self.selectRow(r)

    def invertSelection(self):
        """Called when user clicks Invert button.
        """
        items= []
        for r in range(0, self.numRows()):
            if not self.isRowSelected(r):
                items.append(r)
        self.clearSelection(1)
        for r in items:
            self.selectRow(r)

    def grabSelected(self, objects):
        """Collects the selected objects into a list.<br>
        'objects': list of all objects<br>
        'return': list of the selected objects
        """
        r= []
        # Due to possible sorting the object list is not in the same order
        # as the table items. We thus have to search for the objects.
        # TODO: Subclass TableItem to also hold the object
        for row in range(0, self.numRows()):
            for o in objects:
                if self.item(row, 0) is o[1]:
                    if self.isRowSelected(row) != 0: r.append(o[0])
                    break
        return r

        
