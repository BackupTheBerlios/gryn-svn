""" $Id$<br>
Base class for accessing the databases of gryn. The database may be a
SQL-database or some flat files like XML. The latter case is problematic
because gryn assumes that each object is saved and updated on the fly just
after being edited. Subclass this class for different databases to take care
of database incompatabilities. 
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


import sys
import Model.Global
import Model.Exceptions
import string


class SqlBase(object):
    """Create one DbAccess instance for each database"""
    def __init__(self, dbName):
        """Make the object.<br>
        'dbName:' The name of the database, string<br>
        """
        object.__init__(self)
        self._dbName= dbName
        self._user, self._passwd, self._host= Model.Global.getUsrPwdHost()

        
    def close(self):
        """Close the database connection, any other close-activity too
        """
        self._connection.close()

    def dropTable(self, table):
        """Remove 'table' from the database<br>
        'table:' Name of the table to remove, string
        """
        try:
            self.execute("DROP TABLE IF EXISTS %s"%table)
        except:
            Model.Exceptions.raiser(sys.exc_info())
            

    def createTable(self, table, varType):
        """Create a new table with specified column names and data types<br>
        'table:' Name of the new table<br>
        'varType:' A tuple of (variable name, variable type) tuples
        """
        s= 'CREATE TABLE %s ('%table
        for i in varType: 
            s= s+ ' '+ i[0]
            u= string.split(i[1],'.')
            type= u[0]
            l= u[1]
            if type== 'INDEX':
                s= s+' INT NOT NULL PRIMARY KEY AUTO_INCREMENT,'
            elif type=='BLOB':
                #s= s + ' TINYBLOB,'
                s= s + ' VARCHAR(%s),'%l
            elif type=='BCHAR':
                s= s + ' CHAR(%s) BINARY,'%l
            elif type=='INT':
                s= s + ' INT,'
            elif type=='NONE':
                pass
            else:
                print "wrong table specifier %s"%type
        s= s[:-1]+ ')'
        try:
            self.execute("DROP TABLE IF EXISTS %s"%table)
            self.execute(s)
        except:
            Model.Exceptions.raiser(sys.exc_info())

    def createDataBase(self, name):
        """Create a new database<br>
        'name:' Database name, string
        """
        try:
            self.execute("CREATE DATABASE IF NOT EXISTS %s"%name)
        except:
            Model.Exceptions.raiser(sys.exc_info())
            
    def dropDataBase(self, name):
        """Remove a database<br>
        'name:' Database name, string
        """
        try:
            self.execute("DROP DATABASE IF EXISTS %s"%name)
        except:
            Model.Exceptions.raiser(sys.exc_info())
            
        
    def insert(self, table, vars, values):
        """Insert one row into the database table. The way to get the index
        of the new row differs among database systems, so this method is
        allways subclassed<br>
        'table:' Table name, string<br>
        'vars:' a tuple of variable names, strings<br>
        'values:' a tuple of corresponding variable values<br>
        'return:' The unique table index of this object
        """
        pass
    
    def delete(self, table, id):
        """Delete one row in a database table<br>
        'table:' Name of the table, string<br>
        'id:' Unique index of the roe to delete, int
        """
        s= 'DELETE FROM %s WHERE id= %s'%(table, id)
        try:
            self._cursor.execute(s)
        except:
            Model.Exceptions.raiser(sys.exc_info())


    def update(self, table, vars, values):
        """Update on row in a database table<br>
        'table:' Name of database table, string<br>
        'vars:' tuple of variable names, strings<br>
        'values:' tuple of corresponding values<br>
        The index must sit in vars[0], values[0]
        """
        s= 'UPDATE %s SET '%table
        for i in range(1, len(vars)):
            s= "%s %s='%s',"%(s, vars[i], values[i])
        s= s[:-1] + 'WHERE id= %s'%values[0]
        try:
            self._cursor.execute(s)
        except:
            Model.Exceptions.raiser(sys.exc_info())
        
        
    def select(self, table, vars, where= None):
        """Select a set of rows<br>
        'table:' Name of database table to select from<br>
        'vars:' Tuple of column names, strings<br>
        'where:' Selection criterium, default value 'None'. 'where=None'
        selects all rows<br>
        'return:' The cursor pointing to the relult of this select
        """
        s= 'SELECT'
        for i in vars:
            s= "%s %s,"%(s, i)
        s= s[:-1]
        s= s + ' FROM %s'%table
        if where != None: s= s +' WHERE '+ where
        try:
            a= self._cursor.execute(s)
        except:
            Model.Exceptions.raiser(sys.exc_info())
        return self._cursor


    def execute(self, str):
        """Execute a SQL command<br>
        'str:' SQL command to execute, sting<br>
        'return:'The selections cursor
        """
        return self._cursor.execute(str)
        

    
