""" $Id$<br>
Dialogues to create and maintain accounts.<br>
Wishes: make account name field into a combo and show results while typing like
the url-field in konqueror and Firefox.

        
Emits signal 'account' with parameters the account instance plus a char:<br>
E: Instance was edited<br>
N: This is a new instance<br>
D: This instance was deleted<br>

Reacts to the special signal 'accountSelected', presumeably from an account
select window.
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
#import os
from qt import *
import Control.uAccount
import Model.Global
import Model.Account
import Model.Grep
import Model.Books

# Error messages used to decode exceptions returned from the Model
e= {'Name':QT_TRANSLATE_NOOP('account_name','Client name too short.'),
    'Num':QT_TRANSLATE_NOOP('account_num',
                            'Account must be a four digit number.'),
    'Vat':QT_TRANSLATE_NOOP('account_vat', 'Vat code is out of legal range'),
    'Budget':QT_TRANSLATE_NOOP('account_budget', 'Budget value too short.')
}

class Account(Control.uAccount.uAccount):
    """Base class for account dialogues.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """ Set up the dialogue
        """
        # GUI class generated from designer file
        Control.uAccount.uAccount.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Account")
        self._accountL= Model.Books.getList('account')
        self._vatL= Model.Books.getList('vat')
        self._accObj= None
        #set up grep related 
        self.initNameGrep()
        reAccount= r"^\d\d\d\d$" # account numbers are four digits
        rex= QRegExp(QString(reAccount))
        self.val= QRegExpValidator(rex, None)
        self.wAccNum.setValidator(self.val)

        
        clientO= Model.Global.getClientObject()#so we can get some client props
        self.useBudget= clientO.budget 
        self.useVat= clientO.vat
        self.initCombo() #set up vat-combo
        #These images indicate grep and edit mode for the account name
        self.imgFind = QPixmap(Control.Global.expandImg('filefind.png'))
        self.imgEdit = QPixmap(Control.Global.expandImg('edit.png'))
        self.wLineMode.setPixmap(self.imgFind) #We are grepping

        self.hideAndSuch() # show some or all fields of the dialogue
        self.connect(self.wSave,SIGNAL("clicked()"),self.slotSave)
        self.connect(self.wNew,SIGNAL("clicked()"),self.slotNew)
        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)

    def initNameGrep(self):
        """ Set up a grepper for account names in account list, but
        only for those with account number >= 4
        """
        self._nameGrep= Model.Grep.Grep(self._accountL, 'name',
                                        'len(i._num) < 4')
    def blockSomeSignals(self, yn):
        """ Blocks or unblocks signals from the
        account name and account number fields<br>
        'yn': umblock if 0, block if 1
        """
        self.wAccName.blockSignals(yn)
        self.wAccNum.blockSignals(yn)

        
    def hideAndSuch(self):
        """ Hide irrelevant fields according to if the client
        uses budget and VAT
        """
        if self.useBudget == 'Y':
            self.wBudget.setEnabled(1)
            QObject.connect(self.wBudget,
                            SIGNAL('lostFocus()'), self.budgetLostFocus)
        else:
            self.wBudget.setEnabled(0)
            self.wBudget.hide()
            self.wBudgetLabel.hide() 
        if self.useVat == 'Y':
            self.wVat.setEnabled(1)
        else:
            self.wVat.setEnabled(0)
            self.wVat.hide()
            self.wVatLabel.hide()

    def slotSave(self):
        """The consequences of clicking the Save button is left for the
        subclasses.
        """
        print "Account.slotSave(): Not implemented yet"

    def slotNew(self):
        """When New-button clicked. Clear fields and get a new name-grepper.
        Do not change VAT-code, as this will often be the same as the previous.
        """
        self.wAccNum.setText(QString(''))
        self.wAccName.setText(QString(''))
        self.wBudget.setText(QString(''))
        self._accObj= None
        self.blockSomeSignals(0)
        self.wSave.setEnabled(0)
        self.initNameGrep()
        self.wLineMode.setPixmap(self.imgFind)# we allways start by grepping

    def slotCancel(self):
        """Trow away what we have done
        """
        self.done(0)

    def inject(self, acc):
        """Inject an account object into the dialogue<br>
        'acc': The injected account object
        """
        self.slotNew() # Clear all fields first
        self.wAccNum.setText(acc.num)
        self.wAccName.setText(acc.name)
        if self.useVat == 'Y':
            self.wVat.setCurrentItem(int(acc.defVat))
        if self.useBudget == 'Y':
            self.wBudget.setText(Model.Global.intToMoneyZ(acc.budget))
        self.setActiveWindow() # Get the focus back to our dialogue
        self.wSave.setEnabled(1)

    def budgetLostFocus(self):
        """Called when the budget field loses focus. Reformat the field
        value to money format. Blank field if budget is zero.
        """
        i= Model.Global.moneyToInt(str(self.wBudget.text()))
        self.wBudget.setText(Model.Global.intToMoneyZ(i))

    def initCombo(self):
        """Set up the VAT combo box.<br>
        vatL is supposed to be sorted when read from db by its fixup,
        so just append the instances to the combo
        """
        self.wVat.clear()
        for v in self._vatL:
            self.wVat.insertItem(v.vatName)
    
    def nameGrep(self, stxt):
        """__init__ sets this to be signaled when the account name
        field changes. Adjusts  the name field as the grep progresses.<br>
        'stxt': Current name field text (passed by signal)
        """
        self._accObj= None # we have not found the account yet
        self.wSave.setEnabled(0) # so don't let them save
        txt= str(stxt)
        s, gLen= self._nameGrep.grepInput(txt) # do the grep
        if gLen >= 0: # still not a unique account name
            self.wAccName.blockSignals(1)
            self.wAccNum.blockSignals(1)
            self.wBudget.blockSignals(1)
            self.wAccName.setText(s)
            self.wAccName.setCursorPosition(gLen)
            self.wAccNum.setText('')
            self.wBudget.setText('')
            self._accObj= None
            self.wAccName.blockSignals(0)
            self.wAccNum.blockSignals(0)
            self.wBudget.blockSignals(0)
        else: # a unique account found, so show in fields
            self._accObj= s
            self.wAccName.blockSignals(1)
            self.wAccName.setText(s.name)
            self.wAccName.blockSignals(0)
            self.wAccNum.setText(s.num)
            self.wVat.setCurrentItem(int(s.defVat))
            self.wBudget.setText(Model.Global.intToMoneyZ(self._accObj.budget))

    def nameLostFocus(self):
        """Called when the name field loses focus
        """
        if self.wAccName.text().length() < 1: return # field empty
        if not self._accObj: # Lost focus before a unique account was found
            #so get the first in the list of accounts matching the grep string
            self._accObj= self._nameGrep.getFirstMatch()
        if not self._accObj: return # Well, we didn't get one after all
        sn= string.strip(str(self.wAccName.text()))
        p= string.find(sn, ':') #marks the start of found account name
        if p>=0: # remove any leftovers from the grepping, preceeding the :
            self.wAccName.blockSignals(1)
            self.wAccName.setText(sn[p+2:]) # the full account name
            self.wAccName.blockSignals(0)
        # set fields according to the object
        self.wAccNum.setText(self._accObj.num)
        self.wVat.setCurrentItem(int(self._accObj.defVat))
        self.wBudget.setText(Model.Global.intToMoneyZ(self._accObj.budget))
        self.wSave.setEnabled(1)

    def accNumChanged(self, s):
        """Set up by _init__ to take signal when the account number
        changes.<br>
        's': Field value string, only digits, supplied by signal
        """
        slen= s.length()
        self.wSave.setEnabled(0)
        self._accObj= None
        if slen == 4: # a valid account number
            accO= self._accountL.getByNum(str(s)) # get the account object
            if accO:
                self.wAccName.blockSignals(1)
                self.wAccName.setText(accO.name)
                self.wAccName.blockSignals(0)
                self.wVat.setCurrentItem(int(accO.defVat))
                self.wBudget.setText(Model.Global.intToMoneyZ(accO.budget))
                self._accObj= accO.copyOfAccount()
                self.wSave.setEnabled(1)
            else:
                QMessageBox.information(self, Model.Global.getAppName(),
                                  self.tr('This account does not exist\n'))
        elif slen > 4: # This can't happen, but anyway...
            self.wAccNum.setText(str(s)[:4])
        else: #account < 4 digits long is not a valid account, remove any name
            self.wAccName.blockSignals(1)
            self.wAccName.setText('')
            self.wAccName.blockSignals(0)

class AccountEdit(Account):
    """ This dialogue is used to edit the properties of an account.
    We must edit on copies of account objects in case
    the user later clicks on Cancel. 
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up Edit specific fields and signal connections.<br>
        'parent', 'name', 'modal', 'fl': As usual
        """
        Account.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr('Account edit'))
        self.initCombo()
        self.wNew.setText(self.tr('Clear'))
        self.wSave.setEnabled(0)
        #Set up signal slot relations
        QObject.connect(parent,PYSIGNAL('accountSelected'), self.inject)
        QObject.connect(self.wAccName, SIGNAL('textChanged(const QString &)'),
                        self.nameGrep)
        QObject.connect(self.wAccName, SIGNAL('lostFocus()'),
                        self.nameLostFocus)
        QObject.connect(self.wAccNum, SIGNAL('textChanged(const QString &)'),
                        self.accNumChanged)
        self.wSave.setEnabled(0)

    def inject(self, acc):
        """Inject an account object into the dialoge and turn off signals
        from name and number fields whil we edit<br>
        'acc': Account object, supplied by signal
        """
        Account.inject(self, acc)
        self._accObj= acc.copyOfAccount() # Make a new objet for editing
        self.blockSomeSignals(1)
        self.wLineMode.setPixmap(self.imgEdit) #name field is in edit mode
        
    def slotSave(self):
        """Called when user clicks on Save button. Saves the copy of the
        account object in account object's place
        """
        if self._accObj.id: # else: nothing to do
            o= self._accObj
            try:
                o.num= string.strip(str(self.wAccNum.text()))
                o.name= string.strip(str(self.wAccName.text()))
                if self.useVat == 'Y':
                    o.defVat= str(self.wVat.currentItem())
                else: o.defVat= '0'
                if self.useBudget=='Y':
                    o.budget= Model.Global.moneyToInt(
                        str(self.wBudget.text()))
                else: o.budget= 0
            except Model.Exceptions.VarLimit, s:
                try: # do we have an appropriate error message?
                    m= str(self.tr(e[s[1]]))
                except KeyError: #No, fake one
                    m= str(self.tr("Error text for '%s' is not defined"))%s[1]
                    msg= m + str(self.tr(
                        '\nPlease fix,\nThis account was not saved.'))
                QMessageBox.information(self, Model.Global.getAppName(), msg)
                return # Try again
            res= self._accountL.saveIfChanged(o)
            if res != 0: # changed and saved, tell the world
                self.emit(PYSIGNAL('account'), (self._accObj, 'E'))
            self.slotNew() # prepare for a new edit


    def nameLostFocus(self):
        """Called when the name field loses focus.<br> Almost like the base
        function, perhaps merge into base class.
        """
        if self.wAccName.text().length() < 1: return # field empty
        if not self._accObj: # Lost focus before a unique account was found
            #so get the first in the list of accounts matching the grep string
            self._accObj= self._nameGrep.getFirstMatch()
        if not self._accObj: return # Well, we didn't get one after all
        # We must disable grepping while the account name is edited 
        self.blockSomeSignals(1)

        self.wSave.setEnabled(1)
        sn= string.strip(str(self.wAccName.text()))
        p= string.find(sn, ':')
        if p>=0: # remove any leftovers from the grepping
            self.wAccName.blockSignals(1)
            self.wAccName.setText(sn[p+2:]) # the full account name
            self.wAccName.blockSignals(0)
        # set fields according to the object
        self.wAccNum.setText(self._accObj.num)
        self.wVat.setCurrentItem(int(self._accObj.defVat))
        self.wBudget.setText(Model.Global.intToMoneyZ(self._accObj.budget))
        self.wSave.setEnabled(1)
        self.wLineMode.setPixmap(self.imgEdit)
        self.blockSomeSignals(1)

    def accNumChanged(self, s):
        """Called when the account number changes.<br>
        's': Field value string, only digits, supplied by signal<br>
        Almost like the base
        function, perhaps merge into base class.
        """
        slen= s.length()
        self.wSave.setEnabled(0)
        self._accObj= None
        if slen == 4: # a legal account number
            accO= self._accountL.getByNum(str(s)) # get the account object
            if accO:
                self.wAccName.blockSignals(1)
                self.wAccName.setText(accO.name)
                self.wAccName.blockSignals(0)
                self.wVat.setCurrentItem(int(accO.defVat))
                self.wBudget.setText(Model.Global.intToMoneyZ(accO.budget))
                self._accObj= accO.copyOfAccount()
                self.wSave.setEnabled(1)
                self.wLineMode.setPixmap(self.imgEdit)
                self.blockSomeSignals(1) # while editing name 
            else:
                QMessageBox.information(self, Model.Global.getAppName(),
                                  self.tr('This account does not exist\n'))
        elif slen > 4: # This can't happen, but anyway...
            self.wAccNum.setText(str(s)[:4])
        else: #When account < 4 digits long we can't have an account name
            self.wAccName.blockSignals(1)
            self.wAccName.setText('')
            self.wAccName.blockSignals(0)

class AccountNew(Account):
    """ This dialogue is used to define the properties of a new account.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up New specific fields and signal connections.<br>
        'parent', 'name', 'modal', 'fl': As usual
        """
        Account.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr('Account new'))
        self.wNew.setText(self.tr('Clear'))
        self.wSave.setEnabled(1)
        #Enable inject in case we want to base the new account on an old
        QObject.connect(parent,PYSIGNAL('accountSelected'), self.inject)

        
    def slotSave(self):
        """Save the new account. Called when Save-button clicked
        """
        #First, is this really a new account?
        if self._accountL.getByNum(string.strip(str(self.wAccNum.text()))):
            QMessageBox.information(self, Model.Global.getAppName(),
                    str(self.tr("This account already exists.")) + '\n' +
                    str(self.tr("Please chose a new account number.")))
        else: #no, make a new account object and fill in from fields
            o= Model.Account.Account()
            try:
                o.num= string.strip(str(self.wAccNum.text()))
                o.name= string.strip(str(self.wAccName.text()))
                if self.useVat == 'Y':
                    o.defVat= str(self.wVat.currentItem())
                else: o.defVat= '0'
                if self.useBudget=='Y':
                    o.budget= Model.Global.moneyToInt(
                        str(self.wBudget.text()))
                else: o.budget= 0
            except Model.Exceptions.VarLimit, s: #An unacceptable value
                try: # approporiate error message?
                    m= str(self.tr(e[s[1]]))
                except KeyError: #No, make a substitute
                    m= str(self.tr("Error text for '%s' is not defined"))%s[1]
                    msg= m + str(self.tr(
                        '\nPlease fix,\nThis account was not saved.'))
                QMessageBox.information(self, Model.Global.getAppName(), msg)
                return # and let the user correct
            self._accountL.saveEntry(o)
            self.emit(PYSIGNAL('account'), (o, 'N')) # Tell the world
            self.slotNew()

class AccountDelete(Account):
    """ This dialogue is used to delete an existing account.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up delete specific fields and signal connections.<br>
        'parent', 'name', 'modal', 'fl': As usual
        """
        Account.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr('Account delete'))
        self.wNew.hide() #not useful for a delete action
        self.wSave.setText(self.tr('Delete')) # more appropriate

        self.wSave.setEnabled(0)
        self.hideAndSuch()    
        QObject.connect(parent,PYSIGNAL('accountSelected'), self.inject)
        QObject.connect(self.wAccName, SIGNAL('textChanged(const QString &)'),
                        self.nameGrep)
        QObject.connect(self.wAccName, SIGNAL('lostFocus()'), self.nameLostFocus)
        QObject.connect(self.wAccNum, SIGNAL('textChanged(const QString &)'),
                        self.accNumChanged)
        
    def inject(self, acc):
        """Get the account object from an other dialogue.<br>
        'acc': Account object supplied with signal
        """
        Account.inject(self, acc) # do the basefunction, and then some...
        self._accObj= acc.copyOfAccount()
        self.wAccNum.setText(acc.num)
        self.wAccName.setText(acc.name)
        self.wVat.setCurrentItem(int(acc.defVat))
        self.wBudget.setText(Model.Global.intToMoney(acc.budget))
        
    def slotSave(self): # actually acts as a slotDelete
        """In spite of the name, actually deletes the current account
        if the account is not in use.
        """
        if self._accObj.id:
            keep= self._accObj # remeber a few lines further
            # The deleteEntry will check if the account is used by any
            # split of the ledger, 0 if OK to delete
            if self._accountL.deleteEntry(self._accObj) != 0:
                emsg= self.tr('Account is active. Cannot delete')
                QMessageBox.information(self, Model.Global.getAppName(), emsg)
                return
            self.slotNew()
            self.emit(PYSIGNAL('account'), (keep, 'D'))
    
