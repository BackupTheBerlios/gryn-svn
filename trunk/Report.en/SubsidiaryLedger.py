# $Id$

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
import time
import Model.Global
import Model.Books
import Control.Global

#import gettext
#t = Model.Global.getTrans()
#if t != None:
#    _= t.gettext
#else:
def _(x):
    return x

_sourceL= None
_accountL= None
_cuvenL= None
_splitL= None
_lotL= None
_lotEntryL= None
_htmlColour= [' bgcolor="#ffffff"', ' bgcolor="#F5FAFF"']
newLine= '\n'

def dateTimeStrNow():
        """Make a string of current date and time<br>
        'return:' String of date and time: 'yyyy.mm.dd hh:min'
        """
        sep= Model.Global.getDateSep()
        t= time.localtime()
        return '%4d%s%02d%s%02d %02d:%02d'%(
            t[0], sep, t[1], sep, t[2], t[3], t[4])

def sortBySource(a, b):
    return cmp(int(a.srcLot[0].ref), int(b.srcLot[0].ref))


    

##################
# SubsidiaryLedger

class SubsidiaryLedger(object):
    """The SubsidiaryLedger object is used to produce a list of customer
    and vendor relations 
    """
    def __init__(self, objectL):
        """Read the neccessary information from object lists and assemble
        the report objects.<br>
        'objectL:' object collection, 'objectL[0]' is a tuple of information
        for the report generator and can be used to choose among alternative
        formats, sort order etc. Element 0 may contain
        <ul>
        <li>'summary:' Only print the heading for each cuven</li>
        <li>'open:' Print open lots</li>
        <li>'all:'  Print all lots</li>
        """
        global _sourceL, _accountL, _cuvenL, _splitL, _lotL, _lotEntryL
        object.__init__(self)
        self.cuvens= []
        self.fileName= '/tmp/gryn'
        # Read in the object lists
        _sourceL= Model.Books.getList('source')
        _accountL= Model.Books.getList('account')
        _cuvenL= Model.Books.getList('cuven')
        _splitL= Model.Books.getList('split')
        _lotL= Model.Books.getList('lot')
        _lotEntryL= Model.Books.getList('lotentry')
        client= Model.Global.getClientObject().name
        year= Model.Global.getClientYear()

        format= (objectL[0])[0] # pick the format from the first parameter
        objL= objectL[1:] # the rest holds the objects to be reported

        if objL[0].type == 'C':
            title= 'Customers'
        else:
            title= 'Vendors'

        self.pageHeader=PageHeader(title, client, year, None, None)
            
        for cv in objL:
            self.cuvens.append(Cuven(cv, format))
        self.prelude= Prelude(title)
        self.pageFooter= Footer() 
        self.tableHeader= TableHeader()
        self.postlude= Postlude()

    def makeHtml(self):
        """Generate  a html version of the report<b>
        'return:' html version of the report, string
        """
        t= self.prelude.makeHtml()
        t += self.pageHeader.makeHtml()
        t += self.tableHeader.makeHtml()
        count= 0
        for i in self.cuvens: # alter background colour
            t += i.makeHtml(_htmlColour[count%2])
            count= count + 1
        t += self.pageFooter.makeHtml()
        t += self.postlude.makeHtml()
        return t

    def makeTeX(self, fN):
        """Generate a LaTeX version of the report.<br>
        'fN:' Filename to write tex-code to<br>
        'return:' filename
        """
        fo= open(fN, 'w')
        fo.write(self.prelude.makeTeX())
        fo.write(self.pageFooter.makeTeX())
        fo.write(self.pageHeader.makeTeX())
        fo.write(self.tableHeader.makeTeX())
        for i in self.cuvens:
            fo.write(i.makeTeX())
        fo.write(self.postlude.makeTeX())
        fo.close()
        return fN




###############
# Cuven
def N_(s): return s

class Cuven(object):
    def __init__(self, cuven, format):
        global _lotEntryL, _lotL, _cuvenL, _splitL
        lotL=[]
        self.srcLot=[]
        self.year= Model.Global.getClientYear()
        lots= _lotL.getByCuven(cuven.id)
        if len(lots) == 0:
            self.balance= N_('No transactions')
        else:
            balance= 0
            for i in lots:
                balance += i.sum
            self.balance= Model.Global.intToMoneyZ(abs(balance))
        self.number= cuven.num
        self.name= cuven.name
        if len(lots) == 0 : return
        if format == 'all':
            for i in lots:
                lotL.append(i)
        elif format == 'open':
            for i in lots:
                if i.sum != 0: lotL.append(i)
        else: # summary
            pass
        # we now get al the lotEntries and corresponding sources and sort
        # by source ref number. We might also have made a list of
        #lotentry/source lists, one for each lot and sorted each sublist. 
        lotE=[]
        for i in lotL: lotE= lotE + _lotEntryL.getByLot(i.id)
        for i in lotE:
            s= _sourceL.getById(i.source)
            if s: 
                self.srcLot.append(Lot(s, i))
        self.srcLot.sort(sortBySource)
        
    def makeHtml(self, bgColor):
        t= \
           '<tr%s>'%bgColor +\
           '<td width="50"><b>%s</b></td>'%self.number +\
           '<td colspan="3"><b>%s</b></td>'%self.name +\
           '<td align="right"><b>%s</b></td></tr>\n'%self.balance
        for s in self.srcLot:
            t= t+ s.makeHtml(self.year, bgColor)
        return t
    
    def makeTeX(self):
        t= r'\begin{Cuven}' +\
           '{%s}{%s}{%s}'%(self.number, self.name,
                            self.balance) + newLine
        for s in self.srcLot:
            t= t + s.makeTeX(self.year)
        t += r'\end{Cuven}' + newLine
        return t
    

#############
# Lot

class Lot(object):
    def __init__(self, src, lot):
        self.srcLot= (src, lot)

    def makeHtml(self, year, bgColor):
        t= ''
        s, e= self.srcLot
        t += '<tr%s>'%bgColor
        if year==e.year:
            t += '<td>%s</td><td>%s</td><td>%s</td>'%(
                s.ref, s.date, s.text)
        else:
            t += '<td>%s</td><td>%s</td><td>%s</td>'%('', e.year, '')
        if e.side == 'D':
            t += '<td align="right">%s</td><td></td>'% \
                 Model.Global.intToMoneyZ(e.amount)
        else:
            t += '<td></td><td align="right">%s</td>'% \
                 Model.Global.intToMoneyZ(e.amount)
        t+= '</tr>\n'
        return t

    def makeTeX(self, year):
        t= ''

        s, e= self.srcLot
        t += r'\Source'
        if year==e.year:
            t += '{%s}{%s}{%s}'%(
                s.ref, s.date, s.text)
        else:
            t += '{%s}{%s}{%s}'%('', e.year, '')
        if e.side == 'D':
            t += '{%s}{}'%Model.Global.intToMoneyZ(e.amount)
        else:
            t += '{}{%s}'%Model.Global.intToMoneyZ(e.amount)
        t+= '\n'
        return t
        


##############
# Prelude    

class Prelude(object):
    """First part of the report, initial voodoo
    """
    def __init__(self, title):
        """Set up the object<br>
        'title:' The title of the report<br>
        """
        self.title= title

    
    def makeHtml(self):
        """Generate doctype, head, title, body begin tag for html
        'return:' This object's html-version, string
        """
        t='<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN' +\
        '"http://www.w3.org/TR/html4/loose.dtd">\n' +\
        '<html><head><title>%s</title>'%self.title +\
        '<meta http-equiv="Content-Type"\n' +\
        'content="text/html;charset=ISO-8859-1"></head\n>' +\
        '<body>\n' 
        return t
    
    def makeTeX(self):
        """Generate LaTeX-code for preamble:  documentclass, usepackages,
        begin document tag<br>
        'return:' string of the generated code for this object 
        """
        t= r'\documentclass{grynSubsidiaryLedger}' + newLine +\
           r'\begin{document}\Mark{%s}'%'Page'+ newLine
        return t
    
    
################
# PageHeader

class PageHeader(object):
    """The head of each page, prints client name, accounts year, kind of
    report, beginning and end, also an optional logo
    """
    def __init__(self,  txt, client, year, frm= None, to= None, logo= None):
        """Init the PageHeader object<br>
        'txt:' Text describing the kind of report, string<br>
        'client:' Name of the client<br>
        'frm:' First object in this report<br>
        'to:' Last object in this report<br>
        'logo:' to show in page header, use gryn logo if None<br>
        'frm= None' used for a complete report, e.g. a full year, all
        sources.
        """
        self.client= client
        self.year= year
        self.frm= frm
        self.to= to
        self.txt= txt
        self.logo= logo
        
    def makeHtml(self):
        if self.frm:
            t= '<h2>%s %s</h2>'%(self.client, self.year) +\
               '<b>%s, %s - %s</b><p>\n'%(
                self.txt, self.frm, self.to)
        else:
            t= '<h2>%s %s</h2>'%(self.client, self.year) +\
               '<b>%s</b><p>\n'%self.txt
        return t
        
    def makeTeX(self):
        f= ''
        t= ''
        if self.frm: f= self.frm
        if self.to: t= self.to
        t= r'\Head{%s}{%s}{%s}'%(self.client, self.year, self.txt) +\
           r'\FromTo{%s}{%s}'%(f, t) + newLine
        if self.logo:
            t= t + r'\SetLogo{%s}'%self.logo
        else: t= t +\
             r'\SetLogo{%s}'%Control.Global.expandImg('gryn_logo_64.eps')
        return t + newLine


############
# Footer

class Footer(object):
    def __init__(self):
        self.date= dateTimeStrNow()
        self.caption= 'Time of printout'

    def makeHtml(self):
        t= '</table\n>'
        return t

    def makeTeX(self):
        t= r'\Time{%s: %s}'%(self.caption, self.date)
        return t


#############
# Postlude

class Postlude(object):
    def __init__(self):
        self.lastPage= 'Last page '

    def makeHtml(self):
        t= '</body></html>\n'
        return t

    def makeTeX(self):
        t= r'\Mark{%s}'%self.lastPage + newLine
        return t + r'\end{document}' + newLine


#############
# TableHeader

class TableHeader(object):
    def __init__(self):
        pass
    
    def makeHtml(self):
        return '<table width="100%" frame="void" border="0" rules="none" '+\
             'cellspacing="0" cellpadding="2">\n'

    def makeTeX(self):
        return ''
