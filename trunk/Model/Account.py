'''  $Id$<br>
Account object holds information on accounts, i.e. account number, account
name, default vat code number and budget.
Budget is not implemented and its
actal value is not relevant, usually set to 0.
See also the documentation of Model.Gobject.Gobject
'''

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
import Model.Global
import Model.Gobject
import Model.Books

def createTable(dataBase):
    """This function is called to create the account table in a new database.
    <br>
    <b>dataBase</b>: The name of the database, chars
    """
    db= Database.DbAccess.DbAccess(dataBase) # 
    db.createTable(AccountList._tableName, Account._varsType)
    db.close()

class Account(Model.Gobject.Gobject):
    """The Account object variables are:<br>
    <b>id</b>: database unique index, None if object not yet saved, int<br>
    <b>num</b>: the account number, 4 digits char<br>
    <b>name</b>: the account name, up to 30 chars<br>
    <b>defVat</b>: the delault VAT, vatCode as defined in Model.Vat.Vat,
    1 digit char<br>
    <b>flags</b>: An int holding flagbits, for special account properties<br>
    <b>budget</b>: the account's budget value, moneyint<br>
    The Account object also have a non-persistant variable:<br>
    <b>used</b>: Initialized to 'N', set to 'Y' if the account is used
    for this client
    """
    # These tuples define the name and type of the columns of the
    # database table. These variable names are also used in the object, but
    # then prepended with an underscore. Check the Database.DbAccess file
    # for the definitions of the types
    
    _varsType= (('id','INDEX.0'),
                ('num','BCHAR.15'),
                ('name','BCHAR.30'),
                ('defVat','BCHAR.1'),
                ('flags', 'INT.0'),
                ('budget','INT.0'))

    # generate a tuple of variables from _varsType
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
        """Account object instansiation<br>
        <b>t</b>: A value tuple representing the object. The new object is
        initialized with these values if given. All variables of the object
        will be set to 'None' if this parameter is 'None'.
        """
        self._used= 'N'
        Model.Gobject.Gobject.__init__(self, t)

    def copyOfAccount(self):
        """Produce a copy of this Account object<br>
        <b>return</b>: The new Account object
        """
        t= self.objectToDbTuple()
        return Account(t)

    def __cmp__(self, o2):
        """The compare function used by 'AccountList.sort()'
        Supports sort by account number
        """
        return  cmp(str(self.num), str(o2.num))

    def cmpAccNum(self, id2):
        a= AccountList.getById(self).num
        b= AccountList.getById(self).num
        return cmp(a, b)
        
        
    # property actions
    
    def setName(self, name):
        if len(name) < 1:
            raise(Model.Exceptions.VarLimit(('varlimit', 'Name')))
        self._name= name
    def getName(self):
        return self._name
    name= property(getName, setName, None, None)

    def setNum(self, num):
        try:
            a= int(num)
        except ValueError:
            raise(Model.Exceptions.VarLimit(('varlimit', 'Num')))
        if len(num) != 4 and len(num) != 1:
            raise(Model.Exceptions.VarLimit(('varlimit', 'Num')))
        self._num= num
    def getNum(self):
        return self._num
    num= property(getNum, setNum, None, None)

    def setDefVat(self, vat):
        """'vat:' 1 digit char"""
        s= '0123456789'
        if vat not in s: 
            raise(Model.Exceptions.VarLimit(('varlimit', 'Vat')))
        self._defVat= vat
    def getDefVat(self):
        return self._defVat
    defVat= property(getDefVat, setDefVat, None, None)
    
    def setBudget(self, bud):
        if len(str(bud)) < 1:
            raise(Model.Exceptions.VarLimit(('varlimit', 'Budget')))
        self._budget= bud
    def getBudget(self):
        return self._budget
    budget= property(getBudget, setBudget, None, None)
    
    def setUsed(self, u):
        self._used= u
    def getUsed(self):
        return self._used
    used= property(getUsed, setUsed, None, None)
    
    def getId(self):
        return self._id
    def setId(self, id):
        if id == None: 
            self._id= id
    id= property(getId, setId, None, None)

class AccountList(Model.Gobject.GList):
    """AccountList is a list that holds Account instances.
    See also the documentation of Model.Gobject.GList
    """

    vatItems= 0
    _tableName= 'account' # Used by createTable 
    _accountHash= {} # (account number: account object) hash, for faster
                     # account number search
                     
    def __init__(self, database=None):
        """Make an 'AccountList' object.<br>
        <b>database</b>: Name of the database where this table is. If not
        'None': read in data from database, else produce an empty list
        """
        #self._objectName= 'Account' #
        self._vars= Account._vars    # used in GList.__init__()
        self._init= Account          # used in GList.__init__()
        self._database= database
        if database != None: # prepare to read data from db into this list
            self._connection= Database.DbAccess.DbAccess(database)
        else:
            self._connection= None
        # init list and possibly read from database
        Model.Gobject.GList.__init__(self, self._connection)
        
    def fixup(self, x):
        """Called from 'Model.Books' after all lists have been read from
        the database. Hook do do any linking etc. 'x' is the list dictionary
        """
        self.sort()
        for i in self: # insert into the dictionary
            AccountList._accountHash[i.num]= i
        AccountList.vatItems= len(Model.Books.getList('vat'))
        splitL= Model.Books.getList('split')
        for i in splitL:
            self.getById(i.account)

    def getById(self, id):
        '''Search for account with a given index<br>
        <b>id</b>: Index to search for
        <b>return</b>: The wanted account object or 'None' if not found
        '''
        for i in self:
            if i._id == id:
                # The account must be active if being searched for, so...
                i._used= 'Y'
                return i
        return None
    
    def getByNum(self, num):
        '''Search for account with a given number<br>
        <b>num</b>: Account number to search for
        <b>return</b>: The wanted account object or 'None' if not found
        '''
        #if len(num) == 0: return None
        try:
            return AccountList._accountHash[num]
        except KeyError:
            return None


    def isUsed(self, o):
        '''Check if the account instance o is used. Do not delete if in use.
        Only splits points to accounts<br>
        <b>o</b>: The Account object to check<br>
        <b>return</b>: 0 if not used, 1 if used
        '''
        splitL= Model.Books.getList('split')
        for i in splitL:
            if i.account == o.id: return 1
        return 0

    def saveEntry(self, o):
        '''Save the account instance in the database and update the
        account dictionary too.<br>
        <b>o>/b>: Account object to save
        '''
        AccountList._accountHash[o.num]= o
        Model.Gobject.GList.saveEntry(self, o)
            
    def deleteEntry(self, o):
        '''Delete the instance o from the database if this account is
        not in use. Remember to remove from dictionary too.
        Return 0 if actually deleted, return 1 if in use and therefore
        was not deleted<br>
        <b>o</b>: Account object to delete
        '''
        if self.isUsed(o) == 0:
            del AccountList._accountHash[o.num]
            Model.Gobject.GList.deleteEntry(self, o)
            return 0
        else:
            return 1
        

    def __repr__(self):
        """Produce a string representation of this object, the simplest is to
        just return the list name.
        """
        return 'AccountList'

