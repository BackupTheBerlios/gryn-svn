"""$Id$<br>
A split belongs to a source. Each split describes one posting, i.e. amount,
account and debit/credit. See 'Model.Account.py' for a better documented
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


import Model.Gobject

def createTable(dataBase):
    db= Database.DbAccess.DbAccess(dataBase)
    db.createTable(SplitList._tableName, Split._varsType)
    db.close()

class Split(Model.Gobject.Gobject):
    """Split variables from database table:<br>
    <b>id</b>: The split's unique database table index, int<br>
    <b>source</b>: The index of the source this split belongs to, int<br>
    <b>account</b>: The index of the account this split applies to, int<br>
    <b>side</b>: The side of the account this split applies to, 'D' or 'C',
    1 char<br>
    <b>amount</b>: The amount of this split, moneyint<br>
    <b>line</b>: The original posistion this split appeared on, maybe useful
    to guaranty that split will always be reported in the same order,
    &le;3 chars.<br>
    <b>vat</b>: The VAT code if defined, space if not set.
    """

    _varsType= (('id','INDEX.0'),
                ('source','INT.0'),
                ('account','INT.0'),
                ('side','BCHAR.1'),
                ('amount','INT.0'),
                ('line', 'BCHAR.3'),
                ('vat', 'BCHAR.1'))

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
        
    def copyOfSplit(self):
        t= self.objectToDbTuple()
        return Split(t)

    def getValue(self):
        """Get the amount of this split.<br>
        <b>return</b>: signed integer moneyint, positive for debit
        """
        if self.side == 'D': return self.amount
        if self.side == 'C': return -self.amount
        print "Split marked neither as credit nor debit" #CHIDEP
        return 0
    
    def __cmp__(self, o2):
        return  cmp(self._line, o2._line)

        
    # property actions

    value= property(getValue, None, None, None)
    
    def setSource(self, source):
        self._source= source
    def getSource(self):
        return self._source
    source= property(getSource, setSource, None, None)

    def setAccount(self, a):
        self._account= a
    def getAccount(self):
        return self._account
    account= property(getAccount, setAccount, None, None)

    def setSide(self, s):
        self._side= s
    def getSide(self):
        return self._side
    side= property(getSide, setSide, None, None)
    
    def setAmount(self, a):
        self._amount= a
    def getAmount(self):
        return self._amount
    amount= property(getAmount, setAmount, None, None)
    
    def getLine(self):
        return self._line
    def setLine(self, l):
        self._line= l
    line= property(getLine, setLine, None, None)
    
    def getVat(self):
        return self._vat
    def setVat(self, l):
        self._vat= l
    vat= property(getVat, setVat, None, None)
    
    def getId(self):
        return self._id
    def setId(self, dummy):
        self._id= None
    id= property(getId, setId, None, None)


### SplitList ###


class SplitList(Model.Gobject.GList):
    _tableName= 'split' 
    _objectName= None
    def __init__(self, database=None):
        self._objectName= 'Split'
        self._vars= Split._vars
        self._init= Split
        self._database= database
        if database != None:
            self._connection= Database.DbAccess.DbAccess(database)
        else:
            self._connection= None
        Model.Gobject.GList.__init__(self, self._connection)

    def fixup(self,lists):
        pass


    def getBySource(self, sid):
        """Find the splits belonging to a certain source<br>
        <b>sid</b>: The index of the parent source, int<br>
        <b>return</b>: A list of found splits
        """
        l= []
        for i in self:
            if i._source== sid: l.append(i)
        return l

    def __repr__(self):
        return 'SplitList'

