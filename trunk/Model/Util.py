""" $Id$<br>
This file holds functions to do some gui-independent services for the gui.
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

import Model.Global
import Model.Books

def round(amount):
    s= ((amount + 50)/100)*100
    r= amount - s
    return (s, r)


def calcVat(period):
    """
    Sums the VAT accounts and returns a list of net amounts and corresponding
    VAT for each VAT rate<br>
    'period:' The period to handle<br>
    Returns a list, one item for each VAT code:<br>
    'VAT code: ' The VAT code for this item<br>
    'Amount: ' The net sum for this VAT code<br>
    'Amount rounded: ' The rounded sum<br> 
    'VAT: ' The VAT sum <br>
    'VAT rounded: ' The rounded VAT sum
    """
    pers= int(Model.Global.getClientObject().periodes)
    frm, to= Model.Global.periodeNumToDates(period, pers)

    #Find all the source.id's within the time range
    srcIds= []
    sourceL= Model.Books.getList('source')
    for i in sourceL:
        if i.date >= frm and i.date <= to: srcIds.append(i.id)

    #Collect the splits of these sources, i.e. those within the time range
    ourSplitL= Model.Split.SplitList()
    splitL= Model.Books.getList('split')
    for i in splitL:
        if i.source in srcIds and i.vat != ' ':
            ourSplitL.append(i)
    # Found, (we won't use the source.id list anymore)
    srcIds= None
    
    vatL= Model.Books.getList('vat')

    # For each VAT instance go through the splits and
    # sum the amounts and calculate and sum the VATs

    accSum= []  # The results [code, amount, amount rounded, vat, vat rounded]
    for v in vatL:
        code= v.vatCode
        sum= 0.0
        sumVat= 0.0
        if rate: rate= float(v.vatRate)/100.
        else: rate= 0.0
        for s in ourSplitL:
            if s.vat==code:
                if s.side== 'C':
                    sum= sum - s.amount
                    sumVat= sumVat - s.amount*rate
                else:
                    sum= sum + s.amount
                    sumVat= sumVat + s.amount*rate
        accSum.append([v.vatCode, sum, round(sum)[0],
                       sumVat, round(sumVat)[0]])

    return accSum
            

def vatTransfer(period, pendOK, accSum):
    """
    Generates a source for the end of period VAT-related transfers.<br>
    'period:' The period to handle<br>
    'pEndOK:' if !=0: Do not care if today is prior to end of period<br>
    'accSum:' List of calculated sums and VATs generated by calcVat()
    """
    """
    We need to take exact amounts from the VAT-accounts, transfer
    the rounded amounts to the owe account and the accumulated rounding
    to the rounding account

    Todo:
    check if period already transfered. If so: raise exception
    check if pendOK==0 and today is prior to last day of period.
          If so: raise exception
    """
    
    vatL= Model.Books.getList('vat')
    accL= Model.Books.getList('account')
    sumAccount= Model.Global.getAccVatPeriodeSum()
    sumId= accL.getByNum(sumAccount).id
    sumOwe= 0
    rSumOwe= 0 
    newSplitL= Model.Split.SplitList()
    line= 0
    # Make splits to remove amounts from VAT accounts
    for i in accSum:
        code= i[0]
        v= vatL.getByCode(code)
        if v.vatAccount:
            vId= accL.getByNum(v.vatAccount)
            amount= i[3]
            rAmount= i[4]
            s1= Model.Split.Split()
            s1.account= vId
            rSumOwe= rSumOwe + amount
            sumOwe= sumOwe + rAmount
            if amount >= 0:
                s1.side= 'C'
            else:
                s1.side= 'D';
                amount= -amount
            s1.amount= amount
            s1.line= line
            line= line+1
            s1.vat= ' '
            newSplitL.append(s1)
    sumRound= sumOwe - rSumOwe 
    # Make a split to transfer rounded amount to the owe account
    s2= Model.Split.Split()
    s2.account= sumId
    if rSumOwe > 0.0:
        s2.side= 'D'
    else:
        s2.side= 'C'
        rSumOwe= rSumOwe
    s2.amount= rSumOwe
    s2.line= line
    line= line+1
    s2.vat= ' '
    newSplitL.append(s2)


    # At last we make the rounding split
    
    if sumRound != 0: # we must round
        rIdStr= Model.Global.getAccRound()
        rId= accL.getByNum(rIdStr).id
        s3= Model.Split.Split()
        s3.account= rId
        s3.amount= s
        if sumRound > 0:
            s3.side= 'D'
        else:
            s3.side= 'C'
            sumRound= -sumRound
        s3.amount= sumRound
        s3.line= line
        line= line+1
        s3.vat= ' '
        newSplitL.append(s3)

    #We have all splits, so make the source and save
    newSource= Model.Source.Source()
    newSource.id= None
    newSource.ref= sourceL.getNewRef()
    newSource.text= '--- VAT transfer, period %s'%period
    newSource.date= to
    newSource.amount= 0
    newSource.deleted= 'N'
    sourceL.saveEntry(newSource)

    #newSource.id did just get a value, so update the splits accordingly
    for s in newSplitL:
        s.source= newSource.id
        splitL.saveEntry(s)

    return newSource.id # if the GUI thinks that is useful


#This will be in demand around New Years Eve
def YearTransfer(doTransfer):
    return 0

# Does the rounding function work OK for + and - amount?
if __name__== "__main__":

    a= 1250
    s, r= round(a)
    print a, s, r
    a= 1260
    s, r= round(a)
    print a, s, r
    a= 1230
    s, r= round(a)
    print a, s, r

    a= -1250
    s, r= round(a)
    print a, s, r
    a= -1251
    s, r= round(a)
    print a, s, r
    a= -1260
    s, r= round(a)
    print a, s, r
    a= -1230
    s, r= round(a)
    print a, s, r
