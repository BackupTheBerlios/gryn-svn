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




VERS=20050309
BRANCH=trunk

all: # do nothing not explicitely ordered


#Get all the files given in MANIFEST into a tar-archive 
trunktar: gryn-$(VERS).tar.gz

gryn-$(VERS).tar.gz:
	./collect.py > MANIFEST
	cat MANIFEST | sed s:^:gryn-$(VERS)/: >releasefiles 
	(cd ..; ln -s $(BRANCH) gryn-$(VERS))
	(cd ..; tar czvf gryn-$(VERS)/gryn-$(VERS).tar.gz -T \
		$(BRANCH)/releasefiles)
	(cd ..; rm gryn-$(VERS))
	rm releasefiles

#Remove all scratch and backup files
clean: 
	rm -f *~ \#* *.pyc releasefiles 
	(cd Database && make clean)
	#(cd doc && make clean)
	#(cd etc && make clean)
	#(cd img && make clean)
	#(cd Import && make clean)
	#(cd misc && make clean)	
	(cd Model && make clean)
	(cd Qt && make clean)
	(cd Report.no && make clean)
	#(cd texmf && make clean)
	rm -f tmp/*

# manually make a signature: 
#gpg --output gryn-$(VERS).tar.gz.sig --detach-sig gryn-$(VERS).tar.gz

install:
	ln -s Qt Control
	ln -s Report.no Report
	mkdir -p etc
	mkdir -p tmp
	mkdir -p Import
	mkdir -p var/gryn/locale/no/LC_MESSAGES
	(cd .. ; ln -s gryn-$(VERS) gryn)
	(cd Database && make install)
	#(cd doc && make install)
	#(cd etc && make install)
	#(cd img && make install)
	#(cd Import && make install)
	(cd misc && make install)	
	(cd Model && make install)
	(cd Qt && make install)
	(cd Report.no && make install)
	(cd texmf && make install)


