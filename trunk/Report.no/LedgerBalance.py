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

#import gettext
#t = Model.Global.getTrans()
#if t != None:
#    _= t.gettext
#else:
def _(x):
    return x

#_sourceL= None
_accountL= None
#_cuvenL= None
#_splitL= None
#_lotL= None
#_lotEntryL= None
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



newLine= '\n'

def sortByAccount(a, b):
    return cmp(a.accNum, b.accNum)

class LedgerBalance(object):
    def __init__(self, splitL):
        """Read the neccessary information from object lists and assemble
        the report objects.<br>
        'splitL:' list to be taken into account. Each entry of the list is a
        tuple of a split and a string split date.
        'splitL[0]' is a tuple of information
        for the report generator and can be used to choose among alternative
        formats, sort order etc. The tuple elements are:<br>
        0: Not used<br>
        1: Not used<br>
        2: First periode<br>
        3: Last periode<br>
        """
        global _accountL
        object.__init__(self)
        self.sources=[]
        # Get the object lists
        #_sourceL= Model.Books.getList('source')
        _accountL= Model.Books.getList('account')
        #_cuvenL= Model.Books.getList('cuven')
        #_splitL= Model.Books.getList('split')
        #_lotL= Model.Books.getList('lot')
        #_lotEntryL= Model.Books.getList('lotentry')
        client= Model.Global.getClientObject().name
        year= Model.Global.getClientYear()

        self.parametres= splitL[0] # pick the parametres
        splL= splitL[1:] # the rest is the objects to be reported

        title= 'Ledger balance'
            
        perFrm= self.parametres[2] 
        perTo= self.parametres[3] 
        sums= {}
        self.lines=[]
        # We create one dictionary entry for each referenced account
        # We also make a list of all these  Entries
        for a in splL:
            source, date= a
            try:
                entry= sums[source.account]
            except KeyError:
                entry= Entry(source.account, date)
                sums[source.account]= entry
                self.lines.append(entry)
                
            if source.account < 2: entry.opening= entry.opening + source.value
            if entry.date >= perFrm: entry.perSum= entry.perSum + source.value
            entry.sum= entry.sum + source.value
            entry.yearSum= entry.yearSum + source.value
        # Now we sort the resulting list
        self.lines.sort(sortByAccount)
        if perTo[5:] == '12.31':
            perFrm= None
            perTo= None
        self.pageHeader=PageHeader(title, client, year, perFrm, perTo)
        self.prelude= Prelude(title)
        self.pageFooter= Footer() 
        self.tableHeader= TableHeader()
        self.tableFooter= TableFooter(self.lines)
        self.postlude= Postlude()

    def makeHtml(self):
        """Generate  a html version of the report<b>
        'return:' html version of the report, string
        """
        t= self.prelude.makeHtml()
        t += self.pageHeader.makeHtml()
        t +=self.tableHeader.makeHtml()
        count= 0
        for i in self.lines: # alter background colour
            t += i.makeHtml(_htmlColour[count%2])
            count += 1
        t += self.tableFooter.makeHtml()
        t += self.pageFooter.makeHtml()
        t += self.postlude.makeHtml()
        return t

    def makeTeX(self, fN):
        """Generate a LaTeX version of the report.<br>
        'fN:' File to write tex code to<br>
        'return:' LaTeX-code of the report, string
        """
        t= self.prelude.makeTeX()
        t += self.pageHeader.makeTeX()
        t += self.tableHeader.makeTeX()
        for i in self.lines:
            t += i.makeTeX()
        t += self.tableFooter.makeTeX()
        t += self.pageFooter.makeTeX()
        t += self.postlude.makeTeX()
        fo= open(fN, 'w')
        fo.write(t)
        fo.close()
        return fN





################
# Entry

class Entry(object):
    def __init__(self, accId, date):
        global _accountL
        acc= _accountL.getById(accId)
        self.accNum= acc.num
        self.accName= acc.name
        self.date= date
        self.sum= 0
        self.opening= 0
        self.perSum= 0
        self.yearSum= 0
        
    def makeHtml(self, bgColor):
        mon= Model.Global.intToMoneyZ
        t= \
           '<tr %s>'%bgColor +\
           '<td>%s</td>'%self.accNum +\
           '<td>%s</td>'%self.accName +\
           '<td align="right">%s</td>'%mon(self.opening) +\
           '<td align="right">%s</td>'%mon(self.perSum) +\
           '<td align="right">%s</td>'%mon(self.yearSum) +\
           '<td align="right">%s</td></tr>'%mon(self.sum)
        return t
    
    def makeTeX(self):
        mon= Model.Global.intToTexMoney
        t= r'\Entry{%s}{%s}{%s}{%s}{%s}{%s}'%(self.accNum, self.accName,
                  mon(self.opening), mon(self.perSum), mon(self.yearSum),
                  mon(self.sum)) + newLine
        return t
    
    def getLines(self):
        return 1

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
        t= r'\documentclass{grynLedgerBalance}' + newLine +\
           r'\begin{document}\Mark{%s}'%'Page'+ newLine
        return t
    
############
# TableHeader

class TableHeader(object):
    def __init__(self):
        pass
        
    def makeHtml(self):
        t= '<table width="100%" frame="void" border="0" rules="none" '+\
           'cellspacing="0" cellpadding="2"><tbody>\n' +\
           '<tr><td></td><td></td>' +\
           '<td align="right">%s</td>'%'Opening' +\
           '<td align="right">%s</td>'%'Per mov' +\
           '<td align="right">%s</td>'%'Year mov' +\
           '<td align="right">%s</td></tr>\n'%'Closing'
        return t

        
    def makeTeX(self):
        t= r'\TableHeader{%s}{%s}{%s}{%s}'%(
            'Opening', 'Per mov', 'Year mov', 'Closing') + newLine
        return t

############
# TableFooter

class TableFooter(object):
    def __init__(self, pars):
        self.opening= 0
        self.per= 0
        self.sum= 0
        self.year= 0
        self.sumT= 'Sum'
        for par in pars:
            self.opening= self.opening + par.opening
            self.per= self.per + par.perSum
            self.sum= self.sum + par.sum
            self.year= self.year + par.yearSum
            
    def makeHtml(self):
        mon= Model.Global.intToMoneyZ
        t= '<tr><td></td><td>%s</td>'%self.sumT +\
           '<td align="right">%s</td>'% mon(self.opening) +\
           '<td align="right">%s</td>'% mon(self.per) +\
           '<td align="right">%s</td>'% mon(self.year) +\
           '<td align="right">%s</td></tr>\n'% mon(self.sum)
        return t

        
    def makeTeX(self):
        mon= Model.Global.intToTexMoney
        t= r'\TableFooter{%s}{%s}{%s}{%s}{%s}'%(
            self.sumT, mon(self.opening),
            mon(self.per), mon(self.year), mon(self.sum)) + newLine
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
        t= '</tbody></table>''%s: %s\n'%(self.caption, self.date)
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
