
""" $Id$<br>
This object is a global keeper of parametres and constants used by gryn. The
GUI shall keep its own globals in the Control directory.<p>
There will be several groups of variables here:
<ul>
<li>Hardwired, edit this file to change</li>
<li>Installation specific, edit this file or a property file under 'var/gryn'
    perhaps</li>
<li>User spesific, read from '~/.gryn'</li>
<li>Client specific, store in Client database or a table in the client's
database</li>
</ul>
Anyway, some GUI is needed to help the user<p>
Also, about user roles: There are tree roles defined, but none of this policy
is implemented, all users will act as data base root:
<ul>
<li>'root:' allowed to do anything</li>
<li>'keeper:' allowed to edit anything, but not delete databases or tables</li>
<li>'viewer:' allowed to view everything but not edit. Mainly for report
generation</li></ul>
Access functions ('set..()', 'get..()')for the global variables are
generated on the fly. Therefore
you can not grep for e.g. 'getGrynPath' in this source file.

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
#    The top level file LICENCE holds the verbatim copy of this licence.


#TODO: Translate tool tip texts for the dictionaries
#      Move money related functions to a Money file

import string

import os
import sys
import gettext

#t = getTrans()
t= gettext.translation('gryn', '/home/oao/gryn/var/gryn/locale', ['no'])
if t != None:
    _= t.gettext
else:
    def _(x):
        return x


#def N_(message): return message
def N_(message): return t.gettext(message)
# FIXME: make a Money class one day ...

def moneyToInt(mm):
    """Convert a money string into an int. Moeny strings are only used for
    GUI purposes, int in objects, database and during calculations. This
    function presently works for currencies with two decimal places.<br>
    <b>mm</b>: Money string, i.e. digits, possibly  with an embedded
    decimal sepparator <br>
    <b>Returns</b>: int value
    """
    decSep= getDecSep()
    m= str(mm)
    if len(m) == 0: return 0
    if string.find(m, decSep) >= 0:
        m= string.replace(m, decSep, '.')
    if string.find(m, '.') <0: m= m + '.' + '00'
    elif m[-1] == '.': m= m +'00'
    elif m[-2] == '.': m= m + '0'
    
    s= string.split(m, '.')
    j= s[0]+s[1]
    return int(j) # Can't generate an exception here in a debugged program


    
def intToMoney(i):
    """Makes a money string with two decimal places from an integer.
    Returns an empty string if the value is 0.<br>
    <b>i</b>: The integer representation of money<br>
    <b>Returns</b>: The string representation of money, two decimal places.
    """

    if int(i)==0: return ''
    s= '%s'%i
    if len(s)==1: s='00'+s
    elif len(s)==2: s='0'+s
    s1= s[:-2]
    s2= s[-2:]
    s= string.join([s1, s2], getDecSep())
    return s
    
def intToMoneyZ(i):
    """Makes a money string with two decimal places from an integer.
    Returns '0.00' if the value is 0.<br>
    <b>i</b>: The integer representation of money<br>
    <b>Returns</b>: The string representation of money, two decimal digits.
    """
    if int(i)==0: return '0%s00'%getDecSep()
    s= '%s'%i
    if len(s)==1: s='00'+s
    elif len(s)==2: s='0'+s
    s1= s[:-2]
    s2= s[-2:]
    s= string.join([s1, s2], getDecSep())
    return s

def moneyReformat(m):
    """Returns a properly formatted money string. Returns an empty string
    if the value is zero.<br>
    <b>m</b>: Money string, possibly with an embedded decimal separator.<br>
    <b>returns</b>: Money string, formatted with two decimal digits<br>
    """
    i= moneyToInt(m)
    return intToMoney(i)

def moneyReformatZ(m):
    """Returns a properly formatted money string.<br>
    <b>m</b>: Money string, possibly with an embedded decimal separator.<br>
    <b>returns</b>: Money string, formatted with two decimal digits<br>
    """
    i= moneyToInt(m)
    return intToMoneyZ(i)

def intToTexMoney(i):
    """Formats the value to properly for a LaTeX printout<br>
    <b>i</b>: integer of money value<br>
    <b>returns</b>: string with paranthesis around the decimal separator
    """
    money= intToMoneyZ(i)
    return string.replace(money, getDecSep(), '{%s}'%getDecSep()) 


#### Date functions

def periodeNumToDates(periode, pers):
    """Calculates the first and last date in a periode<br>
    <b>periode</b>: the periode number, string<br>
    <b>pers</b>: How many periodes there is in each year, int<br>
    <b>returns</b>: set of (first date, last date), both strings
    """
    sep= getDateSep()
    per= int(periode)
    step= (12/pers)
    frm= (per-1)*step +1
    to= frm + step - 1
    y= getClientYear()
    dFrom= '%s%s%02d%s01'%(y, sep, frm, sep)
    if to in (1, 3, 5, 7, 8, 10, 12): days= 31
    elif to == 2:
        if int(y)%4 ==0: days= 29
        else: days= 28
    else: days= 30
    dTo= '%s%s%02d%s%02d'%(y, sep, to, sep, days)
    return (dFrom, dTo)

_vars= {    # Global variables
    'grynPath': ('' , N_("The path to the gryn root")),
    'etcPath':('', ''),
    'localePath':('', ''),
    'varPath':('', ''),
    'tmpPath':('', ''),
    'booksConnection':(None, None), #database connection for the client's books
    'booksDbName': (None, None),       #database name for the client's books
    'clientObject': (None, None),      # to save the present client object
    'clientConnection': (None, None), # client database connection
    'clientList': (None, None),        # list of available clients
    'opened': (None, None)             #Singleton sentinel
}

_usrpwd= {   # dictionary of role/password pair sets
    'root': ('root','')        ,
    'keeper': ('keeper', '')   ,
    'viewer': ('viewer', '')
    }

_system= {  # Global options, possibly set from etc/gryn
    'decSep':(',' ,  'Decimal separator in money'), # FIXME:use locale
    'dateSep': ('-' , 'Separator in dates'),
    'appName': ('Qdough' , 'Name of this application'),
    'dbPrefix': ('gryn', 'Database name prefix'),
    'host': ('localhost', 'Name of host running the database'),
    'role': ('root', 'Present role of present user')
    }

_user= {  #User editable options, possibly set from ~/.gryn
    #'locale': (None,'Language, no, se etc'), # Use untranslated if None
    'locale': ('no',N_('Language, no, se etc')), # Use untranslated if None

    # special account numbers, move this to client db
    'accVendor': ('2400',N_('Vendor account')), 
    'accCustomer': ('1500',N_('Customer account')),
    'accVatPeriodeSum': ('2740',N_("Account for period's net VAT")),
    'accRound': ('6999',N_('Account for rounding')),
    'firstCuvenNumber': ('1100', N_('Number assigned to first cuven')) 
    }


def dictGet(dict, key):
    """Return the value of 'key' from the dictionary 'dict'
    """
    return dict[key][0]

def dictSet(dict, key, val):
    """Set the value 'val' into the dictionary 'dict' with key 'key'
    """
    dict[key]= (val, dict[key][1])

def generateGetSet(key, dict):
    """Generates source for 'get<key>()' and 'set<key>(value)' functions
    to access the dictionaries.
    """
    key2= string.upper(key[0])+key[1:]
    return \
     'def get%s(): return dictGet(%s, "%s")\n'%(key2,dict,key) +\
     'def set%s(val): dictSet(%s, "%s", val)\n'%(key2, dict, key)

# generate and compile access functions for the three dictionaries
# e.g. getGryn() and setGryn(value) for dictionary parameter 'gryn' 
for key in _vars.keys():
    s= generateGetSet(key, '_vars')
    f= compile(s, 'f-%s'%key, 'exec')
    exec f

for key in _system.keys():
    s= generateGetSet(key, '_system')
    f= compile(s, 'f-%s'%key, 'exec')
    exec f

for key in _user.keys():
    s= generateGetSet(key, '_user')
    f= compile(s, 'f-%s'%key, 'exec')
    exec f

def readConfigFiles():
    """ read system dictionary entries from etc/gryn and user dictionary
    from $HOME/.gryn
    """
    fn= getEtcPath() + '/gryn'
    try:
        f= open(fn, 'r')
        readFile(f, _system)
        f.close()
    except IOError:
        pass
    fn= os.path.expanduser('~/.gryn')
    try:
        f= open(fn, 'r')
        readFile(f, _user)
        f.close()
    except IOError:
        pass
    
def readFile(f, dict):
    all= f.readlines()
    lc= 0
    for l in all:
        lc= lc + 1
        l= string.split(l, '#') 
        if len(string.strip(l[0]))  < 3: continue
        try:
            key, val= string.split(l[0], '=')
        except ValueError:
            key='*'
        key= string.strip(key)
        if dict.has_key(key):
            val= string.strip(val)
            if val=='None': val= None
            dict[key]= (val, dict[key][1])
        else:
            if key == '*':
                print "Error in line config file line %s"%lc
            else:
                print "Error in config file line %s, unknown parameter '%s'"%(
                    lc, key)
            pass # raise an exception here to signal error in line lc

def writeUserFile():
    fn= os.path.expanduser('~/.gryn')
    f= open(fn, 'w')
    #  pass exception upwards, if can't open file
    for key in _user.keys():
        pars= _user[key]
        f.write(key+'='+str(pars[0])+ ' # ' + pars[1]+'\n')
    

def getVersion():
    return '0.01e-6' 


def getUsrpwd():
    print getRole()
    return (_usrpwd[getRole()][0], _usrpwd[getRole()][1]) 

def getUsrPwdHost():
    return (_usrpwd[getRole()][0],
            _usrpwd[getRole()][1], getHost())

def getTrans():
    if getLocale() != None:
        return gettext.translation('gryn', '/home/oao/gryn/var/gryn/locale', ['no'])


def makeDbName(id):
    for i in getClientList():
        if str(i._id) == str(id):
            n= getDbPrefix() + '_' + str(id) + '_' + str(i.year)
            return n
    return None

def getClientYear():
    return getClientObject().year

def getUserDict():
    return _user

def setUserDict(dict):
    if dict:
        changed= 0
        for key in dict.keys():
            if _user[key][0] != dict[key][0]:
                _user[key]= dict[key]
                changed= 1
        if changed != 0:
            writeUserFile()

def pathFixup(execpath):
    """Called after module load to set the paths to the actual values<br>
    'exepath:' The root path, the path to the Control directory 
    """
    global _vars
    _vars['grynPath']= (execpath, _vars['grynPath'][1])
    _vars['varPath']= (_vars['grynPath'][0]+'/var/gryn',
                         N_('System wide data path'))
    _vars['localePath']= (_vars['grynPath'][0] + '/var/gryn/locale',
                          N_('Locale path'))
    _vars['etcPath']= (_vars['grynPath'][0] + '/etc',
                         N_('System wide etc path'))
    _vars['tmpPath']= (_vars['grynPath'][0] + '/tmp',
                         N_('System wide tmp path'))

    paths= ('varPath','localePath','etcPath', 'tmpPath')
    notfound= 0
    for p in paths:
        path= _vars[p][0]
        if os.path.exists(path) == 0:
            print "The directory '%s' does not exist"%path
            notfound= 1
    if notfound != 0: sys.exit(0)

    
def getAllDicts():
    all= {}
    for k in _system.keys(): all[k]= _system[k]
    for k in _user.keys():   all[k]= _user[k]
    return all


if __name__=='__main__':

    readConfigFiles()
