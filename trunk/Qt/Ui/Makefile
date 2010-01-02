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



VPATH= ..

ALL=uClientOpen.py uClientEditNew.py uAccountImport.py \
uTreeList.py uSource.py uListSelect.py uAccount.py \
uSourceFind.py uCuven.py uSourceSelect.py uSourceVat.py uTimeFrameSelect.py \
uRule.py uRuleAssign.py uQueue.py uCuvenSelect.py uVat.py

all: $(ALL)

uClientOpen.py:uClientOpen.ui
uClientEditNew.py:uClientEditNew.ui
uAccountImport.py:uAccountImport.ui
uTreeList.py:uTreeList.ui
uSource.py:uSource.ui
uListSelect.py:uListSelect.ui
uAccount.py:uAccount.ui
uSourceFind.py:uSourceFind.ui
uSourceSelect.py:uSourceSelect.ui
uSourceVat.py:uSourceVat.ui
uCuven.py:uCuven.ui
uTimeFrameSelect.py:uTimeFrameSelect.ui
uRule.py:uRule.ui
uRuleAssign.py:uRuleAssign.ui 
uQueue.py:uQueue.ui
uCuvenSelect.py:uCuvenSelect.ui
uVat.py:uVat.ui

%.py : %.ui
	pyuic4 -x $< >../$@

clean: 
	rm -f *~ 
	(cd .. ; rm $(ALL))  
