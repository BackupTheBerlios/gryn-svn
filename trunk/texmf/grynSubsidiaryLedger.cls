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
\ProvidesClass{grynSubsidiaryLedger}
\def\Basesize{12pt}
\input{grynBase.sty}

%%%%%%%%%%

\newlength{\Account}
\newlength{\Amount}
\newlength{\Date}
\setlength{\Account}{15mm}
\setlength{\Amount}{30mm}
\setlength{\Date}{25mm}
\def\parsep{4mm plus 5mm minus 1mm}
\newenvironment{Cuven}[3]
               {\begin{minipage}{\textwidth}
                   {\textbf{\makebox[\Account][l]{#1}#2\hfill#3}}\\}
               {\end{minipage}\vspace{\parsep}}%

\newcommand{\Source}[5]{\makebox[\Account][l]{#1}\makebox[\Date][l]{#2}#3\hfill
  \makebox[\Amount][r]{#4}%
    \makebox[\Amount][r]{#5}\\}%


