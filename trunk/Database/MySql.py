""" $Id$<br>
Subclass of SqlBase to access MySQL gryn databases.
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


import MySQLdb
import Database.SqlBase
import Model.Global
import sys
import Model.Exceptions

# MySQLdb class 'connection' may throw NotSupportedError or ProgrammingError


class DbAccess(Database.SqlBase.SqlBase):
    """Create one DbAccess instance for each database"""
    def __init__(self, dbName):
        """Make the object.<br>
        'dbName:' The name of the database, string<br>
        """
        Database.SqlBase.SqlBase.__init__(self, dbName)
        #self.__dbName= dbName
        #self.__user, self.__passwd, self.__host= Model.Global.getUsrPwdHost()

        try:
            self._connection= \
                           MySQLdb.connect(host=self._host, user=self._user,
                           passwd=self._passwd, db=dbName)
            self._cursor= self._connection.cursor()
        except:
            Model.Exceptions.raiser(sys.exc_info())
        
        
        
    def insert(self, table, vars, values):
        """Insert one row into the database table<br>
        'table:' Table name, string<br>
        'vars:' a tuple of variable names, strings<br>
        'values:' a tuple of corresponding variable values<br>
        'return:' The unique table index of this object 
        """
        s= "INSERT INTO %s ( "%table 
        for i in vars:
            s= "%s %s,"%(s,i)
        s= s[:-1]+') VALUES ('
        for i in values:
            s= "%s '%s',"%(s,i)
        s= s[:-1]+')'
        
        try:
            self._cursor.execute(s)
        except:
            Model.Exceptions.raiser(sys.exc_info())
        return self._cursor.lastrowid


if __name__ == '__main__':
    dbg= 1
    print 'MySql'
    Model.Global.Global()
    db= DbAccess('GrynTest')
    db.dropDataBase('createTest')
    db.createDataBase('createTest')
    db2= DbAccess('createTest')
    db2.createTable('testTable',(('id','INDEX.0'),('val','BCHAR.10')))
    db2.insert('testTable',('id', 'val'),('None', '123'))
    db2.insert('testTable',('id', 'val'),('None', '234'))
    db2.insert('testTable',('id', 'val'),('None', '345'))
    db2.delete('testTable', 2)
    db2.update('testTable', ('id', 'val'),('3', '333'))
    cur= db2.select('testTable', ('id', 'val'))
    rows= cur.fetchall()
    if rows[0][0]==1 and str(rows[0][1])=='123' and \
       rows[1][0]==3 and str(rows[1][1])=='333' and len(rows)==2:
        print '**OK**'
    print rows
    db2.close()
    db.dropDataBase('createTest')
    db.close()
    
