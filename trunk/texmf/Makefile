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


TEXMFPATH= ~/texmf/tex/latex
GPWD= $(PWD)

all: 

clean: 
	rm -f *~ \#* 

install:
	mkdir -p $(TEXMFPATH)
	(cd $(TEXMFPATH);\
	rm -f grynLedgerBalance.cls  grynSubsidiaryLedger.cls; \
	rm -f grynBase.sty  grynSourceList.cls; \
	ln -s $(GPWD)/grynLedgerBalance.cls grynLedgerBalance.cls; \
	ln -s $(GPWD)/grynSubsidiaryLedger.cls grynSubsidiaryLedger.cls; \
	ln -s $(GPWD)/grynBase.sty grynBase.sty; \
	ln -s $(GPWD)/grynSourceList.cls grynSourceList.cls \
	)
