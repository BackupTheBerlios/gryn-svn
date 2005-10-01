""" $Id$<br>
Filter exceptions from the gryn functions and reraise new exceptions with
better application related types. All exceptions generated within gryn should
be routed through these classes
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

class Gryn(Exception):
    """Catch all exceptions rised by gryn, this is the base class"""
    def __init__(self, c):
        Exception.__init__(self)
        self.args= c

class Unknown(Gryn):
    """Default exception"""
    def __init__(self, c):
        Gryn.__init__(self, c)
    
class DbError(Gryn):
    """Exceptions related to database"""
    def __init__(self, a):
        Gryn.__init__(self, a)

class VarLimit(Gryn):
    """Used when property functions detect errors"""
    def __init__(self, s):
        Gryn.__init__(self, s)

class FileError(Gryn):
    """Used for file open, read, syntax etc"""
    def __init__(self, s):
        Gryn.__init__(self, s)
        
class ThisCannotHappen(Gryn):
    """Hm..."""
    def __init__(self, s):
        Gryn.__init__(self, s)

def raiser(info):
    """Filter system exceptions, mainly to produce more meaningful
    messages from exceptions generated in libraries gryn call.<br>
    <b>info</b>: Information string, usually from sys.exc_info()
    """
    
    exc= str(info[0])
    c= str(info[1])
    #print "exc:<%s> c:<%s>"%(exc, c)
    causeNum= str(c[0])
    if len(c)>1: cause= str(c[1:])
    else: c= ''
    if string.find(exc, '_mysql_') >= 0:
        if string.find(exc, 'Warning') >= 0:
            print exc,c
            return
        if   string.find(causeNum, '1146')>=0:
            x= DbError(cause)
        elif   string.find(causeNum, '1049')>=0: # unknown database
            x= DbError(cause)
        elif string.find(causeNum, '2005')>=0:
            x= DbError("I do not know the host")
        elif string.find(causeNum, '2003')>=0:
            x= DbError("No connection with host")
        elif string.find(causeNum, '2002')>=0:
            x= DbError("Server is down")
        elif string.find(causeNum, '1044')>=0:
            x= DbError("Wrong user")
        elif string.find(causeNum, '1045')>=0:
            x= DbError('Wrong password')
        elif string.find(exc, 'OperationalError')>=0:
            x= DbError('Operational error')
        elif string.find(exc, 'ProgrammingError')>=0:
            x= DbError('Programming error')
        elif string.find(exc, 'exists')>=0:
            x= DbError('Exists')
        else:
            print exc, c
            x= DbError("Unknown")
    else:
        print exc, c
        x= Unknown(exc+causeNum+cause)

    raise x
