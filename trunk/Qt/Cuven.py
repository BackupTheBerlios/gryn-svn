""" $Id$<br>
Dialogues to create and maintain customer and vendor objects.
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
import Model.Global
import Model.Books
import Control.uCuven
import Control.Global


class Cuven(Control.uCuven.uCuven):
    """Customer and vendor dialogue class
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Create a new customer/vendor object instance.
        """
        Control.uCuven.uCuven.__init__(self,parent,name,modal,fl)
        if not name:
            self.setName("Cuven")
        self._type= None # Type is customer or vendor
        self._cuvenL= None
        self.emsg= None

    def blankFields(self):
        """Get next customer/vendor number and clear name and balance
        fields.
        """
        self.wNumber.setText(self._cuvenL.getNextNumber(self._type))
        self.wName.setText(QString(''))
        self.wRegno.setText(QString(''))

    def slotCancel(self):
        """Called when Cancel button clicked
        """
        self.done(0)


class CuvenNew(Cuven):
    """Dialogue for making a new customer/vendor.
    """
    def __init__(self, parent= None, name= None, modal= 0, fl= 0):
        Cuven.__init__(self,parent,name,modal,fl)
        self._cuvenL= Model.Books.getList('cuven')

    def slotSave(self):
        """Save the new client object.
        """
        o= Model.Cuven.Cuven() # new instance
        o.num= str(self.wNumber.text())
        o.name= str(self.wName.text())
        o.cls= self.wGroup.currentItem()
        o.regno= str(self.wRegno.text())
        o.type= self._type
        if len(o.name) < 1 :
            e= self.tr("No name given")
            QMessageBox.information(self, Model.Global.getAppName(), e)
            return
        if len(o.regno) < 1 :
            e= self.tr("No reg number given")
            QMessageBox.information(self, Model.Global.getAppName(), e)
            return
        self._cuvenL.saveEntry(o)
        self.blankFields()
        self.emit(PYSIGNAL('cuven'), (o, 'N'))
        self.done(1)
        
class CustomerNew(CuvenNew):
    """Dialogue to make a new customer. Inherits CuvenNew
    """
    def __init__(self, parent= None, name= None, modal= 0, fl= 0):
        """Make the new dialogue instance.
        """
        CuvenNew.__init__(self,parent,name,modal,fl)
        self.wNumber.setText(self._cuvenL.getNextNumber('C'))
        self._type= 'C'
        self.setCaption(self.tr('New customer'))
        
class VendorNew(CuvenNew):
    """Dialogue to make a new vendor. Inherits CuvenNew
    """
    def __init__(self, parent= None, name= None, modal= 0, fl= 0):
        """Make the new vendor object instance.
        """
        CuvenNew.__init__(self,parent,name,modal,fl)
        self.wNumber.setText(self._cuvenL.getNextNumber('V'))
        self._type= 'V'
        self.setCaption(self.tr('New vendor'))
        

class CuvenEdit(Cuven):
    """Dialogue to edit the properties of a customer/vendor.
    """
    def __init__(self, parent= None, cL= None):
        """Make dialogue instance.<br>
        'cL': A list of customers/vendors. If None: use client's cuven-list.
        """
        Cuven.__init__(self,parent,None,0,0)
        if cL == None: self._cuvenL= Model.Books.getList('cuven')
        else: self._cuvenL= cL

    def initFields(self):
        """Set up the dialogue fields.
        """
        eo= Control.Global.getListSelected()[0]
        self._o= eo.copyOfCuven() # Edit on a copy
        self.initCombo()
        self.wNumber.setText(self._o.num)
        self.wName.setText(self._o.name)
        self.wRegno.setText(self._o.regno)

    def slotSave(self):
        """Save the edited object. Called when user clicks Save button.
        """
        self._o.num= string.strip(str(self.wNumber.text()))
        self._o.name= string.strip(str(self.wName.text()))
        self._o.cls= self.wGroup.currentItem()
        self._o.regno= self.wRegno.text()
        if len(self._o.name) < 1 :
            e= self.tr("No name given")
            QMessageBox.information(self, Model.Global.getAppName(), e)
            return
        if len(self._o.regno) < 1 :
            e= self.tr("No reg number given")
            QMessageBox.information(self, Model.Global.getAppName(), e)
            return
        res= self._cuvenL.saveIfChanged(self._o)
        if res != 0: # changed and saved, tell the world
            self.emit(PYSIGNAL('cuven'), (self._o, 'E'))
        self.done(1)

    def initCombo(self):
        """Set up the combo boxe.
        """
        pass
    
class CustomerEdit(CuvenEdit):
    """Dialogue for editing cusomer properies. Inherits CuvenEdit.
    """
    def __init__(self, parent= None, name= None, modal= 0, fl= 0):
        """Set up dialogue.
        """
        CuvenEdit.__init__(self,parent)
        self.wNumber.setText(self._cuvenL.getNextNumber('C'))
        self._type= 'C'
        self.setCaption(self.tr('Edit customer'))
        self.initFields()
        
class VendorEdit(CuvenEdit):
    """Dialogue for editing vendor properies. Inherits CuvenEdit.
    """
    def __init__(self, parent= None, name= None, modal= 0, fl= 0):
        CuvenEdit.__init__(self,parent)
        self.wNumber.setText(self._cuvenL.getNextNumber('V'))
        self._type= 'V'
        self.setCaption(self.tr('Edit vendor'))
        self.initFields()
        
class CuvenDelete(Cuven):
    """Dialogue to delete customer/vendors.
    """
    def __init__(self, parent= None, cL= None):
        """Set up dialogue. Use list of cuvens cL. If None: use cuven
        list from model.
        """
        Cuven.__init__(self,parent,None,0,0)
        if cL == None: self._cuvenL= Model.Books.getList('cuven')
        else: self._cuvenL= cL
        self.initFields()
                        
    def initFields(self):
        """Set up and enable dialogue fields.
        """
        self._o= Control.Global.getListSelected()[0]
        self.initCombo()
        self.wNumber.setText(self._o.num)
        self.wName.setText(self._o.name)
        self.wRegno.setText(self._o.regno)
        self.wNumber.setEnabled(0)
        self.wName.setEnabled(0)
        self.wRegno.setEnabled(0)
        self.wGroup.setEnabled(0)
        self.wSave.setText(self.tr('Delete'))

    def initCombo(self):
        """Set up the items of the combo.
        """
        pass

    def slotSave(self):
        """Delete the customer/vendor, decline if in use).
        """
        if self._cuvenL.deleteEntry(self._o) != 0:
            QMessageBox.information(self, Model.Global.getAppName(), self.emsg)
            return
        self.emit(PYSIGNAL('cuven'), (self._o, 'D'))
        self.done(1)

class CustomerDelete(CuvenDelete):
    """Dialogue to delete a customer. Inherits CuvenDelete.
    """
    def __init__(self, parent=None, cL= None):
        """Set up the dialogue.
        """
        self._type= 'C'
        CuvenDelete.__init__(self, parent, cL)
        self.setCaption(self.tr('Delete customer'))
        self.emsg= self.tr('This customer is active and cannot be deleted')

class VendorDelete(CuvenDelete):
    """Dialogue to delete a vendor. Inherits CuvenDelete.
    """
    def __init__(self, parent=None, cL= None):
        """Set up the dialogue.
        """
        self._type= 'V'
        CuvenDelete.__init__(self, parent, cL)
        self.setCaption(self.tr('Delete vendor'))
        self.emsg= self.tr('This vendor is active and cannot be deleted')

