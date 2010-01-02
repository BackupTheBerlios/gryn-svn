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

import os
import string
import Model.Gobject
import Model.Global
import Model.Exceptions

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


def _readFile(f):
    vatL= []
    all= f.readlines()
    for a in all:
        li= string.strip(a)
        if len(li) < 3 or li[0] == '#' : continue
        fields= string.split(a, ':') # raises ValueError
        if len(a) < 10: continue
        vr= Vat()
        try:
            #raises IndexError if not 5 fields
            vr.vatCode= string.strip(fields[0])
            vr.vatName= string.strip(fields[1])
            vr.vatRate= string.strip(fields[2])
            vr.vatAccount= string.strip(fields[3])
            vr.salesAccount= string.strip(fields[4])
        except IndexError:
            raise(Model.Exceptions.FileError(_(
                "Missing field in file of default VAT")))
        vatL.append(vr)
    return vatL
        
def readFile(fn):
    try:
        f= open(fn, 'r')
        vL= _readFile(f)
        f.close()
        vatL= Model.Books.getList('vat')
        for v in vL:
            vatL.saveEntry(v)


    except IOError:
        raise(Model.Exceptions.FileError(_("Could not read file ") + fn))

    except ValueError:
        raise(Model.Exceptions.FileError(_("Syntax error in file ") + fn))


        
