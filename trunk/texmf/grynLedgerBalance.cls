% $Id$
% LaTeX class for gryn reports

%    This file is a part of the gryn/Qdough accounting program
%    Copyright (C) 2003-2005  Odd  Arild Olsen

%    This program is free software; you can redistribute it and/or modify
%    it under the terms of the GNU General Public License as published by
%    the Free Software Foundation; either version 2 of the License, or
%    (at your option) any later version. 

%    This program is distributed in the hope that it will be useful,
%    but WITHOUT ANY WARRANTY; without even the implied warranty of
%    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%    GNU General Public License for more details.

%    You should have received a copy of the GNU General Public License
%    along with this program; if not, write to the Free Software
%    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
%    The top level file LICENSE holds the verbatim copy of this license.


\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{grynLedgerBalance}
\def\Basesize{10pt}
\input{grynBase.sty}

%%%%%%%%%%%%

\newlength{\wAccount}
\newlength{\wAmount}
\newlength{\wAccName}
\setlength{\wAccount}{10mm}
\setlength{\wAmount}{20mm} 
\setlength{\wAccName}{\textwidth}
\addtolength{\wAccName}{-\wAccount}
\addtolength{\wAccName}{-\wAmount}
\addtolength{\wAccName}{-\wAmount}
\addtolength{\wAccName}{-\wAmount}
\addtolength{\wAccName}{-1pt}

\newcommand{\TableHeader}[4]{%{opening}{permoves}{yearmoves}{closing}
  \E{\mbox{}}{\mbox{}}{#1}{#2}{#3}{#4}
  \renewcommand{\baselinestretch}{1.5}\normalsize}

\newcommand{\Entry}[6]{%{accNum}{accName}{opening}{moves}{closing}
  \E{#1}{#2}{$#3$}{$#4$}{$#5$}{$#6$}}

\newcommand{\E}[6]{\noindent%six columns
  \makebox[\wAccount][l]{#1}\parbox[t]{\wAccName}{#2}\hfill%
  \makebox[\wAmount][r]{#3}\makebox[\wAmount][r]{#4}%
  \makebox[\wAmount][r]{#5}\makebox[\wAmount][r]{#6}\\}

\newcommand{\TableFooter}[5]{%'sum' ib per year sum
  \vspace*{-2mm}\hrule\vspace{1mm}\E{}{#1}{$#2$}{$#3$}{$#4$}{$#5$}}
