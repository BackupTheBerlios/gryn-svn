""" $Id$<br>
Dialogue to make and maintain book keeping rules.
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
from qttable import QTable, QCheckTableItem
import Control.uRule
import Model.Books
import Model.Rule
import Model.Global
import Control.Global

class Rule(Control.uRule.uRule):
    """The Rule parent class
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the rule dialogue.
        """
        Control.uRule.uRule.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Rule")

        self.credit= str(self.tr('C'))
        self.debit= str(self.tr('D'))

        # wTabPost entries specifies the posting rules:
        # Account, debit/credit and the posting function
        t= self.wTabPost
        t.setNumCols(3)
        h= t.horizontalHeader()
        h.setLabel(0, self.tr('Account'))
        h.setLabel(1, self.tr('%s/%s'%(self.debit, self.credit)))
        h.setLabel(2, self.tr('Function'))
        v= t.verticalHeader()
        v.hide()
        fm= self.fontMetrics()
        w0= fm.width(str(h.label(0))+'    ')
        w1= fm.width(str(h.label(1))+'    ')
        t.setLeftMargin(0)
        t.setColumnWidth(0, w0)
        t.setColumnWidth(1, w1)
        t.setColumnStretchable(2, 1)
        t.setHScrollBarMode(QScrollView.AlwaysOff)
        t.setVScrollBarMode(QScrollView.AlwaysOff)
        t.setSelectionMode(QTable.SingleRow)

        # wPars entries specifies the parameters to get from the
        # user dialogue when the rule is applied.
        # Parameter: variable name, M: set if the parameter is Money,
        # Name: the parameter name shown to the user
        t= self.wPars
        t.setNumCols(3)
        h= t.horizontalHeader()
        h.setLabel(0, self.tr('Parameter'))
        h.setLabel(1, self.tr('M'))
        h.setLabel(2, self.tr('Dialog tekst'))
        v2= t.verticalHeader()
        v2.hide()
        t.setColumnStretchable(0, 1)
        t.setColumnWidth(1, fm.width('aaaa'))
        t.setColumnStretchable(2, 3)
        t.setLeftMargin(0)
        t.setHScrollBarMode(QScrollView.AlwaysOff)
        t.setVScrollBarMode(QScrollView.AlwaysOff)
        t.setSelectionMode(QTable.SingleRow)
        self.chBox= [None]*self.wPars.numRows()
        for r in range(0, len(self.chBox)):
            self.chBox[r]= QCheckTableItem(self.wPars, '')
            self.chBox[r].setChecked(0)
            self.wPars.setItem(r, 1, self.chBox[r])

        # The prelude is the program executed before the postings
        self.wPrelude.setTextFormat(self.wPrelude.PlainText)

        # Get the relevant lists
        self.ruleL= Model.Books.getList('rule')
        self.accountL= Model.Books.getList('account')
        
    def languageChange(self):
        """Called by the translator.
        """
        self.setCaption(QString.null)
        self.wOK.setText(self.tr("Save"))
        self.wNew.setText(self.tr("New"))
        self.wExit.setText(self.tr("Exit"))
        self.textLabel5.setText(self.tr("Postings"))
        self.textLabel3.setText(self.tr("Parametres"))
        self.textLabel2.setText(self.tr("Default text"))
        self.textLabel4.setText(self.tr("Prelude"))
        self.textLabel1.setText(self.tr("Rule name"))

    def slotExit(self):
        """Called when user clicks OK button.
        """
        self.done(0)

    def slotNew(self):
        """Called when the user clicks New button.
        """
        self.blankFields()

    def save(self, rule):
        """Called when user clicks Save button, Saves the new or
        edited rule.<br>
        'rule': The rule object to save
        """
        #Move from fields to rule object
        rule.name= string.strip(str(self.wName.text()))
        if len(rule.name) < 1:
            QMessageBox.information(self, Model.Global.getAppName(),
                                    self.tr('Rule name is empty'))
            return
            
        rule.text= string.strip(str(self.wText.text()))
        if len(rule.text) < 1:
            QMessageBox.information(self, Model.Global.getAppName(),
                                    self.tr('Rule text is empty'))
            return
        # Make an executable string from the wPars table
        sP= ''
        for row in range(0, self.wPars.numRows()):
            s0= self.wPars.text(row, 0)
            if not s0 or s0.length() < 1: continue
            s1= self.wPars.text(row, 2)
            if not s1 or s1.length() < 1:
                QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('Name is missing in row %s'%row))
                return
            # The string consists of entries separated by colons.
            # Each entry consists of two fields separated by a semi colon
            # These fields are the parameter statement and the money-flag
            money= self.wPars.item(row, 1).isChecked()
            if money == 0: money= 'F'
            else: money= 'M'
            sP= sP + '%s=%s;%s:'%(
                string.strip(str(s0)),
                string.strip(str(s1)), money)
        if len(sP) > 0:
            sP= sP[:-1]
            rule.parametres= sP
            
        # Make an executable string from the prelude field
        # The lines are collected into one string, a semi colon
        # indicates line breaks
        prelude= self.wPrelude.text()
        if prelude and prelude.length() > 0:
            prelude= str(prelude)
            if string.find(prelude, '\n') > 0:
                prelude= string.replace(prelude, '\n', ';')
        else: prelude= ''
        rule.prelude= prelude

        # Make an executable from the wTabPost table rows
        # all posting statements are collected into one string separated by
        # colons. Each statement consists of three elemets separated by
        # semi colon: The account id, the side (debit/credit) and the
        # posting function
        
        sP= ''
        for row in range(0, self.wTabPost.numRows()):
            s0= self.wTabPost.text(row, 0) 
            if not s0 or s0.length() < 1: continue
            account= string.strip(str(s0))
            acc= self.accountL.getByNum(account)
            if not acc:
                QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('%s\nThis account does not exist\n'%account))
                return
            s1= self.wTabPost.text(row, 1)
            if not s1 or s1.length() < 1: s1= 'X '
            s1= string.strip(str(s1)) + ' '
            side= string.upper(s1[0])
            print 's1, side: ', s1, side
            if side != self.credit and side != self.debit:
                QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('The Side-cell must be either %s or %s\n'%(
                    self.debit, self.credit)))
                return
            s2= self.wTabPost.text(row, 2)
            if not s2 or s2.length() < 1:
                QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('The function is missing in row %s\n'%row))
                return
            func= string.strip(str(s2))
            
            sP= sP + '%s;%s;%s:'%(acc.id, side, func)
        if len(sP) > 0:
            rule.postings= sP[:-1]
        # Then ,at last:
        self.ruleL.saveEntry(rule)

    def blankFields(self):
        """Blank some fields and make ready for a new rule.
        """
        for row in range(self.wTabPost.numRows()):
            self.wTabPost.setText(row, 0, QString(''))
            self.wTabPost.setText(row, 1, QString(''))
            self.wTabPost.setText(row, 2, QString(''))
        for row in range(self.wPars.numRows()):
            self.wPars.setText(row, 0, QString(''))
            self.wPars.setText(row, 2, QString(''))
            self.wPars.item(row, 1).setChecked(0)
        self.wText.setText(QString(''))
        self.wName.setText(QString(''))
        self.wPrelude.clear()

    def initFields(self, rule):
        """Set up the fields according to the properties of a rule.<br>
        'rule': The rule object
        """
        posts= string.split(rule.postings, ':')
        row= 0
        for post in posts:
            acc, side, func= string.split(post, ';')
            accObj= self.accountL.getById(int(acc))
            self.wTabPost.setText(row, 0, accObj.num)
            self.wTabPost.setText(row, 1, side)
            self.wTabPost.setText(row, 2, func)
            row= row + 1
        pars= string.split(rule.parametres, ':')
        row= 0
        for par in pars:
            s= string.split(par, ';')
            money= s[1]
            ss= string.split(s[0], '=')
            self.wPars.setText(row, 0, ss[0])
            self.wPars.setText(row, 2, ss[1])
            if money == 'M': self.wPars.item(row, 1).setChecked(1)
            else: self.wPars.item(row, 1).setChecked(0)
            row += 1
        self.wText.setText(rule.text)
        self.wName.setText(rule.name)
        if len(rule.prelude) > 0:
            self.wPrelude.setText(string.replace(rule.prelude, ';', '\n'))
        else:
            self.wPrelude.clear()
        
                           

            
#  RuleNew Class
#  -------------

class RuleNew(Rule):
    """Dialogue to create a new rule.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue.
        """
        Rule.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr('New rule'))
        self.connect(self.wOK,SIGNAL("clicked()"),self.slotSave)
        self.connect(self.wExit,SIGNAL("clicked()"),self.slotExit)
        self.connect(self.wNew,SIGNAL("clicked()"),self.slotNew)

    def slotSave(self):
        """Save the rule.
        """
        rule= Model.Rule.Rule() # Make a new Rule object
        self.save(rule)

#  RuleEdit class
#  --------------

class RuleEdit(Rule):
    """Dialogue to edit an existing rule.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue. Assumes the rule to edit sits in
        the global listSelected.
        """
        Rule.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr('Edit rule'))
        self.connect(self.wOK,SIGNAL("clicked()"),self.slotSave)
        self.connect(self.wExit,SIGNAL("clicked()"),self.slotExit)
        self.connect(self.wNew,SIGNAL("clicked()"),self.slotNew)

        viewList= Control.Global.getListSelected()
        ruleObj= viewList[0]
        self.ruleCopy= ruleObj.copyOfRule() # Edit on a copy in case the user
        # cancels
        self.initFields(self.ruleCopy)

    def slotSave(self):
        """ Save the edited copy in the original's place.
        """
        self.save(self.ruleCopy)

#  RuleView class
#  --------------

class RuleView(Rule):
    """ Dialogue to view rules. Assumes the rules to view sits in the global
    listSelected. Not implemented yet.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue.
        """
        Rule.__init__(self,parent,name,modal,fl)
        self.setCaption(self.tr('View rule'))

#  RuleDelete class
#  ----------------

class RuleDelete(Rule):
    """ Dialogue to delete a rule. The rule to delete sits in
    the global listSelected. Not implemented yet.
    """
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        """Set up the dialogue.
        """
        Rule.__init__(self,parent,name,modal,fl)
        self.setCaption('Delete rule')

