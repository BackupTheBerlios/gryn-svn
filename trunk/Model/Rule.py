"""$Id$<br>
Rules can be used to simplify and speed up accounting of often used
transactions or seldom used, but complicated ones. A rule consists of three
parts: definition of input parametres,  calculations and a posting stage.
These are all defined using python syntax. We will need a sandbox here...<p>
Rules are also a subclass of Gobject and the corresponding list is RuleList.
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
import string
import Model.Gobject
import Model.Split

def createTable(dataBase):
    db= Database.DbAccess.DbAccess(dataBase)
    db.createTable(RuleList._tableName, Rule._varsType)
    db.close()

class Rule(Model.Gobject.Gobject):
    """The rule's variables:<br>
    <b>id</b>: The rule's unique index from the database table, int<br>
    <b>name</b>: The name of this rule, &le;30 chars<br>
    <b>text</b>:The default text of the generated source, &le;30 chars<br>
    <b>parametres</b>:A colon separated line of entries. Each entry is a
    string consisting of a parameter name=parameter description;valuetype.
    Parameter name is a short name usable in a program, parameter description
    is useful for the user interaction and valuetype is 'M' if the
    corresponding value is of type money, &le;255 chars<br>
    <b>prelude</b>: A python snippet for some optional calculations, lines
    are combined into a semi colon separated string, &le;255 chars<br>
    <b>postings</b>: How the postings are to be done. A line with colon
    saparated parts, one part for each posting. The posting part is a
    semicolon separated list of accountindex, side ('D' or 'C') and a
    python function to execute when the rule is run, &le;255 chars<br>
    """
    _varsType= (('id','INDEX.0'),
                ('name','BCHAR.30'),
                ('text','BCHAR.30'),
                ('parametres','BLOB.100'), 
                ('prelude','BLOB.200'),
                ('postings', 'BLOB.200'))

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
        
    def copyOfRule(self):
        t= self.objectToDbTuple()
        return Rule(t)

    def __cmp__(self, o2):
        return  cmp(self._name, o2._name)

        
    # property actions

    def setName(self, name):
        self._name= name
    def getName(self):
        return self._name
    name= property(getName, setName, None, None)
    
    def setText(self, text):
        self._text= text
    def getText(self):
        return self._text
    text= property(getText, setText, None, None)
    
    def setParametres(self, parametres):
        self._parametres= parametres
    def getParametres(self):
        return self._parametres
    parametres= property(getParametres, setParametres, None, None)
    
    def setPrelude(self, prelude):
        self._prelude= prelude
    def getPrelude(self):
        return self._prelude
    prelude= property(getPrelude, setPrelude, None, None)
    
    def setPostings(self, postings):
        self._postings= postings
    def getPostings(self):
        return self._postings
    postings= property(getPostings, setPostings, None, None)
    
    def getId(self):
        return self._id
    def setId(self, dummy):
        self._id= None
    id= property(getId, setId, None, None)

    def runRule(self, varValues, splits):
        """This method executes the code of  this rule. Parametres:<br>
        <b>varValues</b>: a semi colon separated string of variable-value
        pairs. For example 'net=12300;vat=2300'<br>
        <b>splits</b>: A splitList to append the generated splits to<br>
        <b>return</b>: A tuple (errorcode, list of splits). The errorcode is
        'S' when all went good, 'E' if an error occurred during execution.
        Execution errors should not happen when running debugged rules.
        """
        
        # begin to assemble the python program of the rule
        #First the parametres and the prelude statements
        prg= ''
        if varValues:
            varPrg= string.replace(varValues, ';', '\n')
            prg= prg + '#parametres\n' +  varPrg+ '\n'
        if len(self.prelude) > 0: 
            pr= string.split(self.prelude, ';')
            pr= string.join(pr, '\n')
            prg= prg + '#prelude\n'+ pr + '\n'
        try:
            exec(prg) # run the first two parts of the rule
        except: # may happen if user wrote a wrong program
            print 'Rule execution error during definition part'
            return ('E', None)

        # Now the postings
        posts= string.split(self.postings, ":")
        line= 0
        for post in posts:
            accId, side, function= string.split(post, ';')
            # now we know the function to apply, the account to which the
            # result shall be posted and if on the debit or credit side.
            # Any parametres used by the function must have been defined 
            # by the execution of prg above. 
            try:
                val= str(eval(function))
                if string.find(val, '.') >= 0:
                    val= string.replace(val, '.', Model.Global.getDecSep())
                print 'calc val: ', val
            except: # should not happen in a debugged program
                print 'Rule execution error during split part'
                return ('E', None)
            # make a new split
            ival= Model.Global.moneyToInt(val)
            split= Model.Split.Split((
                None, None, accId, side, ival, line, 0))
            line= line + 1
            splits.append(split)
        return ('S', splits)


### RuleList ###


class RuleList(Model.Gobject.GList):
    _tableName= 'rule' ## class dependent
    _objectName= None
    def __init__(self, database=None):
        self._objectName= 'Rule' ## class dependent
        self._vars= Rule._vars
        self._init= Rule
        self._database= database
        if database != None:
            self._connection= Database.DbAccess.DbAccess(database)
        else:
            self._connection= None
        Model.Gobject.GList.__init__(self, self._connection)

    def fixup(self,lists):
        pass

    def getById(self, rid):
        """Find the rule with the given index<br>
        <b>rid</b>: The unique index of the sought rule<br>
        <b>return</b>: the found rule object or 'None' if not found
        """
        for i in self:
            if i._id== rid: return i
        return None

    def __repr__(self):
        return 'RuleList'

