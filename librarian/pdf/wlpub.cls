% -*- coding: utf-8 -*-
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{wlpub}[2011/11/28 wolnelektury.pl book style]

% PDF customizations
%
% nofootnotes - disable generation of footnotes
% nothemes - disable generation of themes
% defaultleading - default leading
% onehalfleading - leading of 1.5 (interlinia)
% doubleleading - double leading (interlinia)
% a4paper,... - paper size as required by LaTeX
% nowlfont - don't use customized WL font

%\RequirePackage{geometry}
\RequirePackage{setspace}
\RequirePackage{type1cm}
\RequirePackage{amssymb}
\RequirePackage{amsmath}
\RequirePackage{paralist}
\RequirePackage[normalem]{ulem}
%\DeclareOption{13pt}{%
%\AtEndOfClass{%
% font size definitions, similar to ones in /usr/share/texmf-texlive/tex/latex/base/
%% \renewcommand\normalsize{%
%%    \@setfontsize\normalsize{13pt}{14.5pt}%
%%    \abovedisplayskip 12\p@ \@plus3\p@ \@minus7\p@
%%    \abovedisplayshortskip \z@ \@plus3\p@
%%    \belowdisplayshortskip 6.5\p@ \@plus3.5\p@ \@minus3\p@
%%    \belowdisplayskip \abovedisplayskip
%%    \let\@listi\@listI}\normalsize%
%% \renewcommand\footnotesize{%
%%    \@setfontsize\footnotesize\@xpt\@xiipt
%%    \abovedisplayskip 10\p@ \@plus2\p@ \@minus5\p@
%%    \abovedisplayshortskip \z@ \@plus3\p@
%%    \belowdisplayshortskip 6\p@ \@plus3\p@ \@minus3\p@
%%    \def\@listi{\leftmargin\leftmargini
%%                \topsep 6\p@ \@plus2\p@ \@minus2\p@
%%                \parsep 3\p@ \@plus2\p@ \@minus\p@
%%                \itemsep \parsep}%
%%    \belowdisplayskip \abovedisplayskip
%}%
%}%
%}

%% \DeclareOption{14pt}{\renewcommand{\normalsize}{\AtEndOfClass{\fontsize{14}{17}\selectfont}}}

\DeclareOption{defaultleading}{}
\DeclareOption{doubleleading}{\AtBeginDocument{\doublespacing}}%\setlength{\leading}{1em plus 0.5ex minus 0.2ex}}
\DeclareOption{onehalfleading}{\AtBeginDocument{\onehalfspacing}}%\setlength{\leading}{1em plus 0.5ex minus 0.2ex}}

%% This does not really work, since dvipdfm(x) will use it's configuration in /etc/texmf/dvipdfm(x) and force a global paper size setting.
\DeclareOption{a5paper}{%
      \setlength{\paperheight}{210mm}%
      \setlength{\paperwidth}{148mm}}
% a5paper dropped down size
\newif\ifcutafivepaper \cutafivepaperfalse
\DeclareOption{a5paperdd}{%
  \setlength{\paperheight}{225mm}%
  \setlength{\paperwidth}{160mm}%
  \cutafivepapertrue
}

\newif\ifshowfootnotes \showfootnotestrue
\DeclareOption{nofootnotes}{\showfootnotesfalse}

\newif\ifshowthemes \showthemestrue
\DeclareOption{nothemes}{\showthemesfalse}

\newif\ifenablewlfont \enablewlfonttrue
\DeclareOption{nowlfont}{\enablewlfontfalse}


\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extbook}}
\ProcessOptions\relax
\LoadClass{extbook}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usepackage{trace}
\usepackage{caption}
\usepackage{tabularx}
\usepackage[MeX]{polski}
\usepackage{icomma}
\usepackage[xetex]{graphicx}
\usepackage{fontspec}
\usepackage{xunicode}
\usepackage{xltxtra}
\usepackage{trimspaces}
\usepackage{color}
\usepackage[overload]{textcase}
\usepackage{scalefnt}
\usepackage[colorlinks=true,linkcolor=black,setpagesize=false,urlcolor=black,xetex]{hyperref}
\usepackage{fancyhdr}
\usepackage[explicit]{titlesec}
\usepackage{fnpos}
\usepackage{printlen}
\usepackage{calc}
\pagestyle{plain}
% bottom figure below footnotes
\makeFNabove


%%%%%%%%%%%%%%%%%%%%%%% Paper size
\setlength\baselineskip{7.14pt}
\ifcutafivepaper
  \usepackage[%
    paperwidth=160mm,%
    paperheight=225mm,%
    text={117mm,162mm},% 
    top=30mm,% 
    headsep=8mm,%
    left=23mm,%
    right=30mm]{geometry}%
\else
  \usepackage[%
    top=\dimexpr14.5mm+\baselineskip-16pt\relax, % margin will be smaller to accomodate for bigger header (16pt) 
    headsep=3\baselineskip,
    headheight=16pt,
    bottom=26.3mm,%
    inner=14.5mm,%
    outer=22.5mm,%
    textheight=\dimexpr7.14pt*(32*2+1)\relax,%
    includehead]{geometry}
\fi

%%%%%%%%%%%%%%%%%%%%%%%% Fonts

\setmainfont[
ItalicFont = CrimsonText-Italic,
BoldFont = CrimsonText-Bold,
BoldItalicFont = CrimsonText-BoldItalic,
Ligatures={Common, Contextual},
SmallCapsFont = CrimsonText-Roman,
SmallCapsFeatures={Letters=SmallCaps},
Mapping=tex-text
]{CrimsonText-Roman}
\newfontface\sb{CrimsonText-Semibold}
\newfontface\intro{Archivo-Black}

%% For faking small caps You burn in typographic hell.
\makeatletter
\newlength\fake@f
\newlength\fake@c
\def\fakesc#1{%
  \begingroup%
  \xdef\fake@name{\csname\curr@fontshape/\f@size\endcsname}%
  \fontsize{\fontdimen8\fake@name}{\baselineskip}\selectfont%
  \uppercase{#1}%
  \endgroup%
}
\makeatother


\renewcommand{\normalsize}{\fontsize{10.4}{14.28}\addfontfeature{LetterSpace=0.3}\selectfont}
\setlength{\parindent}{4mm}
\setlength{\parskip}{0mm}

\renewcommand{\large}{\fontsize{14}{14.28}\selectfont} % srodtytul
\renewcommand{\small}{\fontsize{8}{14.28}\selectfont} % paginy
\renewcommand{\Large}{\fontsize{15}{21.42}\selectfont} % tytuł rozdziału
\renewcommand{\huge}{\fontsize{18}{21.6}\selectfont} % wyimek
\renewcommand{\Huge}{\fontsize{24}{40}\selectfont} % cover
\renewcommand{\footnotesize}{\fontsize{9}{10.74}\selectfont}



\definecolor{stoK}{cmyk}{0,0,0,1}
\definecolor{theme}{gray}{.3}
%\color{stoK}


%%%%%%%%%%%%%%%%%%%%%% Headings.
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\makeatletter
%%%%%%%%%% Nagłówek normalny
\cfoot{}
% this will go to \leftmark
\renewcommand{\chaptermark}[1]{\markboth{\MakeUppercase{#1}}{}}
\fancyhead[CE]{{\small\MakeUppercase{\@title}}}
\fancyhead[CO]{{\small\leftmark}}
\fancyhead[LE,RO]{{\small\intro\thepage}}
%%%%%%%%%% Nagłówek pierwszej strony rozdziału
\fancypagestyle{plain}{%
\fancyhf{}
\fancyhead[LE,RO]{{\small\intro\thepage}}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}}
\makeatother

%%%%%%%%%%%%%%%%%%%%%% Section title styles.
%% Sections
\titleformat{\chapter}[block]%
{\Large\intro\addfontfeature{LetterSpace=0.5,Kerning={Uppercase}}}%
{}{0pt}{\parbox{80mm}{\raggedright\MakeUppercase{#1}}}
\newlength{\chapterposcorrection}\newlength{\chapterspaceafter}
\setlength{\chapterposcorrection}{-\headsep-2\baselineskip}
\setlength{\chapterspaceafter}{14\baselineskip-14pt}%\f@size of large
\titlespacing*{\chapter}{0pt}{\chapterposcorrection}{\chapterspaceafter}

%% Subsections
\titleformat{\section}%
{\addfontfeature{LetterSpace=0.3}\large}%
{\thesection}{.5em}{\MakeUppercase{#1}}

\renewcommand{\thesection}{\Roman{section}}

\titleformat{\subsection}%
{}%
{\thesubsection}{0pt}{\fakesc{#1}}


\newcommand{\typosubsubsection}[1]{%
{\textsc{#1}}
}

%% XXX delete them
\newcommand{\typosubsection}[1]{%
{\MakeUppercase{#1}}
}

\newcommand{\typosection}[1]{%
{\addfontfeature{FakeStretch=0.96, LetterSpace=-4.0}\emph{\scalefont{2}#1}}
%{\addfontfeature{Scale=2.0, FakeStretch=0.98, LetterSpace=-2.0}\emph{#1}}
}
%%%%%%%%%%%%%%%%%% ^^

%%%%% Footnotes %%%%%%%%
\newlength{\footnoteindent}\newlength{\footnoteprespace}
\setlength{\footnoteindent}{6mm}%{3.5mm}
\setlength{\footnoteprespace}{.3em}
\makeatletter

\renewcommand\@makefnmark{%
\hspace{\footnoteprespace}\hbox{{\normalfont \@thefnmark}}%
}
\renewcommand\thefootnote{[\arabic{footnote}]}

\long\def\@makefntext#1{%
\setlength{\leftskip}{\footnoteindent}%
\setlength{\hskip}{-\footnoteindent-\footnoteprespace-.1em}%
\hb@xt@ \dimexpr\footnoteindent+\footnoteprespace%
{\@makefnmark}#1
%  \parindent 1em\noindent \hb@xt@ 1.8em{\hss \@makefnmark \enskip}#1
}

\def\trimspace#1{\trim@spaces{#1}}

\makeatother


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


\newcommand{\makecover}{

  %\pdfpagewidth=#1
  %\pdfpageheight=#2

  \thispagestyle{empty}
  \newlength{\PictHOffset}
  \newlength{\PictVOffset}
  \setlength{\PictHOffset}{1in}
  \addtolength{\PictHOffset}{\hoffset}
  \addtolength{\PictHOffset}{\oddsidemargin}

  \setlength{\PictVOffset}{1in}
  \addtolength{\PictVOffset}{\voffset}
  \addtolength{\PictVOffset}{\topmargin}
  \addtolength{\PictVOffset}{\headheight}
  \addtolength{\PictVOffset}{\headsep}
  \addtolength{\PictVOffset}{\topskip}

  \addtolength{\PictVOffset}{-\paperheight}

  \noindent\hspace*{-\PictHOffset}%
  \raisebox{\PictVOffset}[0pt][0pt]{\makebox[0pt][l]{%
      \includegraphics[height=\paperheight,width=\paperwidth]{cover.jpg}}}
  \newpage
  %\vspace{\paperheight}


  \thispagestyle{empty}
  \begin{center}
  \intro
  {
    \begin{spacing}{1.4}
    \Huge \noindent \thetitle
    \end{spacing}
  }
  \end{center}

  \vspace{2em}
  
  \begin{center}
    \intro
    {
    \huge \noindent \theauthor
    }
  \end{center}
                  %\emph{\thankyou}\\
                  %\indent\emph{You made this book possible.}
  \vspace{16em}

  \begin{center}
    \includegraphics[scale=.2]{logo.eps}
  \end{center}

  \newpage
  \thispagestyle{empty}

  \input{editorial}

  
  }



\renewcommand{\maketitle}{
    {
    \thispagestyle{empty}
    \footnotesize
    \color{theme}
    \noindent \rule{\linewidth}{0.4pt}

    \vspace{.6em}
    \color{black}
    }
}


\newcommand{\editorialsection}{

}



\newcommand{\tytul}[1]{%
#1%
\vspace{1em}%
}

\newcommand{\nazwapodutworu}[1]{%
\section*{#1}%
}

\newcommand{\autorutworu}[1]{%
#1
%\subsection*{\typosubsection{#1}}%
}

\newcommand{\dzielonadrzedne}[1]{%
\subsection*{#1}%
}

\newcommand{\nazwautworu}[1]{%
\section*{#1}%
}

\newcommand{\podtytul}[1]{%
\subsection*{\typosubsubsection{#1}}%
}

\newcommand{\podtytulpodutworu}[1]{%
\subsection*{\typosubsubsection{#1}}%
}

\newcommand{\translator}[1]{%
\subsection*{\typosubsubsection{tłum. #1}}%
}
\newcommand{\translatorsline}[1]{%
#1
}

\newcommand{\powiesc}[1]{#1}
\newcommand{\opowiadanie}[1]{#1}
\newcommand{\lirykal}[1]{#1}
\newcommand{\lirykalp}[1]{#1}
\newcommand{\dramatwierszowanyl}[1]{#1}
\newcommand{\dramatwierszowanylp}[1]{#1}
\newcommand{\dramatwspolczesny}[1]{#1}

\newcommand{\nota}[1]{%
\begin{em}%
\begin{flushright}%
#1%
\end{flushright}%
\end{em}%
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
\part{#1}%
}
\newcommand{\srodtytul}[1]{%
\subsection*{\typosubsection{#1}}%
}

\newcommand{\naglowekscena}[1]{%
\subsubsection*{\typosubsubsection{#1}}%
}

\newcommand{\theautorrozdzialu}{}

\newcommand{\autorrozdzialu}[1]{%
\renewcommand{\theautorrozdzialu}{\newline\newline#1}
}

\newcommand{\naglowekrozdzial}[1]{%
\chapter{#1\theautorrozdzialu{}}\renewcommand{\theautorrozdzialu}{}%
}

\newcommand{\naglowekosoba}[1]{%
\par{\textsc{#1}}\nopagebreak%
}
\newcommand{\naglowekpodrozdzial}[1]{%
\section{#1}\nopagebreak%
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
  \newcommand{\pa}[1]{\NoCaseChange{\footnote{#1 [przypis autorski]}}}
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

\newcommand{\ilustr}[2]{
  \vspace{1em}%
  \begin{center}%
    \par{\includegraphics[width=\textwidth]{\trimspace{#1}}\\#2}%
  \end{center}%
  \vspace{1em}%
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

\newcommand{\lista}[1]{%
\begin{compactitem}
#1
\end{compactitem}
}

\newcommand{\punkt}[1]{%
\item #1
}
\newcommand{\link}[2]{\href{#1}{\uline{#2}\footnote{#1}}}

\newcommand{\www}[1]{\url{#1}}

