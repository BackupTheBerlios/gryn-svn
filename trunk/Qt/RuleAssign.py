""" $Id$<br>
A dialogue to let the user supply parameter velues for rules.
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
from qttable import QTable
import Control.uRuleAssign
import Model.Global

class RuleAssign(Control.uRuleAssign.uRuleAssign):
    """Opens a dialogue where the user can specify the values of
    parameters to the chosen rule. Usually at least an 'amount'-field.
    Generates a set of splits from the rule.
    """
    def __init__(self, parent, ruleObject, splitList):
        """Set up the dialogue.<br>
        'ruleObject': The rule to apply<br>
        'splitList': The splitList to append the new split to.
        """
        Control.uRuleAssign.uRuleAssign.__init__(self,parent,None,0,0)

        self.setName("RuleAssign")
        self.ruleObject= ruleObject
        self.splitList= splitList
        h= self.wTable.horizontalHeader()
        h.setLabel(0, 'Value')
        v= self.wTable.verticalHeader()
        self.pars= string.split(ruleObject.parametres, ':')
        wMax= 0
        fm= self.fontMetrics()
        
        # presents a table of 'parameter name=' for the user
        self.money= []
        self.paramName= []
        row= 0
        for par in self.pars:
            s= string.split(par, '=')
            self.paramName.append(s[0])
            ss= string.split(s[1], ';')
            self.money.append(ss[1]) 
            lbl= ss[0] + '= '
            v.setLabel(row, lbl)
            w= fm.width(lbl + '     ')
            if w > wMax: wMax= w
            row= row + 1
        for r in range(row, self.wTable.numRows()): # clear the rest
            v.setLabel(r, '')
            self.money.append(' ')
        self.wTable.setLeftMargin(wMax)
        self.wTable.setColumnStretchable(0, 1)

        self.connect(self.wOK,SIGNAL("clicked()"),self.slotMake)
        self.connect(self.wCancel,SIGNAL("clicked()"),self.slotCancel)
        self.connect(self.wTable, SIGNAL('valueChanged(int,int)'),
                     self.slotValueChanged)
        self.languageChange()

        self.resize(QSize(203,308).expandedTo(self.minimumSizeHint()))
        self.wOK.setEnabled(0)
        
    def languageChange(self):
        """Called by the translator.
        """
        self.setCaption(QString.null)
        self.textLabel6.setText(self.tr("Assign values"))
        self.wOK.setText(self.tr("OK"))
        self.wCancel.setText(self.tr("Cancel"))

    def slotCancel(self):
        """The user gave in.
        """
        self.done(0)

    def slotMake(self):
        """Collects all parameter and their values into a colon separated
        string and runs the rule.
        """
        s= ''
        v= self.wTable.verticalHeader()
        for row in range(0, self.wTable.numRows()):
            if v.label(row).isEmpty(): break
            val= self.wTable.text(row, 0)
            print 'row, val:', row, val
            if val.isEmpty():
                QMessageBox.information(self, Model.Global.getAppName(),
                   self.tr('A value field is empty'))
                return
            s= s + "%s=%s;"%(self.paramName[row], str(val))
        s= s[:-1] # remove last semi colon
        # Convert all decimal separators to point. A comma will
        # make the interpreter believe we have a tuple, bad.
        if string.find(s, Model.Global.getDecSep()) >= 0:
            s= string.replace(s, Model.Global.getDecSep(), '.')
        # Run the rule and get back the generated splits
        retSplits= self.ruleObject.runRule(s, self.splitList)
        if retSplits[0] == 'S':
            self.emit(PYSIGNAL('splits'), retSplits) # Tell the world about the
        # new splits
        else:
            QMessageBox.information(self, Model.Global.getAppName(),
                   retSplits[1]) #retSplits is now a translated error message str
        self.done(1)

    def slotValueChanged(self, row, col):
        """Called when the text in a cell change. Reformats field if
        the cell is a money field.<br>
        'row': Table row, int supplied by signal<br>
        'col': Table column, int supplied by signal.
        """
        if self.money[row] == 'M':
            c= Model.Global.moneyReformatZ(str(self.wTable.text(row, col)))
            self.wTable.setText(row, col, c)
        valid= 1
        for r in range(0, self.wTable.numRows()):
            if self.wTable.verticalHeader().label(r).isEmpty(): break
            if self.wTable.text(r, 0).isEmpty(): valid= 0
        self.wOK.setEnabled(valid)
