#! /usr/bin/env python
# $Id$
# Collects all files in the directory tree below and including .
# Neglects links, dot-names, backup names, compiled python names and
# names with substring 'aside'
# Also neglects var, tmp, etc and Import directories
# Usually cat the output to MANIFEST

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


import os, string

global printFiles

alist = os.walk('.', 1)    
for a in alist:
    if string.find(a[0], 'aside') >= 0: continue
    if string.find(a[0], '/.') >= 0: continue
    if string.find(a[0], 'var/') >= 0: continue
    if string.find(a[0], 'tmp/') >= 0: continue
    if string.find(a[0], 'etc/') >= 0: continue
    if string.find(a[0], '/Import') >= 0: continue
    try:
        if a[0][3]== '.': continue
    except:
        pass
    
    for f in a[2]:
        if f[0]=='.': continue
        if string.find(f, '.aside')>=0: continue
        if string.find(f, '.pyc')>=0: continue
        if string.find(f, '.tar.gz')>=0: continue
        if string.find(f, '.aux')>=0: continue
        if string.find(f, '.dvi')>=0: continue
        if string.find(f, '.log')>=0: continue
        if string.find(f, '.tex')>=0: continue
        if string.find(f, 'releasefiles')>=0: continue
        if f[-1]=='~': continue
                       
        s= a[0]+'/'+f
        if string.find(s, 'var/')>=0: continue
        if string.find(s, 'tmp/')>=0: continue
        if string.find(s, 'etc/')>=0: continue
        if os.path.islink(s) != 0: continue
        print s[2:]
