"""$Id$<br>
A lot entry keeps track of one of all transactions between us and our
customers and vendors. Lotentries belongs to lots. Here we define both the
LotEntry object and the accompanying list
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

def createTable(dataBase):
    db= Database.DbAccess.DbAccess(dataBase)
    db.createTable(LotEntryList._tableName, LotEntry._varsType)
    db.close()

class LotEntry(Model.Gobject.Gobject):
    """The LotEntry object use these database table variables:<br>
    <b>id</b>: The Lotentry's unique database table index, int<br>
    <b>lot</b>: The index of the parent Lot, int<br>
    <b>source</b>: The index of the parent source, int<br>
    <b>amount</b>: The amount of this lotentry, moneyint<br>
    <b>side</b>: Debit ('D') or credit ('C'), 1 char<br>
    <b>year</b>: The year this transaction occurred. Useful for slow movers
    whos repayments occurs over years, 4 chars.<br>
    """
    _varsType= (('id','INDEX.0'),
                ('lot','INT.0'),
                ('source','INT.0'),
                ('amount', 'INT.0'),
                ('side', 'BCHAR.1'),
                ('year', 'BCHAR.4')
                )

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
        
    def copyOfLotEntry(self):
        t= self.objectToDbTuple()
        return LotEntry(t)


    def __cmp__(self, o2): # sort by source index, not source reference number
        return  cmp(self._source, o2._source)

        
        
    # property actions
    
    def setLot(self, c):
        self._lot= c
    def getLot(self):
        return self._lot
    lot= property(getLot, setLot, None, None)

    def setSource(self, a):
        self._source= a
    def getSource(self):
        return self._source
    source= property(getSource, setSource, None, None)

    def setSide(self, a):
        self._side= a
    def getSide(self):
        return self._side
    side= property(getSide, setSide, None, None)

    def setAmount(self, a):
        self._amount= a
    def getAmount(self):
        return int(self._amount)
    amount= property(getAmount, setAmount, None, None)

    def setYear(self, a):
        self._year= a
    def getYear(self):
        return self._year
    year= property(getYear, setYear, None, None)

    def signedAmount(self):
        if self._side== 'D':
            return self._amount
        if self._side== 'C':
            return -self._amount
        print "LotENtry neither marked as debit nor credit" #CHIDEP
        return 0

    def getId(self):
        return self._id
    def setId(self, dummy):
        self._id= None
    id= property(getId, setId, None, None)


### LotEntryList ###


class LotEntryList(Model.Gobject.GList):
    """List to hold LotEntry objects
    """
    _tableName= 'lotentry' ## class dependent

    def __init__(self, database=None):
        self._objectName= 'LotEntry' 
        self._vars= LotEntry._vars
        self._init= LotEntry
        self._database= database
        if database != None:
            self._connection= Database.DbAccess.DbAccess(database)
        else:
            self._connection= None
        Model.Gobject.GList.__init__(self, self._connection)

    def fixup(self,lists):
        self.sort()
    
    
    def getById(self, id):
        """Find a LotEntry object with a given id<br>
        <b>id</b>: object index, int<br>
        <b>return</b>: LotEntry object or 'None' if not found
        """
        for i in self:
            if i._id == id:
                return i
        return None

    def getByLot(self, lid):
        """Find LotEntry belonging to the given lot<br>
        <b>lid</b>: Lot unique index<br>
        <b>return</b>: List of the found LotEntry objects
        """
        l= LotEntryList()
        for i in self:
            if i._lot == lid: l.append(i)
        return l

    def getBySource(self, sid):
        """Find the lotentry belonging to a source<br>
        <b>sid</b>: Source unique index<br>
        <b>return</b>: The wanted LotEntry object, or 'None' if not found
        """
        for i in self:
            if i._source == sid: return i
        return None
    
    def getFirstSourceByLot(self, lid):
        """Find the first source of a given lot. If this list is sorted by
        'source.id' the first in the list is the lot's opening source.<br>
        <b>lid</b>: The lot index to search for, int<br>
        <b>return</b>: The index of the source, int, if not found: None
        """
        for i in self:
            if i._lot == lid: return i._source
        return None

    def add(self):
        """Calculate the  balance of the lot entries of a
        lot entry list<br>
        <b>return</b>: The balance, moneyint
        """
        sum= 0
        for i in self:
            if i._side== 'D':
                sum= sum + i._amount
            else:
                sum= sum - i._amount
        return sum
        
    def __repr__(self):
        return 'LotEntryList'

