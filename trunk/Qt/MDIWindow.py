""" $Id$<br>
Implements a Multi Document Interface for displaying reports
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


from qt import *
import os
import os.path
import Model.Global
import Control.Global

def _printerIcon():
    return Control.Global.expandImg('printer1.png')


class MDIWindow( QMainWindow):
    """MDI Window class to show reports.
    """

    def __init__(self, parent, ed, objL):
        """Set up the MDI window.<br>
        'ed': The editor to use for this window
        """
        QMainWindow.__init__(self,parent, None, 0 )
        # Minimize any open MDI window
        try:
            for i in parent.windowList():
                i.showMinimized()
        except TypeError:
            pass
        # Set up the tool bar of this window
        self.toolBar= QToolBar('', self, Qt.DockTop)

        # Tool button to print report
        self.printAction= QAction(self, 'printAction')
        self.printAction.setIconSet(QIconSet(QPixmap(_printerIcon())))
        self.printAction.setToolTip(self.tr('Print this report'))
        self.printAction.addTo(self.toolBar)

        self.connect(self.printAction, SIGNAL("activated()"), self.printAct)

        # Save the editor and set self to be the central widget
        self.medit = ed(self, objL)
        self.setFocusProxy( self.medit )
        self.setCentralWidget( self.medit )
        self.showMaximized()

    def printAct(self):
        """Action called to print the report of the window
        """
        # Use the Qt printer dialog to get printer information
        pr= QPrinter()
        pr.setOrientation(pr.Portrait)
        pr.setPageSize(pr.A4)
        pr.setOutputFileName(Model.Global.getTmpPath()+'/out.ps')
        pr.setOutputToFile(0)
        pr.setup()
        if pr.pageOrder() != pr.FirstPageFirst:
            seq= '-r'
        else:
            seq= ''
        #copies= pr.numCopies()
        if pr.outputToFile != 0:
            fi= pr.outputFileName()
        else:
            fi= '!' + pr.printerName()
        # Generate the TeX output
        self.medit.makeTeX('gryn.tex') # LaTeX allways use the pwd
        # TeX the file into dvi
        ret= os.system('latex  -interaction=batchmode gryn.tex >/dev/null')
        print 'ret latex: ', ret
        # Then print the dvi file
        ret= os.system('dvips -q -C %s %s -o %s gryn.dvi >/dev/null'%(
            seq, pr.numCopies(), fi))

        

    def getEditor(self):
        """Return the editor of this window.
        """
        return self.medit

