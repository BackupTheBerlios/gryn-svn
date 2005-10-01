""" $Id$<br>
These functions read the tables of the database into lists.
Any missing table is created. The tables represent data for
the books of the client.
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
import Database.DbAccess
import Model.Exceptions
import Model.Account
import Model.Split
import Model.Source
import Model.Cuven
import Model.Lot
import Model.LotEntry
import Model.Rule
import Model.Invque
import Model.Vat

_bookLists= None # This is a hash of tablename:table of the lists

def readBooks(id):
    """Read in objects from tables and run init-functions on them.<br>
    <b>id</b>: The client's database id
    """
    global _bookLists
    # Create database name
    dbName= Model.Global.makeDbName(id)
    Model.Global.setBooksDbName(dbName)
    #open Database
    conn= Database.DbAccess.DbAccess(dbName)
    Model.Global.setBooksConnection(conn)
    # create a new dictionary in case one already exists from a prev client
    _bookLists= {}
    # name all tables to read
    lists= ('account', 'split', 'source', 'cuven', 'lot', 'lotentry', 'rule',\
            'invque', 'vat')
    # read the tables, possibly create too
    for t in lists:
        readOrCreate(dbName, t)

    # For each list we call its fixup function for possible initialisations
    for t in lists:
        L= _bookLists[t]
        L.fixup(_bookLists)


def readOrCreate(dbName, table):
    """Try to read a table. Creates the table if a database-exception
    is raised. <br><b>dbName</b>:The name of the database to read from<br>
    <b>table</b>:The name of the table to read.
    """
    global _bookLists
    #The Class name and directory are equal to the table name, but first
    # char is capital
    n= string.capitalize(table)
    if n == 'Lotentry': n= 'LotEntry'

    # r is the list class instance maker
    r= 'Model.%s.%sList("%s")'%(n, n, dbName)
    try:
        L= eval(r) # try to create the instance, implicitly read from db
    except Model.Exceptions.DbError: # not found, create
        c= 'Model.%s.createTable("%s")'%(n, dbName)
        eval(c)
        L= eval(r)
        if table=='source': # add opening sources
            L.addOpeningBalance(dbName)
    _bookLists[table]= L # register the result


def close():
    """ Close all the open book tables. Calls the close method of the lists
    """
    global _bookLists
    if not _bookLists: return
    lists= _bookLists.values()
    for i in lists:
        i.close()
    _bookLists= None

def getList(name):
    """ Returns the list object, none if unknown.
    <br><b>name</b>: The name of the list
    """
    global _bookLists
    if _bookLists.has_key(name):
        return _bookLists[name]
    return None


def createDatabase(name):
    """Create a new database to hold a new client's tables.
    <br><b>name</b>: The name of the database to create
    """
    try: # to open the database
        conn= Database.DbAccess.DbAccess(name)
    except Model.Exceptions.DbError, s:
        # First we check for exceptions we are not concerned about here
        if string.find(str(s), 'Operational') < 0:
            raise # nothin more to do here, reraise the exception
        # We got a Operational-exception, i.e. the data base does not excist
        # use the db connection we have for the client database
        conn= Model.Global.getClientConnection()
        conn.createDataBase(name)
        bconn= Database.DbAccess.DbAccess(name)
        Model.Global.setBooksConnection(bconn)
        return
    #We got no exception. The database already excists. This problem arise
    # if the data base is inconsistent, the client is registered in the
    # client table but the client's database has not been created or has
    # been deleted by an error
    conn.close()
    Model.Global.setBooksConnection(None)
    raise Model.Exceptions.DbError("exists") # to tell about our problem

    
