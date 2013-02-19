% -*- coding: utf-8 -*-
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{wl}[2011/11/28 wolnelektury.pl book style]

% PDF customizations
%
% nofootnotes - disable generation of footnotes
% nothemes - disable generation of themes
% defaultleading - default leading
% onehalfleading - leading of 1.5 (interlinia)
% doubleleading - double leading (interlinia)
% a4paper,... - paper size as required by LaTeX
% nowlfont - don't use customized WL font

\RequirePackage{setspace}
\RequirePackage{type1cm}
\RequirePackage{wasysym}
\DeclareOption{13pt}{%
\AtEndOfClass{%
% font size definitions, similar to ones in /usr/share/texmf-texlive/tex/latex/base/
\renewcommand\normalsize{%
   \@setfontsize\normalsize{13pt}{14.5pt}%
   \abovedisplayskip 12\p@ \@plus3\p@ \@minus7\p@
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip 6.5\p@ \@plus3.5\p@ \@minus3\p@
   \belowdisplayskip \abovedisplayskip
   \let\@listi\@listI}\normalsize%
\renewcommand\footnotesize{%
   \@setfontsize\footnotesize\@xpt\@xiipt
   \abovedisplayskip 10\p@ \@plus2\p@ \@minus5\p@
   \abovedisplayshortskip \z@ \@plus3\p@
   \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 6\p@ \@plus2\p@ \@minus2\p@
               \parsep 3\p@ \@plus2\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}%
}%
}

%% \DeclareOption{14pt}{\renewcommand{\normalsize}{\AtEndOfClass{\fontsize{14}{17}\selectfont}}}

\DeclareOption{defaultleading}{}
\DeclareOption{doubleleading}{\AtBeginDocument{\doublespacing}}%\setlength{\leading}{1em plus 0.5ex minus 0.2ex}}
\DeclareOption{onehalfleading}{\AtBeginDocument{\onehalfspacing}}%\setlength{\leading}{1em plus 0.5ex minus 0.2ex}}

%% This does not really work, since dvipdfm(x) will use it's configuration in /etc/texmf/dvipdfm(x) and force a global paper size setting.
\DeclareOption{a5paper}{%
      \setlength{\paperheight}{210mm}%
      \setlength{\paperwidth}{148mm}}


\newif\ifshowfootnotes \showfootnotestrue
\DeclareOption{nofootnotes}{\showfootnotesfalse}

\newif\ifshowthemes \showthemestrue
\DeclareOption{nothemes}{\showthemesfalse}

\newif\ifenablewlfont \enablewlfonttrue
\DeclareOption{nowlfont}{\enablewlfontfalse}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax
\LoadClass[a4paper,oneside]{book}


\usepackage{trace}

\usepackage[xetex]{graphicx}
\usepackage{fontspec}
\usepackage{xunicode}
\usepackage{xltxtra}

\usepackage[overload]{textcase}
\usepackage{scalefnt}
% TODO: link color is a style thing
\usepackage[hyphens]{url}
\usepackage[colorlinks=true,linkcolor=black,setpagesize=false,urlcolor=blue,xetex]{hyperref}

\ifenablewlfont
\setmainfont [
%ExternalLocation,
UprightFont = Dosis-Regular,
ItalicFont = Dosis-SemiBold,
BoldFont = Dosis-Bold,
BoldItalicFont = Dosis-Bold,
SmallCapsFont = Dosis-Regular,
SmallCapsFeatures = {Letters={SmallCaps,UppercaseSmallCaps}},
Numbers=OldStyle,
Scale=1.04,
LetterSpace=-1.0
] {Dosis}

\newfontfamily\alien[
SmallCapsFeatures = {Letters={SmallCaps,UppercaseSmallCaps}},
Numbers=OldStyle,
Scale=0.85,
LetterSpace=-1.0
] {DejaVu Serif}


\defaultfontfeatures{
SizeFeatures={
  {Size={-10.5}, FakeStretch=1.02, LetterSpace=2.0 },
  {Size={10.5-12}, FakeStretch=2.00, LetterSpace=0.0 },
  {Size={12-}, FakeStretch=0.98, LetterSpace=-2.0 }
}
}

\renewcommand{\textsc}[1]{%
{\addfontfeature{
SizeFeatures={
  {Size={-10.5}, Scale=1.2, FakeStretch=1.02, LetterSpace=8.0 },
  {Size={10.5-12}, Scale=1.2, FakeStretch=1.02, LetterSpace=8.0 },
  {Size={12-}, FakeStretch=1.0, LetterSpace=8.0 }
},
Letters={SmallCaps,UppercaseSmallCaps}
}
#1}
}
\fi% enablewlfont

%{\Itshape JunicodeWL-Italic.ttf }
%{\bfseries Junicode-Bold.ttf }
%{\bfseries\itshape Junicode-BoldItalic.ttf }

\pagestyle{plain}
\usepackage{fancyhdr}

\makeatletter

% bottom figure below footnotes
\usepackage{fnpos}
\makeFNabove

\usepackage{color}
\definecolor{theme}{gray}{.3}

\setlength{\marginparsep}{2em}
\setlength{\marginparwidth}{8.5em}
\setlength{\oddsidemargin}{0pt}
\setlength{\voffset}{0pt}
\setlength{\topmargin}{0pt}
\setlength{\headheight}{0pt}
\setlength{\headsep}{0pt}
\setlength{\textheight}{24cm}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\lfoot{{\footnotesize \@author{} \emph{\@title}}}
\cfoot{}
\rfoot{{\footnotesize \thepage}}

\clubpenalty=100000
\widowpenalty=100000


% see http://osdir.com/ml/tex.xetex/2005-10/msg00003.html
\newsavebox{\ximagebox}\newlength{\ximageheight}
\newsavebox{\xglyphbox}\newlength{\xglyphheight}
\newcommand{\xbox}[1]
{\savebox{\ximagebox}{#1}\settoheight{\ximageheight}{\usebox {\ximagebox}}%
\savebox{\xglyphbox}{\char32}\settoheight{\xglyphheight}{\usebox {\xglyphbox}}%
\raisebox{\ximageheight}[0pt][0pt]{%\raisebox{-\xglyphheight}[0pt] [0pt]{%
\makebox[0pt][l]{\usebox{\xglyphbox}}}%}%
\usebox{\ximagebox}%
\raisebox{0pt}[0pt][0pt]{\makebox[0pt][r]{\usebox{\xglyphbox}}}}



\newcommand{\typosubsubsection}[1]{%
{#1}
}

\newcommand{\typosubsection}[1]{%
{\addfontfeature{
SizeFeatures={
  {Size={-10}, Scale=1.2, FakeStretch=1.00, LetterSpace=8.0 },
  {Size={10.5-12}, Scale=1.2, FakeStretch=1.00, LetterSpace=8.0 },
  {Size={12-}, FakeStretch=1.0, LetterSpace=8.0 }
},
Letters={Uppercase}
}
\MakeUppercase{#1}}
}

\newcommand{\typosection}[1]{%
{\addfontfeature{FakeStretch=0.96, LetterSpace=-4.0}\emph{\scalefont{2}#1}}
%{\addfontfeature{Scale=2.0, FakeStretch=0.98, LetterSpace=-2.0}\emph{#1}}
}


\newcommand{\tytul}[1]{%
#1%
\vspace{1em}%
}

\newcommand{\nazwapodutworu}[1]{%
\section*{\typosection{#1}}%
}

\newcommand{\autorutworu}[1]{%
\subsection*{\typosubsection{#1}}%
}

\newcommand{\dzielonadrzedne}[1]{%
\subsection*{\typosubsubsection{#1}}%
}

\newcommand{\nazwautworu}[1]{%
\section*{\typosection{#1}}%
}

\newcommand{\podtytul}[1]{%
\subsection*{\typosubsubsection{#1}}%
}

\newcommand{\translator}[1]{%
% TODO: l10n is a style thing
\subsection*{\typosubsubsection{tłum. #1}}%
}


\newcommand{\powiesc}[1]{#1}
\newcommand{\opowiadanie}[1]{#1}
\newcommand{\lirykal}[1]{#1}
\newcommand{\lirykalp}[1]{#1}
\newcommand{\dramatwierszowanyl}[1]{#1}
\newcommand{\dramatwierszowanylp}[1]{#1}
\newcommand{\dramatwspolczesny}[1]{#1}

\newcommand{\nota}[1]{%
\par{#1}%
}

\newcommand{\dedykacja}[1]{%
\begin{em}%
\begin{flushright}%
#1%
\end{flushright}%
\end{em}%
}

\newcommand{\dlugicytat}[1]{%
\begin{quotation}%
#1%
\end{quotation}%
}

\newcommand{\poezjacyt}[1]{%
\begin{verse}%
#1%
\end{verse}%
}
\newcommand{\motto}[1]{%
\begin{em}%
#1%
\end{em}%
}
\newcommand{\listaosob}[2]{%
\par{#1}%
\begin{itemize}%
#2%
\end{itemize}%
}

\newcommand{\nagloweklisty}[1]{%
\typosubsubsection{#1}%
}

\newcommand{\listaosoba}[1]{%
\item{#1}%
}

\newcommand{\kwestia}[1]{%
\par{#1}%
}

\newcommand{\naglowekakt}[1]{%
\pagebreak
\subsection*{\typosubsection{#1}}%
}
\newcommand{\naglowekczesc}[1]{%
\pagebreak
\subsection*{\typosubsection{#1}}%
}
\newcommand{\srodtytul}[1]{%
\subsection*{\typosubsection{#1}}%
}

\newcommand{\naglowekscena}[1]{%
\subsubsection*{\typosubsubsection{#1}}%
}
\newcommand{\naglowekrozdzial}[1]{%
{\raggedright\subsubsection*{\typosubsubsection{#1}}}%
}

\newcommand{\naglowekosoba}[1]{%
\par{\textsc{#1}}\nopagebreak%
}
\newcommand{\naglowekpodrozdzial}[1]{%
\par{#1}\nopagebreak%
}

\newcommand{\miejsceczas}[1]{%
\par{\emph{#1}}%
}
\newcommand{\didaskalia}[1]{%
\par{\emph{#1}}%
}

\newcommand{\akap}[1]{%
\par{#1}%
}
\newcommand{\akapdialog}[1]{%
\par{#1}%
}
\newcommand{\akapcd}[1]{%
\par{#1}%
}

\newcommand{\mottopodpis}[1]{%
\begin{em}%
\begin{flushright}%
#1%
\end{flushright}%
\end{em}%
}

\newcommand{\strofa}[1]{%
\par{\noindent{\ignorespaces#1\vspace{1em}}}%
}

\newcommand{\wers}[1]{#1}

\newcommand{\wersakap}[1]{%
\hspace*{1em}#1%
}
\newcommand{\werscd}[1]{%
\hspace*{8em}#1%
}
\newcommand{\werswciety}[2][1em]{%
\hspace*{#1}#2%
}

\ifshowfootnotes
  \newcommand{\pa}[1]{\NoCaseChange{\footnote{#1}}}
  \newcommand{\pe}[1]{\NoCaseChange{\footnote{#1}}}
  \newcommand{\pr}[1]{\NoCaseChange{\footnote{#1}}}
  \newcommand{\pt}[1]{\NoCaseChange{\footnote{#1}}}
\else
  \newcommand{\pa}[1]{}
  \newcommand{\pe}[1]{}
  \newcommand{\pr}[1]{}
  \newcommand{\pt}[1]{}
\fi

\newcommand{\mat}[1]{$#1$}

\newcommand{\didasktekst}[1]{%
\emph{#1}%
}
\newcommand{\slowoobce}[1]{%
\emph{#1}%
}
\newcommand{\tytuldziela}[1]{%
\emph{#1}%
}
\newcommand{\wyroznienie}[1]{%
\emph{#1}%
}

\newcommand{\osoba}[1]{%
#1%
}

\newcommand{\sekcjaswiatlo}{%
\vspace{30pt}%
}

\newcommand{\sekcjaasterysk}{%
\vspace{10pt}%
\begin{center}%
\par{*}%
\end{center}%
}

\newcommand{\separatorlinia}{%
\vspace{10pt}%
\hrule{}%
\vspace{10pt}%
}

\newcommand{\motyw}[2][0]{%
\ifshowthemes
\mbox{}%
\marginpar{%
\vspace{-8pt}%
\vspace{-#1\baselineskip}%
\raggedright{\hspace{0pt}%
\footnotesize{\color{theme}{#2}}}%
\vspace{\baselineskip}%
}%
\fi
}
