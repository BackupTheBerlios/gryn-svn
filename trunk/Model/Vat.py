"""$Id$<br>
Vat object keeps properies about one VAT-rate and relevant account numbers.
The VatList is the collection of VAT variants
See 'Model.Account.py' for a better documented
subclass.
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


import Database.DbAccess
import Model.Gobject
import Model.Global

import gettext
t = Model.Global.getTrans()
if t != None:
    _= t.gettext
else:
    def _(x):
        return x


def createTable(dataBase):
    db= Database.DbAccess.DbAccess(dataBase)
    db.createTable(VatList._tableName, Vat._varsType)
    db.close()

class Vat(Model.Gobject.Gobject):
    """Vat variables from database table:<br>
    'id:' The Vat's unique database table index, int<br>
    'vatCode:' A numeric identifier used somewhere, 1 char<br>
    'vatName:' Name of this variant, &le;15 char <br>
    'vatRate:' The rate in percent, &le;10 char (int or float)<br>
    'vatAccount:' The account number to post the VAT of this variant,
    4 char<br>
    'salesAccount:' For sale variants: The account number where the net amount
    shall be posted, 4 char.
    """
    _varsType= (('id','INDEX.0'),
                ('vatCode','BCHAR.1'),
                ('vatName','BCHAR.15'),
                ('vatRate','BCHAR.10'),
                ('vatAccount','BCHAR.4'),
                ('salesAccount', 'BCHAR.4'))





    _vars= ()
    for i in _varsType:
        _vars= _vars+ (i[0],)
    # Generate the format, a number of '%s:%s:%s:...'
    _fmt= ("%s:"*len(_vars))[:-1]
    # Generate the expression, '(self._var1, self._var2,...)'
    _tuple=(('('+'self._%s,'*len(_vars))[:-1] + ')'
                 )%_vars
    # compiled expressions
    _cToTuple= compile(_tuple, '<string>', 'eval')
    _cToObject= compile(_tuple+'= t','<string>', 'exec')

    def __init__(self, t= None):
        Model.Gobject.Gobject.__init__(self, t)
        
    def copyOfVat(self):
        t= self.objectToDbTuple()
        return Vat(t)

    def __cmp__(self, o2):
        return  cmp(self._vatCode, o2._vatCode)

        
    # property actions
    def getVatCode(self):
        return self._vatCode
    def setVatCode(self, vc):
        self._vatCode= vc
    vatCode= property(getVatCode, setVatCode, None, None)

    def getVatName(self):
        return self._vatName
    def setVatName(self, vc):
        self._vatName= vc
    vatName= property(getVatName, setVatName, None, None)

    def getVatRate(self):
        return self._vatRate
    def setVatRate(self, vc):
        self._vatRate= vc
    vatRate= property(getVatRate, setVatRate, None, None)

    def getVatAccount(self):
        return self._vatAccount
    def setVatAccount(self, vc):
        self._vatAccount= vc
    vatAccount= property(getVatAccount, setVatAccount, None, None)

    def getSalesAccount(self):
        return self._salesAccount
    def setSalesAccount(self, vc):
        self._salesAccount= vc
    salesAccount= property(getSalesAccount, setSalesAccount, None, None)

    def getId(self):
        return self._id
    def setId(self, dummy):
        self._id= None
    id= property(getId, setId, None, None)


### VatList ###


class VatList(Model.Gobject.GList):
    _tableName= 'vat' 
    _objectName= None
    def __init__(self, database=None):
        self._objectName= 'Vat'
        self._vars= Vat._vars
        self._init= Vat
        self._database= database
        if database != None:
            self._connection= Database.DbAccess.DbAccess(database)
        else:
            self._connection= None
        Model.Gobject.GList.__init__(self, self._connection)

    def fixup(self, lists):
        #We lack a VAT spec dialog, so do the db-init here for now
        if len(self) == 0:
            self.append(Vat((None, '0', 'None', None, None, '3200')))
            self.append(Vat((None, '1', 'LowIn', '6', '2712', None)))
            self.append(Vat((None, '2', 'MediumIn', '11', '2711', None)))
            self.append(Vat((None, '3', 'HighIn', '25', '2710', None)))
            self.append(Vat((None, '4', 'LowOut', '6', '2702', '3002')))
            self.append(Vat((None, '5', 'MediumOut', '11', '2701', '3001')))
            self.append(Vat((None, '6', 'HighOut', '25', '2700', '3000')))
            for e in self: self.saveEntry(e)
        for v in self:
            if v.vatCode == '0':
                v.vatName= _('None')
                v.vatRate= None
                v.vatAccount= None
            if v.vatCode == '1':
                v.vatName= _('LowIn')
                v.salesAccount= None
            if v.vatCode == '2':
                v.vatName= _('MediumIn')
                v.salesAccount= None
            if v.vatCode == '3':
                v.vatName= _('HighIn')
                v.salesAccount= None
            if v.vatCode == '4': v.vatName= _('LowOut')
            if v.vatCode == '5': v.vatName= _('MediumOut')
            if v.vatCode == '6': v.vatName= _('HighOut')
        self.sort()

    def getByCode(self, code):
        """
        Return the object with vatCode == code<br>
        'code:' vatCode, 1 digit char
        'return:' The found object, None if not found
        """
        for e in self:
            if e._vatCode == code: return e
        return None

    #For some reason the Vat-objects are only referenced to by the vatCode
    # id is only used to follow the Gobject template and to make a distinction
    # between saved and new objects

    def __repr__(self):
        return 'VatList'

