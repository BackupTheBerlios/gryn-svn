""" $Id$<br>
Cuven (customer/vendor) is the class used to hold data about our customers
and vendors. The purpose of this class is mainly for reports and
interactions with the user.
This file defines the cuven object and the cuven list object.
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
import Model.Books

def createTable(dataBase):
    db= Database.DbAccess.DbAccess(dataBase)
    db.createTable(CuvenList._tableName, Cuven._varsType)
    db.close()

class Cuven(Model.Gobject.Gobject):
    """The Cuven model's database variables are:<br>
    <b>id</b: The objects unique database table index, int<br>
    <b>num</b: A reference number for this cust/vend, &le;15 chars<br>
    <b>name</b: The name of the customer/vendor, &le;30 chars<br>
    <b>type</b: Cusomer ('C') or vendor ('V'), 1 char<br>
    <b>class</b: What group the cuven belongs to, bitfield, int<br>
    <b>regno</b: Registration number<br>
    The purpose of the class is to group the cuvens. Some group examples for
    a sports club: Men, women, age 12-14... Class is an int bit field,
    where each bit position represents a group.
    """

    _varsType= (('id','INDEX.0'),
                ('num','BCHAR.15'),
                ('name','BCHAR.30'),
                ('type', 'BCHAR.1'),
                ('cls','INT.0'),
                ('regno','BCHAR.20'))

    _vars= ()
    for i in _varsType: # make a tuple of variable names
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
        """Make an Cuven instance, init with the tuple <tt>t</tt> if given"""
        Model.Gobject.Gobject.__init__(self, t)

    def copyOfCuven(self):
        """Return a deep copy of this object"""
        t= self.objectToDbTuple()
        return Cuven(t)

    def __cmp__(self, o2):
        return  cmp(self._num, o2._num)

        
    # property actions
    
    def setName(self, name):
        self._name= name
    def getName(self):
        return self._name
    name= property(getName, setName, None, None)

    def setNum(self, num):
        self._num= num
    def getNum(self):
        return self._num
    num= property(getNum, setNum, None, None)
    
    def setType(self, u):
        self._type= u
    def getType(self):
        return self._type
    type= property(getType, setType, None, None)

    def setRegno(self, b):
        self._regno= b
    def getRegno(self):
        return self._regno
    regno= property(getRegno, setRegno, None, None)
    
    def setCls(self, u):
        self._cls= u
    def getCls(self):
        return self._cls
    cls= property(getCls, setCls, None, None)
    
    def getId(self):
        return self._id
    def setId(self, id):
        if id == None: 
            self._id= id
    id= property(getId, setId, None, None)


class CuvenList(Model.Gobject.GList):
    """The CuvenList class holds a list of Cuven objects"""
    
    _tableName= 'cuven'

    def __init__(self, database=None):
        """Make a new CuvenList instance. If a database is given the list
        will be populated with all entries from the cuven database table
        """
        self._objectName= 'Cuven' ## class dependent
        self._vars= Cuven._vars
        self._init= Cuven
        self._database= database
        if database != None:
            self._connection= Database.DbAccess.DbAccess(database)
        else:
            self._connection= None
        Model.Gobject.GList.__init__(self, self._connection)
        self.sort()
                                   
    def fixup(self, x):
        #Get pointers to  some handy lists
        self._lotEntryL= Model.Books.getList('lotentry')
        self._lotL= Model.Books.getList('lot')
        self._cuvenL= Model.Books.getList('cuven')

    def getById(self, id):
        """Returns the object with the given id<br>
        <b>id</b>: Database index
        """
        for i in self:
            if i._id == id:
                return i
        print 'getCuvenById: Not found, db-inconsistent(%s)'%id #CHIDEP
        return None
    
    def getByNum(self, num, type):
        """Returns the object with the given number and type<br>
        <b>num</b>: Customer/vendor number, char<br>
        <b>type</b>: 'C' or 'V'
        """
        for i in self:
            if i._type != type: continue
            if i._num==num:
                return i
        return None

    def getBySource(self, id):
        """Returns the Cuven object belonging to the given source<br>
        <b>id</b>:The index of the source, int
        """
        lotEntry= self._lotEntryL.getBySource(id)#max 1 lotEntry/source
        if not lotEntry: return None
        lot= self._lotL.getById(lotEntry.lot)  #max 1 lot/source
        if not lot: return None
        return  self._cuvenL.getById(lot.cuven)
    
    def getNextNumber(self, type):
        """Returns a reference number to be used by a new instance. The first
        cuven will get the number given by <tt>hi</tt>. The customers and
        vendors have parallel number series, the <tt>type</tt> variable
        indicates what they are<br>
        <b>type</b>: cuven ('C') or vendor ('V'), char
        """
        
        hi= Model.Global.getFirstCuvenNumber()
        for i in self:
            if i._type != type: continue
            if i._num > hi: hi= i._num
        return str(int(hi) + 1)

    def isUsed(self, o):
        """An active cuven (one that is related to some transactions) must
        not be deleted. This function checks if used.<br>
        <b>o</b>: the cuven object instance<br>
        Returns 0 if not used, 1 if used
        """
        for i in self._lotL:
            if i.cuven == o.id: return 1
        return 0

    def balance(self, co):
        lots= self._lotL.getByCuven(co.id)
        if len(lots) == 0: return None
        bal= 0
        for l in lots:
            bal += l.sum
        return bal
    


    def deleteEntry(self, o):
        """Try to delete this object. Returns 1 if not deleted
        <b>o</b>: the cuven object to delete
        """
        if self.isUsed(o) == 0:
            Model.Gobject.GList.deleteEntry(self, o)
            return 0
        else:
            return 1

    def __repr__(self):
        return 'CuvenList'
