"""$Id$<br>
This file holds the parts used to import the invoice queue. An invoice object
and related list are defined, and also a function to do the import.
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
import Model.Global
import Model.Gobject
import Model.Books    
import Model.Source
import Model.Split
import Model.Lot
import Model.LotEntry

import gettext

t = Model.Global.getTrans()
if t != None: _ = t.gettext
else:
    def _(x):
        return x



def createTable(dataBase):
    db= Database.DbAccess.DbAccess(dataBase)
    db.createTable(InvqueList._tableName, Invque._varsType)
    db.close()

class Invque(Model.Gobject.Gobject):
    """The Invque object contains these variables read from the database
    table:<br>
    <b>id</b>: The object's unique database table index, int<br>
    <b>invNum</b>: The invoice number, &le;10 chars<br>
    <b>cuven</b>: Customer database table index<br>
    <b>date</b>: Invoice date, 10 chars<br>
    <b>net</b>: The invoice net amount, moneyint<br>
    <b>vat</b>: The vat-amount, moneyint. If 0: No VAT accounting.<br>
    <b>vatCode</b>:The VAT-variant, 1 char digit, irrelevant if vat=0. <br>
    <b>ref</b>: Some possible reference number, e.g. related to bank
    statements or some transaction numbers, &le;15 chars<br>
    <b>text</b>: The text to be entered as the resulting source text
    """
    
    _varsType= (('id','INDEX.0'),
                ('invNum','BCHAR.10'),
                ('cuven', 'INT.0'),
                ('date', 'BCHAR.10'),
                ('net', 'INT.0'),
                ('vat', 'INT.0'),
                ('vatCode', 'BCHAR.1'),
                ('ref', 'BCHAR.15'),
                ('text', 'BCHAR.30')
                )

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
        
    def copyOfInvque(self):
        t= self.objectToDbTuple()
        return Invque(t)


    def __cmp__(o1, o2):
        return  cmp(o1._invNum, o2._invNum)

    #def cmpInvNum(self,  other):
    #    return cmp(self._invNum, other._invNum)

        
    # property actions
    
    def setCuven(self, c):
        self._cuven= c
    def getCuven(self):
        return self._cuven
    cuven= property(getCuven, setCuven, None, None)
    
    def setInvNum(self, c):
        self._invNum= c
    def getInvNum(self):
        return self._invNum
    invNum= property(getInvNum, setInvNum, None, None)

    def setText(self, c):
        self._text= c
    def getText(self):
        return self._text
    text= property(getText, setText, None, None)

    def setDate(self, c):
        self._date= c
    def getDate(self):
        return self._date
    date= property(getDate, setDate, None, None)

    def setRef(self, c):
        self._ref= c
    def getRef(self):
        return self._ref
    ref= property(getRef, setRef, None, None)

    def setNet(self, c):
        self._net= c
    def getNet(self):
        return self._net
    net= property(getNet, setNet, None, None)

    def setVat(self, c):
        self._vat= c
    def getVat(self):
        return self._vat
    vat= property(getVat, setVat, None, None)

    def setVatCode(self, c):
        self._vatCode= c
    def getVatCode(self):
        return self._vatCode
    vatCode= property(getVatCode, setVatCode, None, None)

    def getId(self):
        return self._id
    def setId(self, dummy):
        self._id= None
    id= property(getId, setId, None, None)


### InvqueList ###


class InvqueList(Model.Gobject.GList):
    """List to hold Invque objects"""
    _tableName= 'invque' ## class dependent

    def __init__(self, database=None):
        self._objectName= 'Invque'
        self._vars= Invque._vars
        self._init= Invque
        self._database= database
        if database != None:
            self._connection= Database.DbAccess.DbAccess(database)
        else:
            self._connection= None
        Model.Gobject.GList.__init__(self, self._connection)

    def fixup(self,lists):
        self.sort()

    
    def __repr__(self):
        return 'InvqueList'


    def importInvoices(self, logList):
        """This function is called from the user interface or some
        command line program to import the queue. A GUI is not needed to
        get this task done. The invoice queue table was read into this list
        when the list was instantiated.<br>
        <b>LogList</b>: We report back to the caller an entry in this list
        for each imported invoice.
        """
        # First we need access to other lists to enable proper import
        sourceL= Model.Books.getList('source')
        splitL= Model.Books.getList('split')
        accountL= Model.Books.getList('account')
        lotL= Model.Books.getList('lot')
        lotEntryL= Model.Books.getList('lotentry')
        vatL= Model.Books.getList('vat')
        # After we have imported an entry we remove it from the InvqueList
        # so loop until the list is empty
        while len(self) > 0:
            splits= []
            invoice= self[0]
            txt= invoice.text
            if not txt or len(txt) == 0:
                t= _('Outgoing invoice number ') #Default text if none given
                txt= t + '%s'%invoice.invNum
            # Make a new Source instance
            source= Model.Source.Source((None, sourceL.getNewRef(),
                txt, invoice.date, 0, 'N'))
            # And then make the necessary splits
            line= 0 # split number
            vatObj= vatL.getByCode(invoice.vatCode)
            if vatObj.vatRate == None: # This invoice is without any VAT
                accNum= vatObj.salesAccount
                split= Model.Split.Split((None, None,
                   accountL.getByNum(accNum).id,'C',invoice.net, line))
                splits.append(split)
            else:
                accNumVat= vatObj.vatAccount
                accNumSale= vatObj.salesAccount
                acc= accountL.getByNum(accNumSale).id #Id of sales account
                split= Model.Split.Split((None, None, acc, 'C',
                                          invoice.net, line))
                splits.append(split)
                line= line + 1
                acc= accountL.getByNum(accNumVat).id # id of VAT account
                split= Model.Split.Split((None, None, acc, 'C',
                                          invoice.vat, line))
                splits.append(split)
            line= line + 1
            lotAmount= invoice.net + invoice.vat
            accNum= Model.Global.getAccCustomer() # trade debtors account
            acc= accountL.getByNum(accNum).id
            split= Model.Split.Split((None, None, acc, 'D',
                                      lotAmount, line))
            splits.append(split)

            #save
            
            # begin database transaction, some day...

            sourceL.saveEntry(source) # and get source.id set

            for split in splits:
                split.source= source.id
                splitL.saveEntry(split)
            lot= Model.Lot.Lot()
            lot.cuven= invoice.cuven
            lot.sourceTxt= source.text 
            lot.sourceDate= source.date
            lot.sourceRef= source.ref
            lot.sourceAmount= lotAmount
            lotL.saveEntry(lot) # and get lot.id set

            lotEntry= Model.LotEntry.LotEntry()
            lotEntry.lot= lot.id
            lotEntry.source= source.id
            lotEntry.amount= lotAmount
            lotEntry.side= 'D'
            lotEntry.year= Model.Global.getClientYear()
            lotEntryL.saveEntry(lotEntry)

            #end database transaction

            # report information to the caller
            logList.append((source, lot, invoice))
            #delete invoice from queue and database table.
            self.deleteEntry(invoice)
        # Finished, and the database table is now empty too



################################## Test code
if __name__ == '__main__':
    import sys
    import Model.Client
    #import Model.Global
    #import Model.Books
    
    dbName= 'gryn_20_2003' # or any other database
    if 'create' in sys.argv: # create the database table
        createTable(dbName)
    elif 'drop' in sys.argv: # delete the database table
        db=  Database.DbAccess.DbAccess(dbName)
        db.dropTable('invque')
        db.close()
    else: # fill some invoices into  the database table
        clientList= Model.Client.ClientList('gryn')
        Model.Global.setClientList(clientList)
        Model.Global.setClientConnection(clientList.getConnection())
        Model.Books.readBooks(string.split(dbName, '_')[1])
        cL= Model.Books.getList('cuven')
        l= Model.Books.getList('invque')
        id= 3
        a= Invque((None, 45, id, '2003.08.12', 1200045,1200,'4','1245', ''))
        l.saveEntry(a)
        a= Invque((None, 50, id, '2003.08.11', 1200050,1201,'4','1250', ''))
        l.saveEntry(a)
        a= Invque((None, 46, id, '2003.08.12', 1200046,1000,'3','1246', ''))
        l.saveEntry(a)
        a= Invque((None, 47, id, '2003.08.13', 1200047,1001,'3','1247',
                   'Tekst 47' ))
        l.saveEntry(a)
        a= Invque((None, 49, id, '2003.08.14', 1200049, 0, None, '1249', ''))
        l.saveEntry(a)
        a= Invque((None, 48, id, '2003.08.15', 1200048,0,None, '1248', ''))
        l.saveEntry(a)
        l.sort()
        print
        for i in l:
            print i
