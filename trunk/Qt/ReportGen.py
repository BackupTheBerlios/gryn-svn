""" $Id$<br>
TODO: Eliminate this class, not needed at all.
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
import Report.SourceList
import Report.LedgerBalance
import Report.SubsidiaryLedger

class _Base(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setTextFormat(Qt.RichText)
        self.setReadOnly(1)

    def makeHtml(self):
        return self.reporter.makeHtml()

    def makeTeX(self, file):
        self.reporter.makeTeX(file)

class SourceList(_Base):
    def __init__(self, parent, sourceL):
        _Base.__init__(self, parent)
        self.reporter= Report.SourceList.SourceList(sourceL)

        
class LedgerBalance(_Base):
    def __init__(self, parent, L):
        _Base.__init__(self, parent)
        self.reporter= Report.LedgerBalance.LedgerBalance(L)


class SubsidiaryLedger(_Base):
    def __init__(self, parent, L):
        _Base.__init__(self, parent)
        self.reporter= Report.SubsidiaryLedger.SubsidiaryLedger(L)
