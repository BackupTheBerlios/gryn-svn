""" $Id$<br>
Shows a tree view of the account plan.<br>
Emits signal AccountSelected.
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
import Control.uTreeList
import Model.Books
import Control.Global
#import os.path

#Icons used to tag the used and unused accounts
def pmUsed(): 
    return QPixmap(Control.Global.expandImg('pmUsed.png'))

def pmUnused():
    return QPixmap(Control.Global.expandImg('pmUnused.png'))


class AccountTree(Control.uTreeList.uTreeList):
    """A dialogue with a treeview of the accont plan. The view can
    display the complete plan or only those accounts actually in use
    for this ledger.
    """
    def __init__(self, parent = None,name = None,modal = 0,fl = 0):
        """Create the dialogue instance
        """
        Control.uTreeList.uTreeList.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr('Accounts'))
        self.showHow.setText(self.tr('Only show active accounts'))
        self.accountList.header().setLabel(0,self.tr("Number"))
        self.accountList.addColumn(self.tr("Name"))
        self.accountList.clear()
        self.accountList.setRootIsDecorated(1)
        self.loadList()
        #Control.Global.setAccountTreeWindow(self)

        self.connect(self.showHow,SIGNAL("stateChanged(int)"),self.slotShowHow)
        self.connect(self.accountList, SIGNAL("clicked(QListViewItem*)"),
                     self.slotClick)
        self.connect(parent, PYSIGNAL('account'), self.accountListUpdate)

        
    def loadList(self):
        """Init the tree view with account objects from the account list.
        """
        self.accountList.clear()
        self.aL= Model.Books.getList('account')
        if self.aL==None: # CHIDEP
            print 'AccountTree: Books.accounts==None'
            return None
        for i in self.aL:
            num= string.strip(i.num)
            if len(num) == 1: # Parent (Account group heading)
                p= AccViewItem(self.accountList, None, num, i.name)
                p.setSelectable(0) # which is not selectable
            elif len(num) > 3: # Valid account number
                p= self.findParent(num)
                p=AccViewItem(p, i)
            else: continue

    def slotClick(self,a0):
        """Called when clicked an account in tree view. Emits a
        AccountSelected signal.<br>
        'a0': List view item clicked.
        """
        #Filter away clicks on items which are not valid accounts
        if a0 and len(a0.__repr__()) > 0: # is valid
            # Emit signal with the account object as parameter
            self.emit(PYSIGNAL("AccountSelected"),(a0.getAccObject(),))

    def slotShowHow(self, a0):
        """Called when user clicks on showHow button
        (all or only used accounts).<br>
        a0: button state, comes with the signal
        """
        if a0 != 0: # button is selected, show only used
            #Walk through the item list and set those used visible
            g= self.accountList.firstChild()
            while g:
                i= g.firstChild()
                while i:
                    if i.account:
                        if i.account.used=='N': i.setVisible(0)
                    else: i.setVisible(0)
                    i= i.nextSibling()
                g= g.nextSibling()
        else: # button is not selected, show all
            g= self.accountList.firstChild()
            while g:
                i= g.firstChild()
                while i:
                    if i.account: i.setVisible(1)
                    else: i.setVisible(0)
                    i= i.nextSibling()
                g= g.nextSibling()

    def findParent(self, n):
        """Find the parent list item of the account number given.<br>
        'n': The account number which parent to find, string
        """
        num= n[0] # We want the parent with account number==the first digit 
        p= self.accountList.firstChild()
        while p:
            if str(p.text(0)) == num: return p
            p= p.nextSibling()
        return None # Group not found, moral of this story: Always predefine
    # all possible headings

    def findItemById(self, id):
        """Find the object with the given id.<br>
        'id': Account number to search for
        """
        p= self.accountList.firstChild()
        while p:
            i= p.firstChild()
            while i:
                if i.account:
                    if i.account.id == id: return i
                i= i.nextSibling()
            p= p.nextSibling()
        return None
                
    def accountListUpdate(self, account, what):
        """This method is called by an external signal which indicates that
        one item in the account list has changed and therefore advices
        this object to update its view.<br>
        'account': The account object that changed<br>
        'what': ...happened?, string:  
        'E' edited, 'N' new, 'D' deleted, 'R': reread
        """
        if what == 'E':
            i= self.findItemById(account.id)
            if not i:
                return
            i.setAccObject(account)
        if what == 'N':
            p= self.findParent(account.num)
            if not p:
                return
            AccViewItem(p, account)# The treeview sorts into correct position
        if what == 'D':
            i= self.findItemById(account.id)
            if not i:
                return
            i.setAccObject(None)
            i.setVisible(0)
        if what == 'R':
            self.loadList()
            self.slotShowHow(0)
            self.showHow.setChecked(0)
            
class AccViewItem(QListViewItem):
    """This class inherits QListViewItem. Extended to keep an
    account object too.
    """

    def __init__(self, parent, acc, h1= None, h2= None):
        """Makes a new AccViewItem instance.<br>
        'acc': Account object of this item<br>
        'h1': account number<br>
        'h2': account name<br>
        h1 and h2 are only given for group headings
        """
        if not acc:
            QListViewItem.__init__(self, parent, h1, h2)
        else:
            QListViewItem.__init__(self, parent, acc.num, acc.name)
            if len(acc.num)<4: self.setSelectable(0)
            if acc.used == 'N': self.setPixmap(1, pmUnused())
            else: self.setPixmap(1, pmUsed())
        self.setVisible(1)
        self.account= acc # save the account object with self
            

    def __repr__(self):
        """String representation of this object
        """
        if not self.account:
            return ''
        return "%s"%self.account

    def setAccObject(self, acc):
        """Save account object and display number, name and icon<br>
        'acc': Account object
        """
        self.account= acc
        if acc:
            self.setText(0, acc.num)
            self.setText(1, acc.name)
            if acc.used == 'N': self.setPixmap(1, pmUnused())
            else: self.setPixmap(1, pmUsed())


    def getAccObject(self):
        """Returns the account object og this object
        """
        return self.account

    
