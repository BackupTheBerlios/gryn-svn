"""$Id$<br>
Lots keeps track of money flow between us and our customers and vendors. So
this object is essential to keep a sold and bought ledger. A new lot is opened
when we record an invoice (in or ourgoing). Following payments are added to
the lot and the lot is closed when the sum of all its lotentries has reached
zero (i.e. the claim is settled).
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
    db.createTable(LotList._tableName, Lot._varsType)
    db.close()

class Lot(Model.Gobject.Gobject):
    """The lot object needs only a pointer to the customer/vendor involved.
    However, open lots must be transfered to next year's books if not closed
    before happy new year. We therefore also add some information from
    the opening source to make meaningful reports next year. The variables
    are:<br>
    <b>id</b>: The lots database table unique index, int<br>
    <b>cuven</b>: The customer/vendor's database table index, int<br>
    <b>sourcetxt</b>: The text of the opening source, &le;30 chars<br>
    <b>sourcedate</b>: The date of the opening source, 10 chars<br>
    <b>sourceref</b>: The opening source's reference number, &le;10 chars<br>
    <b>sourceamount</b>: The opening amount, moneyint<br>
    The object also have one non-database variable:<br>
    <b>sum</b>: The remainder of this lot
    
    """

    _varsType= (('id','INDEX.0'),
                ('cuven','INT.0'),
                ('sourcetxt', 'BCHAR.30'),
                ('sourcedate', 'BCHAR.10'),
                ('sourceref', 'BCHAR.10'),
                ('sourceamount', 'INT.0')
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
        self._sum= 0
        
    def copyOfLot(self):
        t= self.objectToDbTuple()
        return Lot(t)


    def __cmp__(self, o2): #sort by cuven,so lots by the same cuven get grouped
        return  cmp(self._cuven, o2._cuven)

        
    # property actions
    
    def setCuven(self, c):
        self._cuven= c
    def getCuven(self):
        return self._cuven
    cuven= property(getCuven, setCuven, None, None)
    
    def setSum(self, c):
        self._sum= c
    def getSum(self):
        return self._sum
    sum= property(getSum, setSum, None, None)

    def setSourceTxt(self, c):
        self._sourcetxt= c
    def getSourceTxt(self):
        return self._sourcetxt
    sourceTxt= property(getSourceTxt, setSourceTxt, None, None)

    def setSourceDate(self, c):
        self._sourcedate= c
    def getSourceDate(self):
        return self._sourcedate
    sourceDate= property(getSourceDate, setSourceDate, None, None)

    def setSourceRef(self, c):
        self._sourceref= c
    def getSourceRef(self):
        return self._sourceref
    sourceRef= property(getSourceRef, setSourceRef, None, None)

    def setSourceAmount(self, c):
        self._sourceamount= c
    def getSourceAmount(self):
        return self._sourceamount
    sourceAmount= property(getSourceAmount, setSourceAmount, None, None)

    def getId(self):
        return self._id
    def setId(self, dummy):
        self._id= None
    id= property(getId, setId, None, None)


### LotList ###


class LotList(Model.Gobject.GList):
    """List to hold Lot objects"""
    
    _tableName= 'lot' ## class dependent

    def __init__(self, database=None):
        self._objectName= 'Lot' ## class dependent
        self._vars= Lot._vars
        self._init= Lot
        self._database= database
        if database != None:
            self._connection= Database.DbAccess.DbAccess(database)
        else:
            self._connection= None
        Model.Gobject.GList.__init__(self, self._connection)
        self._sum= 0

    def fixup(self,lists):
        self._lotEntryL=  lists['lotentry'] # We'll need access to this one
        #for lo in self:
        #    lel= self._lotEntryL.getByLot(lo.id)
        #    lo.sum= lel.add()
        #    print 'lot sum: ', lo.cuven, lo.sum
            
                
    def getById(self, id):
        """Find Lot object with the given id<br>
        <b>id</b>: id of lot to find<br>
        <b>return</b>: sought Lot object or 'None' if not found
        """
        for i in self:
            if i._id == id:
                return i
        return None

    def getByCuven(self, cid):
        """Find Lot objects that relates to the given customer/vendor<br>
        <b>cid</b>: Customer/vendor database table index, int<br>
        <b>return</b>: List of found lots. The remainder is calculated for
        each returned lot.
        """
        l= []
        for i in self:
            if i._cuven == cid:
                le= self._lotEntryL.getByLot(i._id)#get all entries of this lot
                sum= 0
                #print 'new lot: '
                for j in le:
                    if j.side == 'D': # debit or credit?
                        sum= sum + j.amount
                    else:
                        sum= sum - j.amount
                    #print '   ', j.side, sum, j.amount
                    i._sum= sum
                l.append(i)
        return l

    def getOpenByCuven(self, cid):
        """Find <b>open</b> Lot objects that relates to the given
        customer/vendor<br>
        <b>cid</b>: Customer/vendor database table index, int<br>
        <b>return</b>: List of found lots. The remainder is calculated for
        each returned lot.
        """
        l= []
        for i in self:
            if i._cuven == cid:
                le= self._lotEntryL.getByLot(i._id)
                sum= 0
                for j in le:
                    if j.side == 'D':
                        sum= sum + j.amount
                    else:
                        sum= sum - j.amount
                if sum != 0:
                    i._sum= sum
                    l.append(i)
        return l

        
    def __repr__(self):
        return 'LotList'

