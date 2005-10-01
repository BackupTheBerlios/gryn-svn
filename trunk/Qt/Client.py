""" $Id$<br>
Dialogues to create and maintain clients.<br>
Emits signal 'client'
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
import os
import time
from qt import *
import Control.uClientEditNew
import Model.Client
import Model.Books
import Model.Global
import Model.Exceptions
import Model.AccountImport
import Control.Global

# Some error messages
e= {'Name':QT_TRANSLATE_NOOP('err','Client name too short.'),
    'RegNum':QT_TRANSLATE_NOOP('err','Registration number too short.'),
    'FirstEntry':QT_TRANSLATE_NOOP('err',
    'First journal entry must be a number and larger than 0.')
}

def initCombos(obj):
    """Set up the como boxes of this dialogue<br>
    'obj': The form of this dialogue.
    """
    obj.periodes.insertItem('1') #Number of periodes of the year
    obj.periodes.insertItem('2')
    obj.periodes.insertItem('3')
    obj.periodes.insertItem('4')
    obj.periodes.insertItem('6')
    obj.periodes.insertItem('12')
    obj.dimension.insertItem('0') #Dimensions are not implemented yet
    obj.dimension.insertItem('1')
    obj.dimension.insertItem('2')
    obj.dimension.insertItem('3')
    path= Model.Global.getVarPath()
    files= os.listdir(path)
    # All account plan files
    for file in files:                     
        if string.find(file, '.gapl') > 0:
            fn= string.split(file, '.')
            obj.accPlan.insertItem(fn[0])
    # All VAT files
    for file in files:
        if string.find(file, '.vat') > 0:
            fn= string.split(file, '.')
            obj.vatFile.insertItem(fn[0])

def initFields(obj, o):
    """Set up the fields of the dialogue<br>
    'obj': The form of this dialogue<br>
    'o': The client object
    """
    obj.clients.clear()
    obj.clients.insertItem(o.name)
    obj.year.setValue(int(o.year))
    obj.regNum.setText(o.regNum)
    obj.firstEntry.setText(o.firstEntry)
    obj.periodes.setCurrentText(o.periodes)
    obj.dimension.setCurrentText(o.dimension)
    if o.budget=='Y': obj.budget.setChecked(1)
    else: obj.budget.setChecked(0)
    if o.vat=='Y': obj.vat.setChecked(1)
    else: obj.vat.setChecked(0)



    
class ClientEdit(Control.uClientEditNew.uClientEditNew):
    """A class to edit some properies of an existing client
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Create a new dialogue instance. Assume the client object
        is placed in Control.Global.ListSelected[0]
        """
        Control.uClientEditNew.uClientEditNew.__init__(self,parent,name,
                                                       modal,fl)
        
        clientL= Model.Global.getClientList() 
        c= Control.Global.getListSelected()[0]
        #initCombos(self)
        self._o= c.copyOfClient()# Edit a copy in case the user Cancels
        initFields(self, self._o)
        # Enable the fields we can change for an existing ledger
        self.clients.setEditable(1)
        self.regNum.setEnabled(1)
        self.vat.setEnabled(0)
        self.firstEntry.setEnabled(0)
        self.periodes.setEnabled(0)
        self.budget.setEnabled(1)
        self.dimension.setEnabled(1)
        self.year.setEnabled(0)

    def slotSave(self):
        """Make an object from the fields and save
        """
        try:
            # Commented statements are for pars not available for editing now
            self._o.name= string.strip(str(self.clients.currentText()))
            #self._o.year= "%s"%self.year.value()
            self._o.regNum= string.strip(str(self.regNum.text()))
            #if self.vat.isChecked(): self._o.vat= 'Y'
            #else: self._o.vat= 'N'
            #self._o.firstEntry= self.firstEntry.text()
            self._o.periodes= string.strip(str(self.periodes.currentText()))
            if self.budget.isChecked(): self._o.budget= 'Y'
            else: self._o.budget= 'N'
            self._o.dimension= string.strip(str(self.dimension.currentText()))
            #self._o.vat= 'Y'
        except Model.Exceptions.VarLimit, s: # parameter out of range
            try: # if error message exists
                m= str(self.tr(e[s[1]]))
            except KeyError: # did not
                m= str(self.tr("Error text for '%s' is not defined"))%s[1]
            msg= m + str(self.tr('\nPlease fix,\nThis client was not saved.'))
            QMessageBox.information(self, Model.Global.getAppName(), msg)
            return # give a chance to fix
        cl= Model.Global.getClientList()
        if cl.saveIfChanged(self._o) != 0:
            self.emit(PYSIGNAL("client"),(self._o, 'E')) # Tell the world
        self.done(1)

        
    def slotCancel(self):
        """Called when the user clicks the Cancel button
        """
        self.done(0)
        
    def slotClientSelected(self, nameYear):
        pass


class ClientDelete(Control.uClientEditNew.uClientEditNew):
    """A dialogue for removal of a client
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Create a new delete dialogue instance. The client object
        sits in Control.Global.listSelected[0]
        """
        Control.uClientEditNew.uClientEditNew.__init__(self,parent,name,
                                                       modal,fl)
        
        self._o= Control.Global.getListSelected()[0]# the client (object) to
                                                    #delete
        self._clientL= Model.Global.getClientList()

        self._db= Model.Global.makeDbName(self._o.id)
        #initCombos(self)
        initFields(self, self._o)
        self.clients.setEditable(0)
        self.setCaption(self.tr("Delete client"))
        self.accPlan.clear()
        # Disable field edits
        self.regNum.setEnabled(0)
        self.firstEntry.setEnabled(0)
        self.periodes.setEnabled(0)
        self.budget.setEnabled(0)
        self.dimension.setEnabled(0)
        self.vat.setEnabled(0)
        self.year.setEnabled(0)
        self.pbSave.setText(self.tr('Delete'))

    def slotSave(self):
        """Delete the chosen client. This removes the entry in the
        client database, but also removes all the client's books.
        Called when Delete button clicked.
        """
        conn= Model.Global.getClientConnection()
        ## FIXME: begin transaction
        conn.dropDataBase(self._db)
        self._clientL.deleteEntry(self._o)
        ## FIXME: end transaction
        self.emit(PYSIGNAL("client"),(self._o, 'D')) # Tell about it
        self.done(0)
        
    def slotCancel(self):
        """Do not delete after all
        """
        self.done(0)

class ClientNew(Control.uClientEditNew.uClientEditNew):
    """Dialogue to specify a new client
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue
        """
        Control.uClientEditNew.uClientEditNew.__init__(self,parent,name,
                                                       modal,fl)
        self.setCaption(self.tr("New client"))
        self.clients.setEditable(1)
        self.vat.setChecked(1)
        self.vat.setEnabled(1)
        self._o= Model.Client.Client()
        self.firstEntry.setText('2') # Entry 0 and 1 are reserved
        initCombos(self)
        self.year.setValue(int(time.localtime(time.time()).tm_year))

    def slotSave(self):
        """Save the new client object. Called when Save button clicked.
        """
        try:
            self._o.name= string.strip(str(self.clients.currentText()))
            self._o.year= "%s"%self.year.value()
            self._o.regNum= string.strip(str(self.regNum.text()))
            if self.vat.isChecked(): self._o.vat= 'Y'
            else: self._o.vat= 'N'
            self._o.firstEntry= string.strip(str(self.firstEntry.text()))
            self._o.periodes= string.strip(str(self.periodes.currentText()))
            if self.budget.isChecked(): self._o.budget= 'Y'
            else: self._o.budget= 'N'
            self._o.dimension= string.strip(str(self.dimension.currentText()))
        except Model.Exceptions.VarLimit, s: #A parameter is out of range
            try:
                m= str(self.tr(e[s[1]]))
            except KeyError:
                m= str(self.tr(
                    "Error '%s' in one of the dialogue fields"%s[1]))
            msg= m + str(self.tr('\nPlease fix,\nThis client was not saved.'))
            QMessageBox.information(self, Model.Global.getAppName(), msg)
            return # to fix the error
        clientL= Model.Global.getClientList()
        clientL.saveEntry(self._o)
        # The new client is saved in the client database table.
        # Now make the client's database and all tables therein
        dbName= Model.Global.makeDbName(self._o.id) #New database name
        Model.Books.createDatabase(dbName)
        Model.Books.readBooks(self._o.id) #implies: create them too


        # Import the account plan chosen by the combo
        path= Model.Global.getVarPath() + '/' + \
              str(self.accPlan.currentText()) + '.gapl'
        try:
            Model.AccountImport.importGapl(path)# and import
        except Model.Exceptions.FileError, s:
            QMessageBox.information(self, Model.Global.getAppName(),
                   str(self.tr('Could not read the chart of accounts')) +
                                     '\n' + str(s))
            return

        # Import the VAT file chosen by the combo
        path= Model.Global.getVarPath() + '/' + \
              str(self.vatFile.currentText()) + '.vat'
        try:
            Model.Vat.readFile(path)# and import
        except Model.Exceptions.FileError, s:
            QMessageBox.information(self, Model.Global.getAppName(),
                  str(self.tr('Could not read the file of VAT-defaults')) +
                                    '\n' + str(s))
            return

        clientL.saveEntry(self._o)

        self.emit(PYSIGNAL("client"),(self._o, 'N'))# Tell about the new client
        self.done(1)
        
    def slotCancel(self):
        self.done(0)


