""" $Id$<br>
The sources organize the information needed to generate the accounting
books. The Source object subclass Gobject and the SourceList subclass GList.
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
import Model.Global
import Model.Gobject
import Model.Account

import gettext

t = Model.Global.getTrans()

if t != None: _ = t.gettext
else:
    def _(x):
        return x

def createTable(dataBase):
    db= Database.DbAccess.DbAccess(dataBase)
    db.createTable(SourceList._tableName, Source._varsType)
    db.close()

class Source(Model.Gobject.Gobject):
    """Source object variables are: <br>
    <b>id</b>: The source unique database table index, int<br>
    <b>ref</b>: The source reference number. This is incremented for each
    new source. &le;10 chars<br>
    <b>text</b>: The text or caption of the source, &le;30 chars<br>
    <b>date</b>:The source date, in ISO format yyyy.mm.dd, 10 chars<br>
    <b>amount</b>: not used, moneyint<br>
    <b>deleted</b>: 'Y' if deleted, 'N' else. 1 char
    """
    
    _varsType= (('id','INDEX.0'),
                ('ref','BCHAR.10'),
                ('text','BCHAR.30'),
                ('date','BCHAR.10'),
                ('amount','INT.0'),
                ('deleted', 'BCHAR.1'))
    
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
        
    def copyOfSource(self):
        t= self.objectToDbTuple()
        return Source(t)

    def __cmp__(self, o2): # sort by reference number
        if len(self._ref) > len(o2._ref): return 1
        elif len(self._ref) < len(o2._ref): return -1
        return  cmp(self._ref, o2._ref)

    def cmpDate(self, o2): #compare the dates
        return cmp(self.date, o2.date)

        
    # property actions
    
    def setRef(self, ref):
        self._ref= ref
    def getRef(self):
        return self._ref
    ref= property(getRef, setRef, None, None)

    def setText(self, a):
        self._text= a
    def getText(self):
        return self._text
    text= property(getText, setText, None, None)

    def setDate(self, s):
        self._date= s
    def getDate(self):
        return self._date
    date= property(getDate, setDate, None, None)
    
    def setAmount(self, a):
        self._amount= a
    def getAmount(self):
        return self._amount
    amount= property(getAmount, setAmount, None, None)

    def getId(self):
        return self._id
    def setId(self, dummy):
        self._id= None
    id= property(getId, setId, None, None)
    
    def getDeleted(self):
        return self._deleted
    def setDeleted(self, v):
        self._deleted= v
    deleted= property(getDeleted, setDeleted, None, None)



### SourceList ###

class SourceList(Model.Gobject.GList):
    _tableName= 'source' ## class dependent

    def __init__(self, database=None):
        self._objectName= 'Source' ## class dependent
        self._vars= Source._vars
        self._init= Source
        self._database= database
        
        if database != None:
            self._connection= Database.DbAccess.DbAccess(database)
        else:
            self._connection= None
        Model.Gobject.GList.__init__(self, self._connection)
        self.sort()

    def fixup(self, lists):
        pass

    def NotUsedgetByRef(self, ref):
        """Get the source with the given reference number<br>
        <b>ref</b>: reference number, chars<br>
        <b>return </b>: The wanted source, or None if not found
        """
        for i in self:
            if i._ref == ref:
                return i
        return None

    def getById(self, id):
        """Get the source with the given index<br>
        <b>id</b>: index, int<br>
        <b>return </b>: The wanted source, or None if not found
        """
        for i in self:
            if i._id == id:
                return i
        return None

    def deleteEntry(self, o):
        """Delete the object from the source list and database. Only delete
        object if last in list. If not last in list the object is kept but
        marked as deleted.<br>
        <b>o</b>: The object to delete
        """
        if o.ref != self[-1].ref:# not last in list
            o.deleted= 'Y'
            o.text= "--- Deleted"
            Model.Gobject.GList.saveEntry(self, o)

        elif o.id != None: # is last and saved in db
            Model.Gobject.GList.deleteEntry(self, o)

        else: # last and not saved in db. Can this happen? No
            print "Source:deleteEntry: This can't happen"
            self.remove(o)

    #def saveEntry(self, o):
        """Save a source object. If the object already exists in the
        database the database is updated, else the object is inserted<br>
        <b>o</b>: Source object to save
        """
        #if o.id == None:
        #    o.insert(self._connection, self._tableName)
        #    self.append(o)
        #else: # should we do a list.replace here too? 
        #    o.update(self._connection, self._tableName)

    def getNewRef(self):
        """Generates the next number to use for source reference.<br>
        <b>return</b>: The lowest available number, chars
        """
        hi= 0 # we should set this from firstEntry in the clientobject
        for i in self:
            ii= int(i._ref)
            if ii > hi: hi= ii
        return  str(hi + 1)

    def sortBySourceNum(self):
        """Sort the source list by the source reference numbers"""
        self.sort()
        
    def sortByDate(self):
        """Sort this source list by date"""
        self.sort(Source.cmpDate)

    def __repr__(self):
        return 'SourceList'

    def addOpeningBalance(self, dbName):
        """This function generates the first two sources when opening the
        books at the beginning of a new year. The first source is used by
        automatic transfer from one year to the other. The second source is
        reserved for manual opening postings.<br>
        <b>dbName</b>: The name of the new database
        """
        year= string.split(dbName, '_')[2]
        sep= Model.Global.getDateSep()
        s= Source()
        s.ref= '0'
        s.text= _('Opening balance, generated by program')
        s.date='%s%s01%s01'%(year, sep, sep)
        s.amount= 0
        s.deleted= 'N'
        self.saveEntry(s)
        s= Source()
        s.ref= '1'
        s.text= _('Opening balance, manual corrections')
        s.date='%s%s01%s01'%(year, sep, sep)
        s.amount= 0
        s.deleted= 'N'
        self.saveEntry(s)
        
