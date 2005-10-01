""" $Id$<br>
This module imports chart of accounts into the account-database table.
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
import Model.Account
import Model.Global
import Model.Exceptions

def importGapl(fileN):
    """Import Gryn-chart-of-accounts. This chart is a textfile ('fileN'),
    the usual  
    extension is 'gapl', and the file is probably located in 
    the  'var/gryn' directory (specified by 'Model.Global._varPath').
    Each account is
    represented by one line in this file. Fields are separated by a colon,
    the fields are:<br>
    'account number:account name:default vat code'<br>
    The vat code is a single digit char specifying the defaut VAT of this
    account per definition of 'vatCode' in the 'Model.Vat.Vat' class.
    The file can hold lines with any account number, but only those accounts
    with 1 or 4 digit account numbers will be imported. The 1 digit accounts
    act as account group headings. 
    """
    db= Model.Global.getBooksConnection()
    if db== None: #CHIDP
        print 'Book-database not open'
        return
    fi= open(str(fileN), 'r')
    # Get a new account list. This function should only be run when
    # creating a client. Further imports will add new components to the
    # list and may lead to double entries. Bad
    accountL= Model.Books.getList('account')

    #Read in all lines from the gapl-file
    lines= fi.readlines()
    lNum= 1
    #First we find the top level accounts, i.e. those with 1-digit number
    for line in lines:
        sline= string.strip(line)
        if len(sline) < 3 or sline[0]=='#': continue
        try:
            elm= string.split(sline, ':')
        except ValueError:
            raise(Model.Exceptions.FileError(_(
                "Syntax error in VAT file line %d:"%lNum)+'\n'+line))
        if len(elm) != 3:
            raise(Model.Exceptions.FileError(_(
                "VAT file line %d do not have three fields:"%lNum)+'\n'+line))
        else:
            num= string.strip(elm[0])
            if len(num)!= 1: continue
            nam= string.strip(elm[1])
            # Make a new account object instance
            a= Model.Account.Account()
            a.num= num
            a.name= nam
            a.defVat= '0'
            a.flags= 0
            a.budget= 0
            # and save in database
            accountL.saveEntry(a)
    #Now we can find the 4-digit accounts. These are the real accounts
    for line in lines:
        elm= string.split(string.strip(line), ':')
        if len(elm) != 3:
            pass
        else:
            num= string.strip(elm[0])
            if len(num)== 1: continue
            nam= string.strip(elm[1])
            vat= string.strip(elm[2])
            a= Model.Account.Account()
            a.num= num
            a.name= nam
            a.defVat= vat
            a.flags= 0
            a.budget= 0
            accountL.saveEntry(a)
    fi.close()

    #We now have the heading accounts at the lowest db-indexes

