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
	rm -f *~  \#* *pyc


install: mo


po:   # Merge old translations or make a new file if not exists
	xpot -o locale/report.pot -n -k N_ *.py\
	&& \
	msgmerge -U locale/report_no.po locale/report.pot || \
	cp locale/report.pot locale/report_no.po


mo:	locale/report_no.mo

locale/report_no.mo: locale/report_no.po
	msgfmt  locale/report_no.po -o locale/report_no.mo && \
	cp locale/report_no.mo $(LOCALEPATH)/report.mo
