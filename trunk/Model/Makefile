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


LOCALEPATH=../var/gryn/locale/no/LC_MESSAGES

all:

clean:
	rm -f *~ *pyc \#* locale/*~ locale/\#*


install:
	cp locale/gryn_no.mo $(LOCALEPATH)/gryn.mo


po:   # Merge old translations or make a new file if not exists
	xpot -o locale/gryn.pot -n -k N_ Global.py Source.py Invque.py Vat.py\
	../Report.no/*.py \
	&& \
	msgmerge -U locale/gryn_no.po locale/gryn.pot || \
	cp locale/gryn.pot locale/gryn_no.po


mo:	locale/gryn_no.mo

locale/gryn_no.mo: locale/gryn_no.po
	msgfmt  locale/gryn_no.po -o locale/gryn_no.mo && \
	cp locale/gryn_no.mo $(LOCALEPATH)/gryn.mo
