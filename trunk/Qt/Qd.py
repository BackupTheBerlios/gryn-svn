#!/usr/bin/env python
"""$Id$<br>
This is the main program setting up the application form and menues.
The main statements at the end of this file sets up the application and inits
the program to a state where a client can be chosen.
This file is handwritten and not generated from a ui-file.
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


#BUGS: 
#The tree-windows are not garbage collected when closed, perhaps they are
#pointed to by Qt-signals. Find out about this and fix.

    
import sys
import os
from qt import *

#print "path: ", sys.path
p= os.path.split(os.path.abspath(os.path.dirname(sys.argv[0])))
sys.path= [p[0]] + sys.path
#print "p: ", p[0]
#print "path: ", sys.path
import Model.Global

#Find the application absolute path and calculate the dir above. Prepend
#this path to the system path so the interpreter will find our modules.
#Must do it here before Control modules are imported in the main func below.
MyExecPath= p[0]
import Control.Global
Model.Global.pathFixup(MyExecPath)
Model.Global.readConfigFiles()

import Control.Client
import Control.Source
import Control.AccountTree
import Control.ListSelect
#import Control.Global
import Control.Account
import Control.SourceFind
import Control.Cuven
import Control.CuvenTree
import Control.CuvenSelect
import Control.SourceSelect
import Control.SourceVat
import Control.ReportGen
import Control.TimeFrameSelect
import Control.MDIWindow
import Control.Rule
import Control.Queue
import Control.Configtable
import Control.Vat

#Some application states to help enable/disable menues and their entries
stateEvents={
    'clientIsOpen':0,      # Set while a client is open
    'clientsAvailable': 0  # Set when the client table is not empty(first use)
    }


def appIcon(): # The application icon to be shown at the top left corner
    #return os.path.join(Model.Global.getGrynPath(), 'img/gryn_logo_16.png')
    return Control.Global.expandImg('gryn_logo_16.png')
def bgImage(): # The background image of the empty central window
    return Control.Global.expandImg('gryn_bg.png')


def menuSetup(slf, name, action, text):
    """Generates code for menu action<br>
    'name:' The name of the menu<br>
    'action:' The action of the menuitem<br>
    'text:' The text will appear on the item<br>
    Returns the new action object when the generated program is run. 
    """
    
    o= slf # to satify pychecker
    s= 'slf.%s%sAction = QAction(slf,"%s%sAction")\n'%(
        name, action, name, action) +\
    'o= slf.%s%sAction\n'%(name, action) +\
    'o.addTo(slf.%sMenu)\n'%(name) +\
    'slf.connect(o,SIGNAL("activated()"),slf.%s%s)\n'%(name, action) +\
    'o.setMenuText("%s")\n'%(text)
    c= compile(s, 'menuSetup-%s%s'%(action,name), 'exec') 
    exec c
    return o

def menuDecorate(slf, path= None, accel=None, tooltip=None):
    """Adds icon, acceleration key and/or tooltip to a menu action
    'path:' filename of the icon<br>
    'accel:' The acceleration key, e.g. Qt.CTRL+Qt.Key_K<br>
    'tooltip:' The tooltip text, will appear on the window status line
    """
    if path and len(path)>1:
        ic= QIconSet(QPixmap(Control.Global.expandImg(path)))
        if ic: slf.setIconSet(ic)
    if tooltip and len(tooltip)>0: slf.setToolTip(tooltip)
    if accel: slf.setAccel(accel)

    
    
class Qd(QMainWindow):
    """The main window of the application. Defines all menues, menue items
    and actions.
    """
    #TODO: Define accellerator keys
    
    def __init__(self,parent = None,name = None,fl = 0):
        """This sets up the menues etc.
        """
        QMainWindow.__init__(self,parent,name,fl)
        self.statusBar() # we do have a status bar here, but it is not used yet
        self.parent= parent
        
        if not name:
            self.setName("Qd")

        f = QFont(self.font())
        # Maybe font and size should be configurable in a setup dialogue.
        f.setPointSize(12)
        self.setFont(f)
        self.setCaption(Model.Global.getAppName())
        self.menubar = QMenuBar(self,"menubar")

        ### Menu definitions

        #CLIENT menu
        #===========
        self.clientMenu = QPopupMenu(self)
        self.connect(self.clientMenu, SIGNAL(
            "aboutToShow()"), self.clientAboutToShow)

        o= menuSetup(self,'client','New', self.tr('New','client'))
        menuDecorate(o, "folder_new.png", None, 'Lager en ny klient')
        menuSetup(self,'client','Open', self.tr('Open', 'client'))
        menuSetup(self,'client','Edit', self.tr('Edit'))
        menuSetup(self,'client','Delete', self.tr('Delete'))
        menuSetup(self,'client','Close', self.tr('Close'))
        self.clientMenu.insertSeparator()
        menuSetup(self,'client','Exit', self.tr('Exit'))

        self.menubar.insertItem(self.tr("Client"),self.clientMenu,0,0)

        #Account Menu
        #============
        
        #Todo: add handler for aboutToShow
        self.accountMenu = QPopupMenu(self)
        menuSetup(self,'account','New', self.tr('New', 'account'))
        menuSetup(self,'account','Edit', self.tr('Edit'))
        menuSetup(self,'account','Delete', self.tr('Delete'))

        self.menubar.insertItem(self.tr("Account"),self.accountMenu,1, 1)

        #Customer/Vendor Menu
        #====================
        
        #Todo: add handler for aboutToShow
        self.cuvenMenu = QPopupMenu(self)
        self.customerMenu= self.cuvenMenu
        self.vendorMenu= self.cuvenMenu
        
        menuSetup(self,'customer','New', self.tr('New customer', 'customer'))
        menuSetup(self,'customer','Edit', self.tr('Edit customer'))
        menuSetup(self,'customer','Delete', self.tr('Delete customer'))
        self.cuvenMenu.insertSeparator()
        menuSetup(self,'vendor','New', self.tr('New vendor', 'vendor'))
        menuSetup(self,'vendor','Edit', self.tr('Edit vendor'))
        menuSetup(self,'vendor','Delete', self.tr('Delete vendor'))


        self.menubar.insertItem(self.tr("Cuven"),self.cuvenMenu, 2, 2)



        #Source Menu
        #===========

        
        self.sourceMenu = QPopupMenu(self)
        menuSetup(self,'source','New', self.tr('New', 'source'))
        menuSetup(self,'source', 'Edit', self.tr('Edit'))
        menuSetup(self,'source', 'View', self.tr('View'))
        menuSetup(self,'source', 'Delete', self.tr('Delete'))
        menuSetup(self,'source', 'Find', self.tr('Find'))
        menuSetup(self,'source', 'Invque', self.tr('Import invoices'))
        menuSetup(self,'source', 'Vat', self.tr('VAT transfer'))

        self.menubar.insertItem(self.tr("Source"),self.sourceMenu, 3, 3)

        #Rule menu
        #=========
        
        self.ruleMenu = QPopupMenu(self)
        menuSetup(self,'rule','New', self.tr('New', 'rule'))
        menuSetup(self,'rule','Edit', self.tr('Edit'))
        menuSetup(self,'rule','Delete', self.tr('Delete'))


        self.menubar.insertItem(self.tr("Rules"),self.ruleMenu, 4, 4)


        #Report Menu
        #===========
        
        self.reportMenu = QPopupMenu(self)

        menuSetup(self,'report','SourceList', self.tr('Source list'))
        menuSetup(self,'report','LedgerBalance', self.tr('Ledger balance'))
        menuSetup(self,'report','SubsLedger', self.tr('Subs. ledger'))


        self.menubar.insertItem(self.tr("Report"),self.reportMenu, 5, 5)


        #Window Menu
        #===========
        
        self.windowMenu = QPopupMenu(self)
        self.windowMenu.setCheckable(1)
        self.connect(self.windowMenu, SIGNAL(
            "aboutToShow()"), self.windowAboutToShow)

        o=menuSetup(self,'window','AccountTree', self.tr('Account tree'))
        o.setToggleAction(1)
        o=menuSetup(self,'window','CustomerTree', self.tr('Customer tree'))
        o.setToggleAction(1)
        o=menuSetup(self,'window','VendorTree', self.tr('Vendor tree'))
        o.setToggleAction(1)


        
        self.accTreeObject= None
        self.customerTreeObject= None
        self.vendorTreeObject= None
        
        self.menubar.insertItem(self.tr("Window"), self.windowMenu, 6, 6)


        #Configuration Menu
        #==================

        self.configMenu = QPopupMenu(self)
        self.connect(self.configMenu, SIGNAL(
            "aboutToShow()"), self.configAboutToShow)

        menuSetup(self,'config','Edit', self.tr('Edit'))
        menuSetup(self,'config','View', self.tr('View all'))
        menuSetup(self, 'config','VatAcc', self.tr('VAT accounts'))

        self.menubar.insertItem(self.tr("Config"),self.configMenu, 7, 7)


        # HELP menu
        #==========
        
        self.helpContentsAction = QAction(self,"helpContentsAction")
        self.helpIndexAction = QAction(self,"helpIndexAction")
        self.helpAboutAction = QAction(self,"helpAboutAction")

        self.helpMenu = QPopupMenu(self)
        self.helpContentsAction.addTo(self.helpMenu)
        self.helpIndexAction.addTo(self.helpMenu)
        self.helpMenu.insertSeparator()
        self.helpAboutAction.addTo(self.helpMenu)
        self.menubar.insertItem(self.tr("Help"),self.helpMenu)

        self.connect(self.helpIndexAction,SIGNAL("activated()"),
                     self.helpIndex)
        self.connect(self.helpContentsAction,SIGNAL("activated()"),
                     self.helpContents)
        self.connect(self.helpAboutAction,SIGNAL("activated()"),self.helpAbout)

        #self.helpContentsAction.setText(self.tr("Contents"))
        self.helpContentsAction.setMenuText(self.tr("Contents"))
        #self.helpContentsAction.setAccel(QString.null)

        #self.helpIndexAction.setText(self.tr("Index"))
        self.helpIndexAction.setMenuText(self.tr("Index"))
        #self.helpIndexAction.setAccel(QString.null)

        #self.helpAboutAction.setText(self.tr("About"))
        self.helpAboutAction.setMenuText(self.tr("About"))
        #self.helpAboutAction.setAccel(QString.null)

        self.resize(QSize(561,456).expandedTo(self.minimumSizeHint()))

        ### Work space
        ##############
        
        self.vb = QVBox( self )
        self.vb.setFrameStyle( QFrame.StyledPanel | QFrame.Sunken )
        self.ws = QWorkspace( self.vb)
        self.ws.setScrollBarsEnabled(1)
        self.ws.setPaletteBackgroundPixmap (QPixmap(bgImage()))
        self.setCentralWidget(self.vb)

        ### connect the state event handler
        self.connect(self,PYSIGNAL("stateEvent"), self.stateEventHandler)

        ### end of init


    ### Signal handlers


    
    def stateEventHandler(self, s):
        """Triggered by the 'stateEvent' signal. Updates states
        stored in stateEvents.<br>
        's': The action, string
        """
        if s == 'opened':
            stateEvents['clientIsOpen']= 1
            for i in range(1, 7): #Enable menues
                w.menubar.setItemEnabled(i, 1)
        elif s == 'closed':
            stateEvents['clientIsOpen']= 0
            for i in range(1, 7): #Disable menues
                w.menubar.setItemEnabled(i, 0)
        elif s == 'notAvailable':
            stateEvents['clientsAvailable']= 0
        elif s == 'available':
            stateEvents['clientsAvailable']= 1

    # Some of the following dialogues emit signals ment for other open
    # dialogues.
    # For example: An editAccount dialogue emits a account-signal carrying
    # information about the changed object and if the object was edited,
    # new or deleted. Such signals are catched here and reemitted.
    # The dialogues wanting to connect to these signals can therefore
    # always connect to this form instead of keeping track of the dialogues
    # originally emitting the signal.

    # Client actions
    #===============

    def clientAboutToShow(self):
        """Enables and disables some menuitems according to if any client
        is open and if any client is available at all.
        Called with click on client menu. BUG: Creating first client
        should enable several items, as for now one must exit and restart
        to get open, edit, delete enabled
        """
        if stateEvents['clientIsOpen']!=0: #client is open
            self.clientNewAction.setEnabled(0)
            self.clientOpenAction.setEnabled(0)
            self.clientEditAction.setEnabled(0)
            self.clientCloseAction.setEnabled(1)
            self.clientDeleteAction.setEnabled(0)
            self.clientExitAction.setEnabled(0)
        else:
            if stateEvents['clientsAvailable']!=0: #One or more clients
                self.clientNewAction.setEnabled(1)
                self.clientOpenAction.setEnabled(1)
                self.clientEditAction.setEnabled(1)
                self.clientCloseAction.setEnabled(0)
                self.clientDeleteAction.setEnabled(1)
                self.clientExitAction.setEnabled(1)
            else:
                self.clientNewAction.setEnabled(1) #No clients available
                self.clientOpenAction.setEnabled(0)
                self.clientEditAction.setEnabled(0)
                self.clientCloseAction.setEnabled(0)
                self.clientDeleteAction.setEnabled(0)
                self.clientExitAction.setEnabled(1)


    def clientNew(self):
        """Opens a ClientNew dialogue.
        """
        c= Control.Client.ClientNew(self)
        c.show()
        c.exec_loop()
        clients= len(Model.Global.getClientList())
        if clients == 0:
            w.emit(PYSIGNAL('stateEvent'), ('notAvailable',))
        else:
            w.emit(PYSIGNAL('stateEvent'), ('available',))

    def clientOpen(self):
        """Presents a selection list of clients and
        opens the one clicked on.
        """
        cL= Model.Global.getClientList()
        c= Control.ListSelect.ClientSelect(self, cL)
        c.show()
        r= c.exec_loop()
        if r != 0:
            c= Control.Global.getListSelected()[0]
            try:
                Model.Global.setClientObject(c)
                #Read all tables from db
                Model.Books.readBooks(str(c.id))
                self.setCaption(Model.Global.getAppName() + ':'+ c.name)
                self.emit(PYSIGNAL('stateEvent'),('opened',))
                return  
            except (Model.Exceptions.DbError, Model.Exceptions.Unknown):
                QMessageBox.critical(self, Model.Global.getAppName(),
                 str(self.tr("Can not connect to the '%s_%s_%s' database.\n"%
                 (Model.Global.getDbPrefix(), c.id, c.year))) +
                 str(self.tr("Check if this database exists, and that\n"))+
                 str(self.tr("user, password and host are correctly set.\n")))
                self.emit(PYSIGNAL('stateEvent'),('closed',))

    def clientEdit(self):
        """Presents a selection list of clients and opens a client edit
        dialogue for the chosen client.
        """
        cL= Model.Global.getClientList()
        c= Control.ListSelect.ClientSelect(self, cL)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.Client.ClientEdit(self)
                c.show()
                c.exec_loop()

    def clientDelete(self):
        """Presents a selection list of clients and opens a client delete
        dialogue for the chosen client.
        """
        cL= Model.Global.getClientList()
        c= Control.ListSelect.ClientSelect(self, cL)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.Client.ClientDelete(self)
                c.show()
                c.exec_loop()
        clients= len(Model.Global.getClientList())
        if clients == 0:
            w.emit(PYSIGNAL('stateEvent'), ('notAvailable',))
        else:
            w.emit(PYSIGNAL('stateEvent'), ('available',))


    def clientClose(self):
        """Called when a client is closing. Emties Model.Books collection
        and close any open account, customer or vendor windows.
        """
        try:
            Model.Books.close()
            Model.Global.setClientObject(None)
        except: pass
        Model.Global.setBooksConnection(None)
        if self.accTreeObject:
            self.accTreeObject.close(1)
            self.accTreeObject= None
        if self.vendorTreeObject:
            self.vendorTreeObject.close(1)
            self.vendorTreeObject= None
        if self.customerTreeObject:
            self.customerTreeObject.close(1)
            self.customerTreeObject= None
        self.setCaption(Model.Global.getAppName())
        # Add other implemented windows here
        self.emit(PYSIGNAL('stateEvent'),('closed',))
        #Add other closing matter here, can't think of any right now

    def clientExit(self):
        """Called when user clicks on Exit item on Client menu. Supposed
        to close everything and shut down the application. Not implemented yet.
        The application updates the data base for each change, so there is
        nothing to do here now
        """
        pass

        # FIXME: needs a shutdown method perhaps:
        # close anything. All databases should be
        # up to date.
        # For XML-files etc: write them here
        # this function must also be called by SIG-SHUTDOWN + friends


                    
    # Account actions
    #================

    def accountEdit(self):
        """Opens a AccountEdit dialogue.
        """
        c= Control.Account.AccountEdit(self)
        QObject.connect(c, PYSIGNAL('account'), self.accountEmit)
        c.show()
        c.exec_loop()

    def accountNew(self):
        """Opens a AccountNew dialogue.
        """
        c= Control.Account.AccountNew(self)
        QObject.connect(c, PYSIGNAL('account'), self.accountEmit)
        c.show()
        c.exec_loop()

    def accountDelete(self):
        """Opens a AccountDelete dialogue.
        """
        c= Control.Account.AccountDelete(self)
        QObject.connect(c, PYSIGNAL('account'), self.accountEmit)
        c.show()
        c.exec_loop()

    def accountEmit(self, a, b):
        """Called by an 'account' signal from accountEdit, accountNew or
        accountDelete. Forward the signal parametres with
        a new  'account' signal generated here.
        """
        self.emit(PYSIGNAL('account'), (a, b))

    # Customer actions
    #=================

    def customerNew(self):
        """Opens a dialogue to create a new customer.
        """
        c= Control.Cuven.CustomerNew(self)
        QObject.connect(c, PYSIGNAL('cuven'), self.cuvenEmit)
        c.show()
        c.exec_loop()
        
    def customerEdit(self):
        """Opens a list select dialogue and then a CustomerEdit dialogue
        for the selected customer.
        """
        sL= Model.Books.getList('cuven')
        c= Control.ListSelect.CustomerSelect(self, sL)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.Cuven.CustomerEdit(self)
                QObject.connect(c, PYSIGNAL('cuven'), self.cuvenEmit)
                c.show()
                c.exec_loop()

    def customerDelete(self):
        """Opens a list select dialogue and then a CustomerDelete dialogue
        for the selected customer.
        """
        sL= Model.Books.getList('cuven')
        c= Control.ListSelect.CustomerSelect(self, sL)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.Cuven.CustomerDelete(self)
                QObject.connect(c, PYSIGNAL('cuven'), self.cuvenEmit)
                c.show()
                c.exec_loop()

    def customerView(self):
        """Opens a list select dialogue and then a CustomerView dialogue
        for the selected customers (multiselection).
        """
        sL= Model.Books.getList('cuven')
        c= Control.ListSelect.CustomerSelect(self, sL, 1)
        c.show()
        r= c.exec_loop()
        if r != 0:
            c= Control.Cuven.CustomerView(self)
            c.show()
            c.exec_loop()


    def vendorNew(self):
        """Opens a dialogue to create a new vendor.
        """
        c= Control.Cuven.VendorNew(self)
        QObject.connect(c, PYSIGNAL('cuven'), self.cuvenEmit)
        c.show()
        c.exec_loop()
        
    def vendorEdit(self):
        """Opens a list select dialogue and then a VendorEdit dialogue
        for the selected vendor.
        """
        sL= Model.Books.getList('cuven')
        c= Control.ListSelect.VendorSelect(self, sL)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.Cuven.VendorEdit(self)
                QObject.connect(c, PYSIGNAL('cuven'), self.cuvenEmit)
                c.show()
                c.exec_loop()

    def vendorDelete(self):
        """Opens a list select dialogue and then a VendorDelete dialogue
        for the selected vendor.
        """
        sL= Model.Books.getList('cuven')
        c= Control.ListSelect.VendorSelect(self, sL)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.Cuven.VendorDelete(self)
                QObject.connect(c, PYSIGNAL('cuven'), self.cuvenEmit)
                c.show()
                c.exec_loop()

    def vendorView(self):
        """Opens a list select dialogue and then a VendorView dialogue
        for the selected vedorsrs (multiselection).
        """
        sL= Model.Books.getList('cuven')
        c= Control.ListSelect.VendorSelect(self, sL, 1)
        c.show()
        r= c.exec_loop()
        if r != 0:
            c= Control.Cuven.VendorView(self)
            c.show()
            c.exec_loop()
            Control.Cuven.emptyGlobals()


    def cuvenEmit(self, a, b):
        """Called by an 'cuven' signal from cuvenEdit, cuvenNew or
        cuvenDelete. Forward the signal parametres with
        a new  'cuven' signal generated here.
        """
        print "Qd emit cuven"
        self.emit(PYSIGNAL('cuven'), (a, b))

    # Source actions
    #===============

    def sourceNew(self):
        """Opens a dialogue to create a new source.
        """
        c= Control.Source.SourceNew(self)
        c.show()
        c.exec_loop()
        
    def sourceEdit(self):
        """Opens a list select dialogue and then a SourceEdit dialogue
        for the selected source.
        """
        sL= Model.Books.getList('source')
        c= Control.ListSelect.SourceSelect(self, sL[1:])
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.Source.SourceEdit(self)
                c.show()
                c.exec_loop()


    def sourceDelete(self):
        """Opens a list select dialogue and then a SourceDelete dialogue
        for the selected source.
        """
        sL= Model.Books.getList('source')
        c= Control.ListSelect.SourceSelect(self, sL[2:])
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.Source.SourceDelete(self)
                c.show()
                c.exec_loop()
                for s in sL: print s


    def sourceView(self):
        """Opens a list select dialogue and then a SourceView dialogue
        for the selected sources (multiselection).
        """
        #TODO: implement 'source' signal from SourceView dialogue?
        sL= Model.Books.getList('source')
        c= Control.ListSelect.SourceSelect(self, sL, 1)
        c.show()
        r= c.exec_loop()
        if r != 0:
            c= Control.Source.SourceView(self)
            c.show()
            c.exec_loop()

    def sourceInvque(self):
        """Make auto sources from the invoice que list and shows a
        list of generated sources.
        """
        queL= Model.Books.getList('invque')
        if len(queL) == 0:
            QMessageBox.information(self, Model.Global.getAppName(),
                      self.tr('The invoice queue is empty'))
        else:
            c= Control.Queue.InvoiceQueue(self)
            c.show()
            c.exec_loop()

    def sourceVat(self):
        """Make auto source for transfer of the period's VAT. 
        """
        c= Control.SourceVat.SourceVat(self)
        c.show()
        c.exec_loop()


    def sourceFind(self):
        """Opens a SourceFind dialogue to search for sources satisfying some
        criteria. Then shows a selection list of the found sources. If the user
        clicks on one of the sources a 'source' signal with the chosen source
        is emitted. This can be used to inject a copy of a source into a
        sourceNew dialogue.
        """
        c= Control.SourceFind.SourceFind(self)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.ListSelect.SourceFindSelect(self, viewList)
                QObject.connect(c, PYSIGNAL('source'), self.sourceSourceEmit)
                c.show()
                c.exec_loop()
    
    def sourceSourceEmit(self, a):
        """Reemits a 'source' signal as a sourceSelected' signal.
        """
        self.emit(PYSIGNAL('sourceSelected'), (a,))


    # Rule actions
    #=============

    def ruleNew(self):
        """Opens a RuleNew dialogue.
        """
        c= Control.Rule.RuleNew(self)
        c.show()
        c.exec_loop()
        

    def ruleEdit(self):
        """Opens a select list dialogue. And then a RuleEdit dialogue
        for the rule the user clicked.
        """
        rL= Model.Books.getList('rule')
        c= Control.ListSelect.RuleSelect(self, rL)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                c= Control.Rule.RuleEdit(self)
                c.show()
                c.exec_loop()


    def ruleDelete(self):
        """Delete a rule. Not implemented.
        """
        pass

    def ruleView(self):
        """View rules, possibly also emit a ruleselected signal
        for copy into RuleNew dialogue. Not implemented.
        """
        pass

    # Report actions
    #===============
    
    def reportSourceList(self):
        """Opens a SourceSelect dialogue where user can select a range
        of sources. Then opens a report generator that displays a
        list of sources in the central widget. The user can
        choose to print or save the report.
        """
        c= Control.SourceSelect.SourceSelect(self)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                ed= Control.ReportGen.SourceList
                self.reportw = Control.MDIWindow.MDIWindow(
                    self.ws, ed, viewList)
                self.editor= self.reportw.getEditor()
                self.reportw.setCaption(self.tr("Source list"))
                self.reportw.setIcon(QPixmap(appIcon()))
                self.editor.setText(self.editor.makeHtml())

                
    def reportLedgerBalance(self):
        """Opens TimeFrameSelect dialogue where user can select a range
        of dates. Then opens a report generator that displays the
        ledger balance for the range  in the central widget. The user can
        choose to print or save the report.
        """
        c= Control.TimeFrameSelect.LedgerBalanceSelect(self)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                ed= Control.ReportGen.LedgerBalance
                self.reportw = Control.MDIWindow.MDIWindow(
                    self.ws, ed, viewList)
                self.editor= self.reportw.getEditor()
                self.reportw.setCaption(self.tr("Ledger balance"))
                self.reportw.setIcon(QPixmap(appIcon()))
                self.editor.setText(self.editor.makeHtml())
                
    def reportSubsLedger(self):
        """Opens CuvenSelect dialogue where user can select customers and
        vendors. Then opens a report generator that displays the
        subsidiary ledger for the chosen in the central widget. The user can
        choose to print or save the report.
        """
        c= Control.CuvenSelect.CuvenSelect(self)
        c.show()
        r= c.exec_loop()
        if r != 0:
            viewList= Control.Global.getListSelected()
            if len(viewList) > 0:
                ed= Control.ReportGen.SubsidiaryLedger
                self.reportw = Control.MDIWindow.MDIWindow(
                    self.ws, ed, viewList)
                self.editor= self.reportw.getEditor()
                self.reportw.setCaption(self.tr("Subsidiary ledger"))
                self.reportw.setIcon(QPixmap(appIcon()))
                self.editor.setText(self.editor.makeHtml())

    #TODO: reports, reports, reports....

    # Config menu actions
    #====================

    def configAboutToShow(self):
        """Enables and disables some menuitems according to if any client is
        open.  Called with click on client menu.
        """
        if stateEvents['clientIsOpen']!=0: #client is open
            self.configVatAccAction.setEnabled(1)
        else:
            self.configVatAccAction.setEnabled(0)
    
    def configEdit(self):
        """Opens Configuration dialogue where user can edit preferences
        Get parameter dictionary from Model.Global
        Make a copy in case user cancels edit.
        """
        d= Model.Global.getUserDict().copy()
        c= Control.Configtable.Configtable(d, 1)
        c.show()
        r= c.exec_loop()
        if r != 0: #save
            Model.Global.setUserDict(c.res)
 
            
    def configView(self):
        """Opens dialogue to display all options
        Get parameter dictionary from Model.Global
        All fields are disabled
        """
        d= Model.Global.getAllDicts()
        c= Control.Configtable.Configtable(d, 0)
        c.show()
        c.exec_loop()
        
            
    def configVatAcc(self):
        """Opens dialogue to show and edit a list of VAT
        codes and related accounts
        """
        c= Control.Vat.Vat()
        c.show()
        c.exec_loop()
        
            

    # Window menu actions
    #====================
        
    def windowAboutToShow(self):
        """Called when clicking the window menu. Manage the available
        windows.
        """
        if self.accTreeObject:
            if self.accTreeObject.isVisible() == 0:
                # window is gone, do a reality sync
                self.accTreeObject= None
                self.windowAccountTreeAction.toggle()
        if self.customerTreeObject:
            if self.customerTreeObject.isVisible() == 0:
                # window is gone, do a reality sync
                self.customerTreeObject= None
                self.windowCustomerTreeAction.toggle()
        if self.vendorTreeObject:
            if self.vendorTreeObject.isVisible() == 0:
                # window is gone, do a reality sync
                self.vendorTreeObject= None
                self.windowVendorTreeAction.toggle()

    def windowAccountTree(self):
        """Opens an account tree window if not open, closes if open.
        Connects AccountSelected signal from an opened window.
        """
        if self.accTreeObject:
            self.accTreeObject.close(1)
            self.accTreeObject= None
            #Disconnect AccountSelected signal here?
        else:
            self.accTreeObject= Control.AccountTree.AccountTree(self, None, 0)
            c= self.accTreeObject
            c.show()
            QObject.connect(c, PYSIGNAL('AccountSelected'),
                            self.windowAccountEmit)

    def windowAccountEmit(self, a):
        """Gets the AccountSelected signal from the tree view window and
        reemits as an accountSelected signal.
        """
        self.emit(PYSIGNAL('accountSelected'), (a,))

        
    def windowCustomerTree(self):
        """Opens a customer tree window if not open, closes if open.
        Connects CustomerSelected signal from an opened window.
        """
        if self.customerTreeObject:
            self.customerTreeObject.close(1)
            self.customerTreeObject= None
            #Disconnect CustomerSelected signal here?
        else:
            self.customerTreeObject= Control.CuvenTree.CustomerTree(
                self, None, 0)
            c= self.customerTreeObject
            c.show()
            QObject.connect(c, PYSIGNAL('CustomerSelected'),
                            self.windowCustomerEmit)

    def windowCustomerEmit(self, a):
        """Gets the CustomerSelected signal from the tree view window and
        reemits as a customerSelected signal.
        """
        self.emit(PYSIGNAL('customerSelected'), (a,))
        
    def windowVendorTree(self):
        """Opens a vendor tree window if not open, closes if open.
        Connects VendorSelected signal from a opened window.
        """
        if self.vendorTreeObject:
            self.vendorTreeObject.close(1)
            self.vendorTreeObject= None
            #Disconnect VendorSelected signal here?
        else:
            self.vendorTreeObject= Control.CuvenTree.VendorTree(self, None, 0)
            c= self.vendorTreeObject
            c.show()
            QObject.connect(c, PYSIGNAL('VendorSelected'),
                            self.windowVendorEmit)

    def windowVendorEmit(self, a):
        """Gets the VendorSelected signal from the tree view window and
        reemits as a vendorSelected signal.
        """
        self.emit(PYSIGNAL('vendorSelected'), (a,))
        

    # Help menu actions
    #==================

    def helpIndex(self):
        """Help index. Not implemented.
        """
        pass

    def helpContents(self):
        """Help contents, not implemented.
        """

    def helpAbout(self):
        """Shows an about window.
        """
        QMessageBox.about(self, str(self.tr('About %s'))%
                          Model.Global.getAppName(), 
        str(self.tr('%s is an accounting program for Linux'))%
                          Model.Global.getAppName()+ '\n\n' +\
        'Copyright 2003-2005 Odd Arild Olsen\n' +\
        str(self.tr('License: GNU GPL, see the LICENSE file')) + '\n\n'+ \
        str(self.tr('Project home:')) + ' http://gryn.berlios.de') 


#
###### The main function
#

if __name__ == "__main__":
    """Here begins the execution of this application.
    """

    import Database.DbAccess
    import Model.Client
    import Model.Exceptions
    import string
    
    global wrksp

    
    #Model.Global.pathFixup(MyExecPath)
    #Model.Global.readConfigFiles()
    gc= Control.Global.Global()
    a = QApplication(sys.argv)
    # Pick the tanslator 
    translator= QTranslator(None)
    loc= Model.Global.getLocale()
    if not loc: # use system locale
        loc= str(QTextCodec.locale())
    lpath= Model.Global.getLocalePath() + '/'+ loc + '/LC_MESSAGES/'+'gryn.qm'
    translator.load(lpath)
    a.installTranslator(translator)

    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
                              #FIXME connect to shutdown function instead?

    w = Qd()
    QObject.connect(w.clientExitAction, SIGNAL("activated()"),
                   a, SLOT("quit()"))

    a.setMainWidget(w)
    Model.Global.setRole('root') #FIXME: get user role from some conf file
                                 # or dialog
    appName= Model.Global.getAppName()
    w.setIcon(QPixmap(appIcon()))
    dbPrefix= Model.Global.getDbPrefix()
    
    # Trial-open database, create if not exists
    try:
        db= None
        cause= ''
        db=Database.DbAccess.DbAccess(dbPrefix)
        db.close()
    except Model.Exceptions.DbError, e:
        pass # does not exist or no data base connection
    except Model.Exceptions.Unknown, s:
        cause= str(a.tr("Unknown error: \n")) +s
        QMessageBox.critical(w, appName,
          str(a.tr("A problem with the database access occurred:\n%s"%cause))+\
                    str(a.tr("\nThe program will terminate.")))
        sys.exit(1)
    if not db: # We must create the data base for gryn
        r= QMessageBox.information(w, appName,
            str(a.tr("The '%s' data base does"%dbPrefix))+ '\n'+ \
                str(a.tr("not exsist. Shall I create it?")),
                                   a.tr("Yes"), a.tr("No"))
        if r==0:
            try:
                db= Database.DbAccess.DbAccess(None)
                db.createDataBase(dbPrefix)
                db.close()
            except Model.Exceptions.DbError, e:
                cause= e.args
            except Model.Exceptions.Unknown, s:
                cause= str(a.tr("Unknown error: \n")) +s.args
        else: sys.exit(1) # do not want to create
    if not db:
        QMessageBox.critical(w, appName,
          str(a.tr("A problem with the database access occurred:\n%s"%cause))+\
                    str(a.tr("\nThe program will terminate.")))
        sys.exit(1)

    # Now we know the database is present
    #open Client data base, create new or terminate if not there
    #this must be done before the client-menue becomes active
    try:
        clientList= Model.Client.ClientList(dbPrefix)
    except Model.Exceptions.DbError, e:
        r= QMessageBox.information(w, appName,
            str(a.tr("The 'client' data table does\n"))+
                str(a.tr("not exsist. Shall I create one?")),
                                   a.tr("Yes"), a.tr("No"))
        if r==0:
            usr, pwd, host= Model.Global.getUsrPwdHost()
            Model.Client.createTable(dbPrefix)
        else: sys.exit(1)
        
        # the table shall now be present, empty though
        try:
            clientList= Model.Client.ClientList(dbPrefix)
        except Model.Exceptions.DbError, e:
            r= QMessageBox.critical(w, appName,
                 str(a.tr("I can not create a new 'client' table\n"))+
                 str(a.tr("so I will quit now")))
            sys.exit(1)
    Model.Global.setClientList(clientList)
    Model.Global.setClientConnection(clientList.getConnection())
    if len(clientList)==0:
        w.emit(PYSIGNAL('stateEvent'), ('notAvailable',))
    else:
        w.emit(PYSIGNAL('stateEvent'), ('available',))
    w.emit(PYSIGNAL('stateEvent'),('closed',))# to enable/disable menubar items
    w.show()
    a.exec_loop() # Here we spend most of the time clicking and typing
    Model.Books.close()
    #Fin

