""" $Id$<br>
Grep is a class for searching text strings by a regular expression.
This is useful for the GUI.
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
import re

class Grep(object):
    """ Grep is a class for regular expression search for text strings in
    list objects. The search string may be found enywhere in the target string.
    Specify that the search string must be at the beginning or end of target
    string by using ^ and $ as usual for regular expressions.
    """

    def __init__(self, list, field, skip= '0'):
        """Instantiate a Grep object.<br>
        <b>list</b>: The list to search<br>
        <b>field</b>: The name of the object variable to search in<br>
        <b>skip</b>: The search functions tests all objects search by
        this expression. If the expression is true the object is skipped.
        """
        self._list= list
        #The regexp specifies: case insensitive, find anywhere in string
        self._if= compile('rex.search(string.lower(i.%s))'%field,
                          '<string>', 'eval')
        self._skip= compile(skip,  '<string>', 'eval')
        self._field= compile('s.%s'%field, '<string>', 'eval')
        self._prevLen= 0
        self._firstMatch= None

    def _doGrep(self, s):
        """Do a grep, this is a local function<br>
        <b>s</b>: the regular expression to serach for, usually a plain
        string<br>
        <b>return</b>: a tuple: (the first string found, number of strings
        found).<br>
        BUG: 'ÆØÅ' are case sensitive, latin-1 lower() doesn't work
        for non-ascii. Will UTF8 codec help here?
        """
        reS= string.lower(s)
        if len(reS)==0: return (None, 0)
        rex= re.compile(reS)
        found= 0
        first= None
        for i in self._list:
            if eval(self._skip): continue
            if eval(self._if):
                if not first: first= i
                found= found+1
        return (first, found)

    def grepInput(self, stxt):
        """Search for a string satisfying the regexp stxt.<br>
        A colon may be embedded in this string. Only the part before the colon
        should be considered.<br>
        <b>stxt</b>: regexp string [:irrelevant chars], string.<br>
        <b>return</b>: Depending on state:<br>
        (1) regexp string shorter than in previous call:
        (stxt, length of
        regexp string)<br>
        (2) no target found: (regexp string, length of regexp string)
        <br>
        (3) several target found: (regexpstring:first targetstring
        found, length of regexp string)<br>
        (4) one target found: (target string , -1)
        """
        txt= str(stxt)
        if string.find(txt, ':') >= 0: # remove the last part
            st= string.split(txt, ':')
            g= string.strip(st[0])
            #n= string.strip(st[1])
        else:
            g= string.strip(txt)
            #n= ''
        if len(g) < self._prevLen: # problem if we do search while the
            # user deletes from search string
            self._prevLen= len(g)
            return stxt, len(g)      # (1)
        self._prevLen= len(g)
        s, m= self._doGrep(g)
        if m == 0:
            self._firstMatch= None
            rs= g + ' : '
            return rs, len(g)        # (2)
        if s:
            self._firstMatch= s
            if m != 1:
                rs= g+' : '+ eval(self._field)
                return rs, len(g)    # (3)
            else:
                return s, -1         # (4)

    def getFirstMatch(self):
        """Returns the first target string of the matching
        target strings found during the last search.
        """
        return self._firstMatch
        

# The following is only for testing

if __name__ == '__main__':

    class D(object):
        """A class used for testing only"""
        def __init__(self, str):
            self._name= str

        def getName(self):
            return self._name
        def setName(self, s):
            self._name= s
        name= property(getName, setName, None, None)

    import sys
    ss=[]
    ss.append(D('first'))
    ss.append(D('second'))
    ss.append(D('third'))
    ss.append(D(None))
    ss.append(D('first'))
    g= Grep(ss, 'name', 'i.name==None')
    rs= ''
    leng= 0
    while(1):
        t= sys.stdin.readline()
        rs, leng= g.grepInput(t)
        if leng >= 0:
            print rs, leng
        else:
            print rs.name
            
