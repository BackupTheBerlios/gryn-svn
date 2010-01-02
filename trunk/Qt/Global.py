""" $Id$<br>
Some global variables and functions for the user interface.
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


import os
from PyQt4 import *
import Model.Global
import Model.Exceptions

def expandImg(name):
    """Returns the full path to the image file 'name'
    """
    return os.path.join(Model.Global.getGrynPath(), 'img/'+name)

class Global(object):
    """Class to hold some global variables.
    """
    # Keep track of some dialogue states:
    #_accTreeWindow= None
    #_customerTreeWindow= None
    #_vendorTreeWindow= None
    # used to pass selected objects from some selection dialogues:
    _listSelected= None
    _opened= None
    
    def __init__(self):
        """Create the class instance
        """
        if Global._opened: #CHIDEP
            print 'Control.Global.Global shall only be opened once'
            a= 1/0 # force error
        Global._opened= self
        object()
        
    #Access functions for the globals above

#def getAccountTreeWindow():
#    """Return the account tree view dialogue
#    """
#    return Global._accTreeWindow

#def setAccountTreeWindow(w):
#    """Set the account tree view dialogue.<br>
#    'w': The dialogue, None when window hidden/closed
#    """
#    Global._accTreeWindow= w

    #accountTreeWindow= property(getAccountTreeWindow, setAccountTreeWindow,
    #                            None, None)
    
## def getCustomerTreeWindow():
##     """Return the customer tree view dialogue
##     """
##     return Global._customerTreeWindow

## def setCustomerTreeWindow(w):
##     """Set the customer tree view dialogue.<br>
##     'w': The dialogue, None when window hidden/closed
##     """
##     Global._customerTreeWindow= w

##     #customerTreeWindow= property(getCustomerTreeWindow, setCustomerTreeWindow,
##     #                             None, None)
    
## def getVendorTreeWindow():
##     """Return the vendor tree view dialogue
##     """
##     return Global._vendorTreeWindow

## def setVendorTreeWindow(w):
##     """Set the vendor tree view dialogue.<br>
##     'w': The dialogue, None when window hidden/closed
##     """
##     Global._vendorTreeWindow= w

##     #vendorTreeWindow= property(getVendorTreeWindow, setVendorTreeWindow,
##     #                           None, None)

def setListSelected(r):
    """Set the list of selected objects so they can be passed around<br>
    'r': The object list 
    """
    Global._listSelected= r

def getListSelected():
    """Return the list of objects.
    """
    return Global._listSelected

    #listSelected= property(getListSelected, setListSelected, None, None)


def dateFieldInit(field, date= None):
    """Set up a date spin box.<br>
    'field': The spin box instance<br>
    'date': Set the field's initial date to this value. Set to
    today if Null, QDate.
    """
    sep= Model.Global.getDateSep()
    field.setAutoAdvance(1)
    field.setSeparator(sep)
    field.setOrder(QDateEdit.YMD)
    field.setMaxValue(QDate(2010,12,31))# Better update the program then 
    field.setMinValue(QDate(2000,1,1))
    if date:
        field.setDate(date)
    else:
        field.setDate(QDate.currentDate())

def strFromQdate(date):
    sep= Model.Global.getDateSep()
    return '%4d%s%02d%s%02d'%(date.year(), sep, date.month(), sep, date.day())


class MissingField(Model.Exceptions.Gryn): 
    """An obligatory form field was empty"""
    def __init__(self, s):
        Model.Exceptions.Gryn.__init__(self, s)
        
