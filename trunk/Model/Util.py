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

def vatTransfer(period, pendOK):
    """
    Generates a source for the end of period VAT-related transfers.<br>
    'period:' The period to handle<br>
    'pEndOK:' if !=0: Do not care if today is prior to end of period
    """
    caption='Periode VAT transfers'
    # Todo:
    # check if period already transfered. If so: raise exception
    # check if pendOK==0 and today is prior to last day of period.
    #     If so: raise exception
    # if no relevant sources found: raise exception
    # We should take out pieces and write two new functions:
    # getSales, roughly snippet A:  getVATs, roughly snippet B
    
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
        if i.source in srcIds:
            ourSplitL.append(i)
    # Found, (we won't use the source.id list anymore)
    
    vatL= Model.Books.getList('vat')
    accL= Model.Books.getList('account')

    # collect amounts for sales accounts, snippet A
    # This is actually only needed to generate a VAT statement
    #We should consider the sides here
    saleAccs= {}
    for i in vatL:
        a= i.salesAccount
        if a:
            id= accL.getByNum(a).id        
            saleAccs[id]= 0

    for i in ourSplitL:
        if saleAccs.has_key(i.account):
            amnt= i.amount
            if i.side=='C': amnt= -amnt
            saleAccs[i.account]= saleAccs[i.account] + amnt
    for k in saleAccs.keys():
        print k, saleAccs[k]
    
    # Then collect the VAT amounts, snippet B
    # This would be much easier if we had tagged the splits with
    # the VAT code. Do that one day...
    vatAccs= {}
    for i in vatL:
        a= i.vatAccount
        if a:
            id= accL.getByNum(a).id        
            vatAccs[id]= 0

    for i in ourSplitL:
        if vatAccs.has_key(i.account):
            amnt= i.amount
            if i.side=='C': amnt= -amnt
            vatAccs[i.account]= vatAccs[i.account] + amnt
    for k in vatAccs.keys():
        print k, vatAccs[k]
    
    # Now we can generate the splits
    sumAccount= Model.Global.getAccVatPeriodeSum()
    sumOwe= 0
    sumId= accL.getByNum(sumAccount).id
    newSplitL= Model.Split.SplitList()
    line= 0
    for v in vatL:
        #First the remove from VAT account split 
        sIdStr= v.vatAccount
        if sIdStr: sId= accL.getByNum(sIdStr).id
        else: continue
        amount= vatAccs[sId]
        if amount == 0: continue
        s1= Model.Split.Split()
        s1.account= sId
        sumOwe= sumOwe + amount
        if amount >= 0:
            s1.side= 'C'
        else:
            s1.side= 'D';
            amount= -amount
        s1.amount= amount
        s1.line= line
        line= line+1
        s1.vat= ''

        #Then the corresponding add to owe-account split 
        newSplitL.append(s1)
        s2= Model.Split.Split()
        s2.account= sumId
        s2.amount= s1.amount
        if s1.side== 'C':
            s2.side= 'D'
        else:
            s2.side= 'C'
        s2.line= line
        line= line+1
        s2.vat= ''
        newSplitL.append(s2)


    # At last we need a rounding split pair too
    
    s, r= round(sumOwe)
    if r != 0: # If we must round
        s3= Model.Split.Split()
        s3.account= sumId
        if r >= 0:
            s3.side= 'C'
        else:
            s3.side= 'D';
            r= -r
        s3.amount= r
        s3.line= line
        line= line+1
        s3.vat= ''
        newSplitL.append(s3)

        rIdStr= Model.Global.getAccRound()
        rId= accL.getByNum(rIdStr).id
        s4= Model.Split.Split()
        s4.account= rId
        s4.amount= s3.amount
        if s3.side== 'C':
            s4.side= 'D'
        else:
            s4.side= 'C'
        s4.line= line
        line= line+1
        s4.vat= ''
        newSplitL.append(s4)
            
    #We have all splits, so make the source and save
    newSource= Model.Source.Source()
    newSource.ref= sourceL.getNewRef()
    newSource.text= '--- VAT transfer, periode %s'%period
    newSource.date= to
    newSource.amount= 0
    newSource.deleted= 'N'
    sourceL.saveEntry(newSource)

    #newSource.id did just now get a value, so update the splits accordingly
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
