""" $Id$<br>
Generates Sources from input queues.
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
from qt import *
from qttable import QTable
import Control.uQueue
import Model.Books
import Model.Global
import Model.Invque
debug= sys.stderr

class Queue(Control.uQueue.uQueue):
    """Parent class of queue importer.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the queue importer
        """
        Control.uQueue.uQueue.__init__(self,parent,name,modal,fl)
        if not name:
            self.setName("Queue")

        # wTable will display the generated Sources
        self.wTable.setReadOnly(1)
        self.wTable.setSelectionMode(QTable.NoSelection)
        self.resize(QSize(600,223).expandedTo(self.minimumSizeHint()))
        

class InvoiceQueue(Queue):
    """This subclass imports invoices.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up dialogue and activate the import.
        """
        Queue.__init__(self,parent,name,modal,fl)
        self.wOK.setEnabled(0)
        t= self.wTable
        t.setNumCols(5)
        h= t.horizontalHeader()
        h.setLabel(0, self.tr('Source'))
        h.setLabel(1, self.tr('Invoice'))
        h.setLabel(2, self.tr('Date'))
        h.setLabel(3, self.tr('Amount'))
        h.setLabel(4, self.tr('Customer'))
        v= t.verticalHeader()
        v.hide()
        t.setLeftMargin(0)
        t.setColumnStretchable(0, 1)
        t.setColumnStretchable(1, 1)
        t.setColumnStretchable(2, 1)
        t.setColumnStretchable(3, 1)
        t.setColumnStretchable(4, 10)
        self.connect(self.wOK, SIGNAL('clicked()'), self.slotOK)
        queL= Model.Books.getList('invque')
        cuvenL= Model.Books.getList('cuven')
        logg= [] # The list to display in the wTable
        
        t.setNumRows(len(queL))
        queL.importInvoices(logg) # from Model.Invque. Implicitly removes
        # the que entries from the database table.
        
        # For each invoice the element in logg contains a tuple of
        # the Source, Lot and Invoice objects
        row= 0
        for i in logg:
            if i == None: break
            source, lot, invoice= i
            t.setText(row, 0, source.ref)
            t.setText(row, 1, invoice.invNum)
            t.setText(row, 2, invoice.date)
            t.setText(row, 3, Model.Global.intToMoney(lot.sourceAmount))
            t.setText(row, 4, cuvenL.getById(invoice.cuven).name)
            row= row + 1
        self.wOK.setEnabled(1)




    def slotOK(self):
        """Called when OK button clicked, close the window
        """
        self.done(1)

        
    def languageChange(self):
        """Called by translator.
        """
        self.setCaption(self.tr('Importing invoice queue'))
        self.wOK.setText(self.tr("OK"))


