"""  $Id$<br>
This file defiens the Client object and the client object list object.
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


import string
import Database.DbAccess
import Model.Gobject

DbAccess= Database.DbAccess.DbAccess


def createTable(dataBase):
    """Create an empty database table for this object list.<br>
    <b>dataBase</b>: database name, usually <tt>gryn</tt>."""

    db= Database.DbAccess.DbAccess(dataBase)
    db.createTable(ClientList._tableName, Client._varsType)
    db.close()

class Client(Model.Gobject.Gobject):
    """This class holds all data about the client:<br>
    <b>id</b>: The database unique index of this object, int<br>
    <b>name</b>: The name of the client, &le;30 chars<br>
    <b>year</b>: The year of the client's accounting, 4 char (200x)<br>
    <b>vat</b>: <tt>Y</tt> if the client uses VAT accounts, 1 char<br>
    <b>regNum</b>: Some kind of official registration number for the
    client, &le;15 char.<br>
    <b>firstEntry</b>: The referencenumber given to the first source,
    &le;5chars.<br>
    <b>periodes</b>: Number of periodes of the year. Usually equal to the
    number of VAT statements to be reported each year, 2 chars.<br>
    <b>budget</b>: Set to <tt>Y</tt> to use budgeting.<br>
    <b>dimension</b>: Number ofr dimensions, 1 char (0-3).<br>
    <b>open</b>: Set to <tt>N</tt> when this year's accounts has been finally
    transfered to the next year, 1 char.<p>
    Not all of these variables are used, budget and dimension are for possible
    use in the future.
    """
    _varsType= (('id','INDEX.0'),
                ('name','BLOB.30'),
                ('year','BLOB.4'),
                ('vat','BLOB.1'),
                ('regNum','BLOB.15'),
                ('firstEntry', 'BLOB.5'),
                ('periodes','BLOB.2'),
                ('budget','BLOB.1'),
                ('dimension','BLOB.1'),
                ('open','BLOB.1'))
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

    def copyOfClient(self):
        """ return a deep copy of this object"""
        t= self.objectToDbTuple()
        return Client(t)

    def __cmp__(self, o2):
        a= cmp(self._name, o2._name)
        if a != 0: return a
        return cmp(self._year, o2._year)
        

        
    # property actions
    
    def setName(self, name):
        if len(name) < 1:
            raise(Model.Exceptions.VarLimit(('varlimit', 'Name')))
        self._name= name
    def getName(self):
        return self._name
    name= property(getName, setName, None, None)

    def setYear(self, year):
        if len(year) != 4 or year < '2000' or year > '2010':
            raise(Model.Exceptions.VarLimit(('varlimit', 'Year')))
        self._year= year
    def getYear(self):
        return self._year
    year= property(getYear, setYear, None, None)

    def setVat(self, vat):
        if vat not in 'YN':
            raise(Model.Exceptions.VarLimit(('varlimit', 'Vat')))
        self._vat= vat
    def getVat(self):
        return self._vat
    vat= property(getVat, setVat, None, None)

    def setRegNum(self, numb):
        if len(numb) < 1:
            raise(Model.Exceptions.VarLimit(('varlimit', 'RegNum')))
        self._regNum= numb
    def getRegNum(self):
        return self._regNum
    regNum= property(getRegNum, setRegNum, None, None)

    def setFirstEntry(self, num):
        try:
            a= int(num)
        except ValueError:
            raise(Model.Exceptions.VarLimit(('varlimit', 'FirstEntry')))
        if a < 1:
            raise(Model.Exceptions.VarLimit(('varlimit', 'FirstEntry')))
        self._firstEntry= num
    def getFirstEntry(self):
        return self._firstEntry
    firstEntry= property(getFirstEntry, setFirstEntry, None, None)
    
    def setPeriodes(self,per):
        if per not in '12346':
            raise(Model.Exceptions.VarLimit(('varlimit', 'Periodes')))
        self._periodes= per
    def getPeriodes(self):
        return self._periodes
    periodes= property(getPeriodes, setPeriodes, None, None)
    
    def setBudget(self, bud):
        if bud not in 'YN':
            raise(Model.Exceptions.VarLimit(('varlimit', 'Budget')))
        self._budget= bud
    def getBudget(self):
        return self._budget
    budget= property(getBudget, setBudget, None, None)
    
    def setDimension(self, dim):
        if dim not in '0123':
            raise(Model.Exceptions.VarLimit(('varlimit', 'Dimension')))
        self._dimension= dim
    def getDimension(self):
        return self._dimension
    dimension= property(getDimension, setDimension, None, None)
    
    def setOpen(self,opn):
        if opn not in 'YN':
            raise(Model.Exceptions.VarLimit(('varlimit', 'Open')))
        self._open= opn
    def getOpen(self):
        return self._open
    open= property(getOpen, setOpen, None, None)

    def getId(self):
        return self._id
    def setId(self,id):
        if id==None: self._id= None
    id= property(getId, setId, None, None)


class ClientList(Model.Gobject.GList):
    """ClientList is based on list and keeps all client-objects.
    """
    _tableName= 'client' ## class dependent

    def __init__(self, database=None):
        """Creates a ClientList, possibly with a related database.<br>
        <b>database</b>: Database name. If given the list will be loaded
        with the data of this database.
        """
        self._objectName= 'Client' ## class dependent
        self._vars= Client._vars
        self._init= Client
        self._database= database
        if database != None:
            self._connection= DbAccess(database)
        else:  # we want a temporary list to keep some objects
            self._connection= None
        Model.Gobject.GList.__init__(self, self._connection)

    def getByDbname(self, n):
        """Return the client object with the given name<br>
        <b>n</b>: The name of the client database<br>
        The database name consists of <tt>gryn_id_yyyy</tt> where <tt>id</tt>
        is the database index of the client. So the client objects id is
        given by the middle part of the name string.
        """
        ndb= string.strip(str(n))
        s= string.split(ndb, '_')
        id= int(s[1])
        for i in self:
            if i.id == id: return i
        return None # if not found


