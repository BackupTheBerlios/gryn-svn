""" $Id$<br>
These two classes, Gobject and GList, take care of much of the functionality of
the gryn-classes. They are used to read from database, save, delete and
rearrange objects. The gryn object classes inherit from these classes.
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








class Gobject(object):
    """A Gobject inherits from object and is subclassed by all data object
    classes in Gryn.Model.
    """
    def __init__(self, t):
        """The format to print the object and a expression for the arrangement
        of the object's variables into a tuple is generated during
        instantiation."""
        
        object.__init__(self)
        # The following lines should be made global in the subclass.
        # There is no need to keep them with each instance, only with each
        # class. So, move them one day...
        
        # if a database to read from is not specified, make a tuple
        # with all elements set to None and then make an object from that
        if t == None: t= (None,)*len(self._vars)
        self.dbTupleToObject(t)

    def __repr__(self):
        """Prints this object as a colon separated sequence of values"""
        return  self._fmt%self.objectToDbTuple()

    def objectToDbTuple(self):
        """Compiles and evaluates the expression defined during instantiation
        to make a tuple from this object. The compiled expression is cached
        in the object. Returns the tuple.
        """
        return eval(self._cToTuple)
    
    def dbTupleToObject(self, t):
        """Compiles and executes a statement to set the tuple values into
        this object.<br>
        <b>t</b>: The tuple to convert
        """
        exec self._cToObject
        
    # db actions    
    def update(self, db, table):
        """Update this object in the database.<br>
        <b>db</b>: The database connection<br>
        <b>table</b>: The table name
        """
        db.update(table, self._vars, self.objectToDbTuple())
        
    def insert(self, db, table):
        """Insert this object in the database.<br>
        <b>db</b>: The database connection<br>
        <b>table</b>: The table name
        """
        self._id= db.insert(table, self._vars,
                            self.objectToDbTuple())

    def delete(self, db, table):
        """Delete this object from the database.<br>
        <b>db</b>: The database connection<br>
        <b>table</b>: The table name
        """
        db.delete(table, self._id)


    def isEqual(self, o2):
        """Returns 1 if this object and o2 are equal valued, else 0.
        """
        if self.__repr__() == o2.__repr__(): return 1
        return 0

    def __cmp__(o1, o2): # class dependent
        """Compares two object for sort and such, implement this in
        the subclass.
        """
        print 'Model.Gobject:__cmp__Not implemented'


    # property functions, these are all object dependent
    # and are implemented in the subclasses
 

### Gobject List ###



class GList(list):
    """The GList class is the base for all gryn-lists. Each object class is
    defined in a separate file together with the list to hold the object,
    along the lines of this file. See Acount.py for examples of how these
    classes are used. 
    """
    
    def __init__(self, dbc=None):
        """Instantiates a new list of this kind. All data from the
        corresponding database table will be read into the list if a
        database connection is supplied with the call.<br>
        <b>dbc</b>: Database connection
        """
        self._opened= self
        list(self)
        self._connection= dbc
        if dbc != None:
            # Do a select on all columns. Specify each variable names.
            # The table can thereby hold other columns that are irrelevant
            # for this application without causing any disturbances.
            c= dbc.select(self._tableName, self._vars)
            rows= c.fetchall()
            append= self.append
            # and put into list: Use the Gobject init to transform from
            # the row value tuple to Gobject-subclass
            map((lambda r: append(self._init(r))),rows)
        
    def getConnection(self):
        """Return this list's database connection"""
        return self._connection
    connection= property(getConnection, None, None, None)

    def close(self):
        """Close this list. May be useful when tables are stored in
        text files, e.g. XML, to save everything before the application
        terminates.
        """
        self._connection.close()

    def deleteEntry(self, o):
        """Delete an object from the database and this list. The object will
        always be removed from the list. The object is not in the database
        if the object id=None. In this case the database delete is not
        called. <br>
        This function must be reimplemented in some subclasses to confirm
        that the object is not referenced by other objects before it is
        deleted.<br>
        <b>o</b>: The object to delete<br>
        """
        if o.id != None:
            o.delete(self._connection, self._tableName)
        self.remove(o)


    def saveEntry(self, o):
        """Insert the object in this list and database if not already there
        (id=None). Else: update in database and replace in the list. <br>
        <b>o</b>: The object to insert/update
        """
        if o.id == None:
            o.insert(self._connection, self._tableName)
            self.append(o)
        else:
            o.update(self._connection, self._tableName)
            idx= 0
            for i in self:
                if i._id == o._id:
                    self[idx]= o
                    break
                idx= idx + 1
            

    def saveIfChanged(self, obj):
        """This function checks if the object has been modified after it
        was read from the database.<br>
        <b>obj</b>: The object to save<br>
        <b>returns</b>: 1 if changed, 0 if unchanged
        """
        for i in self:
            if i.id == obj.id:
                if i.isEqual(obj):
                    return 0
                else:
                    self.saveEntry(obj)
                    return 1

    def __repr__(self):
        """Print the name of the list, reimplement in subclass"""


