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

import gettext
t = Model.Global.getTrans()
if t != None:
    N_= t.gettext
else:
    def N_(x):
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


############
# SourceList

class SourceList(object):
    """The SourceList object is used to produce a list of sources
    """
    def __init__(self, objectL):
        """Read the neccessary information from object lists and assemble
        the report objects.<br>
        'objectL:' object collection, 'objectL[0]' is a tuple of information
        for the report generator and can be used to choose among alternative
        formats, sort order etc. If element 0 contains the substring 'splits'
        then the splits of each source will be printed.
        """
        global _sourceL, _accountL, _cuvenL, _splitL, _lotL, _lotEntryL
        object.__init__(self)
        self.sources=[]
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

        self.parametres= objectL[0] # pick the parametres
        format= string.find(self.parametres[0], 'splits')
        objL= objectL[1:] # the rest is the objects to be reported

        # Collect the report objects
        if objL[0] == _sourceL[0] and objL[-1] == _sourceL[-1]:
            frm= None
            to= None
        else:
            frm= objL[0].ref
            to= objL[-1].ref
        title= N_('Source list')
        self.pageHeader=PageHeader(title, client, year, frm, to)
            
        for s in objL:
            self.sources.append(Source(s, format))
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
        for i in self.sources: # alter background colour
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
        fo.write(self.pageHeader.makeTeX())
        fo.write(self.tableHeader.makeTeX())
        for i in self.sources:
            fo.write(i.makeTeX())
        fo.write(self.pageFooter.makeTeX())
        fo.write(self.postlude.makeTeX())
        fo.close()
        return fN




###############
# Source        

class Source(object):
    def __init__(self, source, format):
        global _lotEntryL, _lotL, _cuvenL, _splitL
        lotEntry= _lotEntryL.getBySource(source.id)
        if lotEntry:
            self.lot= _lotL.getById(lotEntry.lot)
            cuven= _cuvenL.getById(self.lot.cuven)
            self.cuvenName= cuven.name
            self.lots= Lots(self.lot.id, source) 
        else:
            self.cuvenName=''
            self.lots= None 
        self.ref= source.ref
        self.date= source.date
        self.deleted= source.deleted
        if self.deleted == 'Y':
            self.text=N_('Deleted')
        else:
            self.text= source.text
        self.splits= []
        if format > 0:
            splits= _splitL.getBySource(source.id)
            for s in splits:
                r= Split(s)
                self.splits.append(r)
        
    def makeHtml(self, bgColor):
        if self.deleted == 'Y':
            t= '<tr%s>'%bgColor +\
            '<td width="50"><b>%s</b></td>'%self.ref +\
            '<td><b>%s</b></td>'%self.text +\
            '<td><b></b></td>' +\
            '<td colspan= "2"><b></b></td></tr>\n'
        else:
            if self.lots: st= self.lots.makeHtml(bgColor)
            else: st= ''
            t= \
            '<tr%s>'%bgColor +\
            '<td width="50"><b>%s</b></td>'%self.ref +\
            '<td><b>%s</b></td>'%self.date +\
            '<td><b>%s</b></td>'%self.cuvenName +\
            '<td colspan= "2"><b>%s</b></td></tr>\n'%self.text
            for s in self.splits:
                t= t+ s.makeHtml(bgColor)
            t= t + st
        return t
    
    def makeTeX(self):
        if self.deleted == 'Y':
            t= r'\begin{Source}' +\
               r'{%s}{%s}{}{}'%(self.ref, self.text) + newLine +\
               r'\end{Source}' + newLine
            
        else:
            if self.lots: st= self.lots.makeTeX()
            else: st= ''
            t= r'\begin{Source}' +\
            r'{%s}{%s}{%s}{%s}'%(self.ref, self.date,
               self.cuvenName, self.text) + newLine
            for s in self.splits:
                t= t + s.makeTeX()
            t= t + st + newLine +\
            r'\end{Source}' + newLine
        return t
    
    def getLines(self):
        if self.deleted == 'Y': return 1
        if len(self.lots) > 0: n= 3
        else: n= 2
        return n + len(self.splits) 

#############
# Lots

class Lots(object):
    def __init__(self, lotId, thisSource):
        global _lotEntryL, _sourceL
        self.text= ''
        if not lotId:
            return
        entries= _lotEntryL.getByLot(lotId)
        ref= [] # collected list of sources of this lot 
        sum= 0
        for e in entries:
            s= _sourceL.getById(e.source)
            if s:
                ref.append(s)
                sum= sum + e.signedAmount()
            else:
                print 'Problem: e.source None:',e.source, e #CHIDEP
        if len(ref) == 1:
            return # this source is a lone entry of the lot
        if ref[0].id == thisSource.id: # this source opened the lot
            if sum == 0:
                T= N_('Setteled by ')
            else:
                T= N_('Partly settled by ')
            for i in ref[1:]:
                T= T  + i.ref + ', '
            T= T[:-2] # remove last comma
            if sum != 0:
               T= T + ' '+ N_('balance')+ \
               ': %s'%Model.Global.intToMoney(abs(sum))
        else: # this source settels the lot wholly or in part
            if len(ref) > 2:
                T= N_('Repayment of')+ ' %s'% ref[0].ref
            else:
                T= N_('Setteling of')+' %s'% ref[0].ref
        self.text= T

    def makeHtml(self, bgColor):
        t= '<tr%s><td></td>'%bgColor +\
           '<td colspan="4">%s</td></tr>'%self.text
        return t

    def makeTeX(self):
        return '\Lot{%s}'%self.text

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
        t= r'\documentclass{grynSourceList}' + newLine +\
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
        self.caption= N_('Time of printout')

    def makeHtml(self):
        t= '</tbody></table>''%s: %s\n'%(self.caption, self.date)
        return t

    def makeTeX(self):
        t= r'\Time{%s: %s}'%(self.caption, self.date)
        return t

############
# Split

class Split(object):
    def __init__(self, split):
        global _accountL
        s= _accountL.getById(split.account)
        self.num= s.num
        self.name= s.name
        if split.side == 'D':
            self.debit= Model.Global.intToMoney(split.amount)
            self.credit= ''
        else:
            self.debit= ''
            self.credit= Model.Global.intToMoney(split.amount)
                
    def makeHtml(self, bgColor):
        t=  '<tr%s>'%bgColor +\
           '<td></td>' +\
           '<td>%s</td>'%self.num +\
           '<td>%s</td>'%self.name +\
           '<td align="right">%s</td>'%self.debit +\
           '<td align="right">%s</td>'%self.credit +\
           '</tr>\n'
        return t

    def makeTeX(self):
        return r'\Split{%s}{%s}{%s}{%s}'%(self.num, self.name, self.debit,
                                  self.credit) + newLine
    


#############
# Postlude

class Postlude(object):
    def __init__(self):
        self.lastPage= N_('Last page ')

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
             'cellspacing="0" cellpadding="2"><tbody>\n'

    def makeTeX(self):
        return ''
