""" $Id$<br>
Dialogue to show a tree view of customers/vendors.
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


#TODO: Implement view update from external signal

from qt import *
import Control.uTreeList
import Model.Books
import Control.Global



class CuvenTree(Control.uTreeList.uTreeList):
    """This dialogue shows groups of customer/vendors in a treeview.
    Customer/vendors can appear in several such groups.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue instance.
        """
        Control.uTreeList.uTreeList.__init__(self,parent,name,modal,fl)
        #self._type= None
        self.cuvenList= self.accountList #fix this when uTreeList is fixed
        if not name:
            self.setName("CuvenTree")

        # We inherit a class where the tree view widget is called accountList
        # Maybe fix this to give the widget a neutral name... 
        self.accountList.header().setLabel(0,self.tr("Number"))
        self.accountList.addColumn(self.tr("Name"))
        self.accountList.setRootIsDecorated(1)

        self._cuvenL= Model.Books.getList('cuven')
        self.accountList.clear()
        self.loadList()
            
        self.connect(self.showHow,SIGNAL("stateChanged(int)"),self.slotShowHow)
        self.connect(self.accountList, SIGNAL("clicked(QListViewItem*)"),
                     self.slotClick)
        self.connect(parent, PYSIGNAL('cuven'), self.cuvenListUpdate)

    def slotShowHow(self):
        """Called when showHow button clicked. Not implemented
        """
        # See AccountTree for implementation 
        pass

    def slotClick(self,a0):
        """Called when user clicks a tree item.
        """
        pass

    def findParents(self, cClass):
        """Find the parent list item of the class number given.<br>
        'cClass': The class number which parent to find, int. The class is a
        bitfield, so several parents may be found. This function is
        presently only implemented for one class
        """
        pList= []
        # We want the parents with correct class bits 
        p= self.accountList.firstChild()
        pList.append(p)
        return pList # only one parent implemented yet
        #while p:
        #    if p.cls & cClass != 0: pList.append(p)
        #    p= p.nextSibling()
        #if len(pList) == 0: return None
        #return pList

    def findItemsById(self, id):
        """Find the object with the given id.<br>
        'id': Account number to search for
        """
        oL= []
        p= self.cuvenList.firstChild()
        while p:
            i= p.firstChild()
            while i:
                if i._cuven:
                    if i._cuven.id == id: oL.append(i)
                i= i.nextSibling()
            p= p.nextSibling()
        if len(oL) == 0: return None
        return oL

    def cuvenListUpdate(self, cuven, what):
        """Called from an external signal meaning a vendor object
        has changed. We want to update the object view here.
        A cuven can sit several places in the tree if it belongs to more than
        one group.<br>
        'cuven': The altered cuven object<br>
        'what': happened. 
        'E' edited, 'N' new, 'D' delted, 'R': reread
        """
        if cuven.type != self._type: return
        if what == 'E':
            iList= self.findItemsById(cuven.id)
            if not iList:
                return
            for i in iList: i.setCuvenObject(cuven)
        if what == 'N':
            pList= self.findParents(cuven.cls)
            if not pList:
                return
            for p in pList: CuvenViewItem(p, cuven)# The treeview sorts into
                                                   #correct position
        if what == 'D':
            iList= self.findItemsById(cuven.id)
            if not iList:
                return
            for i in iList:
                i.setCuvenObject(None)
                i.setVisible(0)
        if what == 'R':
            self.loadList()
            self.slotShowHow(0)
            self.showHow.setChecked(0)
            

    def loadList(self): #probably move this to subclasses
        if self._cuvenL==None: #CHIDEP
            print 'CuvenTree: Books.cuven==None'
            return None
        #we need to set class bit for each parent, not implemented
        p= CuvenViewItem(self.cuvenList, None, 'All') 
        p.setSelectable(0)
        for i in self._cuvenL:
            print "CuvenL: ", i, i.type, self._type
            if i.type == self._type: 
                CuvenViewItem(p, i)
        # add other groups below. We need some way to specify the groups
        # in a config file and arrange the cuvens in the groups according
        # to their cls-property


class CustomerTree(CuvenTree):
    """Dialogue to view customers in a tree. Inherits CuvenTree.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue.
        """
        self._type= 'C'
        CuvenTree.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr('Customers'))
        self.showHow.setText(self.tr('Only show active customers'))
        #Control.Global.setCustomerTreeWindow(self)

    def slotClick(self,a0):
        """Called when user clicks on a tree item.<br>
        'a0': item clicked, supplied with the signal.
        """
        if a0 and len(a0.__repr__()) > 0: #check if spurious
            self.emit(PYSIGNAL("CustomerSelected"),(a0._cuven,)) #OK

class VendorTree(CuvenTree):
    """Dialogue to view vendorss in a tree. Inherits CuvenTree.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue.
        """
        self._type= 'V'
        CuvenTree.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr('Vendors'))
        self.showHow.setText(self.tr('Only show active vendors'))
        #Control.Global.setVendorTreeWindow(self)

    def slotClick(self,a0):
        """Called when user clicks on a tree item.<br>
        'a0': item clicked, supplied with the signal.
        """
        if a0 and len(a0.__repr__()) > 0:
            self.emit(PYSIGNAL("VendorSelected"),(a0._cuven,))

    
class CuvenViewItem(QListViewItem):
    """An QListViewItem extended with a propert to hold the
    corresponding cuven-object.
    """

    def __init__(self, parent, cuven, h1= None, h2= None):
        """Init the item.<br>
        'cuven': The cuven object<br>
        'h1': Column 1 entry, string<br>
        'h2': Column 2 entry, string<br>
        If 'cuven' is given: use cuven number and name. Else use 'h1' and 'h2'.
        'h1' and 'h2' are used for group headings.
        """
        if not cuven:
            QListViewItem.__init__(self, parent, h1, h2)
            self.setSelectable(0)
            #Must somehow set the class of this parent
        else:
            QListViewItem.__init__(self, parent, cuven.num, cuven.name)
            self.setSelectable(1)
        self.setVisible(1)
        self._cuven= cuven
        print "CuvenViewItem: ", self._cuven
            

    def __repr__(self):
        if not self._cuven:
            return ''
        return "%s"%self._cuven


    def setCuvenObject(self, cuven):
        """Save cuven object and display number and name<br>
        'cuven': Cuven object
        """
        self._cuven= cuven
        if cuven:
            self.setText(0, cuven.num)
            self.setText(1, cuven.name)

    def getCuvenObject(self):
        """Returns the cuven object og this object
        """
        return self._cuven

