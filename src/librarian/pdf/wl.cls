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

\RequirePackage{fixltx2e}
\RequirePackage{setspace}
\RequirePackage{type1cm}
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
\DeclareOption{16pt}{%
\AtEndOfClass{%
% font size definitions, similar to ones in /usr/share/texmf-texlive/tex/latex/base/
\renewcommand\normalsize{%
   \@setfontsize\normalsize{16pt}{18pt}%
   \abovedisplayskip 15\p@ \@plus3\p@ \@minus7\p@
   \abovedisplayshortskip \z@ \@plus3.5\p@
   \belowdisplayshortskip 8\p@ \@plus4\p@ \@minus3\p@
   \belowdisplayskip \abovedisplayskip
   \let\@listi\@listI}\normalsize%
\renewcommand\footnotesize{%
   \@setfontsize\footnotesize\@xpt\@xiipt
   \abovedisplayskip 12\p@ \@plus2\p@ \@minus5\p@
   \abovedisplayshortskip \z@ \@plus3.5\p@
   \belowdisplayshortskip 7\p@ \@plus3.5\p@ \@minus3\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 7\p@ \@plus2.5\p@ \@minus2.5\p@
               \parsep 3.5\p@ \@plus2.5\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}%
}%
}

\newif\iflargefont
\largefontfalse

\DeclareOption{26pt}{%
\largefonttrue
\AtEndOfClass{%
% font size definitions, similar to ones in /usr/share/texmf-texlive/tex/latex/base/
\renewcommand\normalsize{%
   \@setfontsize\normalsize{26pt}{31pt}%
   \abovedisplayskip 14\p@ \@plus6\p@ \@minus14\p@
   \abovedisplayshortskip \z@ \@plus6\p@
   \belowdisplayshortskip 13\p@ \@plus7\p@ \@minus6\p@
   \belowdisplayskip \abovedisplayskip
   \let\@listi\@listI}\normalsize%
   \setlength{\parindent}{1.5em}%
\renewcommand\footnotesize{%
   \@setfontsize\footnotesize{15pt}{20pt}
   \abovedisplayskip 20\p@ \@plus4\p@ \@minus10\p@
   \abovedisplayshortskip \z@ \@plus6\p@
   \belowdisplayshortskip 12\p@ \@plus6\p@ \@minus6\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 12\p@ \@plus4\p@ \@minus4\p@
               \parsep 6\p@ \@plus4\p@ \@minus\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}%
\renewcommand\LARGE{\@setfontsize\LARGE{41pt}{50pt}}%
\renewcommand\huge{\@setfontsize\huge{49pt}{60pt}}%
}%
}

%  not supported on texlive version on jessie, and has weird side effects in some readers
%% \XeTeXgenerateactualtext=1

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

\newif\ifendnotes \endnotesfalse
\DeclareOption{endnotes}{\endnotestrue}

\newif\ifshowthemes \showthemestrue
\DeclareOption{nothemes}{\showthemesfalse}

\newif\ifenablewlfont \enablewlfonttrue
\DeclareOption{nowlfont}{\enablewlfontfalse}

\newif\ifshowtoc \showtoctrue
\DeclareOption{notoc}{\showtocfalse}

%\newif\ifsansfont \sansfontfalse
%\DeclareOption{sansfont}{\sansfonttrue}

\newif\ifmargins \marginstrue
\DeclareOption{nomargins}{\marginsfalse}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax
\LoadClass[a4paper,oneside]{book}


\usepackage{trace}

\usepackage[MeX]{polski}

\usepackage[xetex]{graphicx}
\usepackage{fontspec}
\usepackage{xunicode}
\usepackage{xltxtra}

\usepackage{longtable}
\usepackage{tabu}
\usepackage{unicode-math}
\setmathfont{Latin Modern Math}

\usepackage{wrapfig}


\ifendnotes
  \usepackage{enotez}
  \setenotez{list-name=Przypisy}
  \setenotez{backref=true}
\fi


\usepackage[overload]{textcase}
\usepackage{scalefnt}
\usepackage[colorlinks=true,linkcolor=black,setpagesize=false,urlcolor=black,xetex]{hyperref}

%\ifsansfont
%\renewcommand{\familydefault}{\sfdefault}
%\fi

\newfontfamily\alien[
SmallCapsFeatures = {Letters={SmallCaps,UppercaseSmallCaps}},
Numbers=OldStyle,
Scale=0.85,
LetterSpace=-1.0
] {DejaVu Serif}

\newfontfamily\fallback[
SmallCapsFeatures = {Letters={SmallCaps,UppercaseSmallCaps}},
Numbers=OldStyle,
Scale=0.85,
LetterSpace=-1.0
] {OpenSans-VariableFont_wdth,wght.ttf}

\ifenablewlfont
\setmainfont [
%ExternalLocation,
UprightFont = JunicodeWL-Regular,
ItalicFont = JunicodeWL-Italic,
BoldFont = JunicodeWL-Regular,
BoldItalicFont = JunicodeWL-Italic,
SmallCapsFont = JunicodeWL-Regular,
SmallCapsFeatures = {Letters={SmallCaps,UppercaseSmallCaps}},
Numbers=OldStyle,
Scale=1.04,
LetterSpace=-1.0
] {JunicodeWL}

%\setmainfont [
%UprightFont = NotoSerif-Regular,
%ItalicFont = NotoSerif-Italic,
%BoldFont = NotoSerif-Regular,
%BoldItalicFont = NotoSerif-Italic,
%SmallCapsFont = NotoSerif-Regular,
%SmallCapsFeatures = {Letters={SmallCaps,UppercaseSmallCaps}},
%Scale=1.04,
%LetterSpace=-1.0
%] {NotoSerif}

%\setsansfont [
%UprightFont = NotoSansDisplay-Regular,
%ItalicFont = NotoSansDisplay-Italic,
%BoldFont = NotoSansDisplay-Regular,
%BoldItalicFont = NotoSansDisplay-Italic,
%SmallCapsFont = NotoSansDisplay-Regular,
%SmallCapsFeatures = {Letters={SmallCaps,UppercaseSmallCaps}},
%Scale=1.04,
%LetterSpace=-1.0
%] {NotoSansDisplay}

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
\usepackage{marginnote}


\makeatletter

% bottom figure below footnotes
\usepackage{fnpos}
\makeFNabove

\usepackage{color}
\definecolor{theme}{gray}{.3}

\ifmargins
\setlength{\marginparsep}{2em}
\setlength{\marginparwidth}{8.5em}
\setlength{\oddsidemargin}{0pt}
\setlength{\voffset}{0pt}
\setlength{\topmargin}{0pt}
\setlength{\headheight}{0pt}
\setlength{\headsep}{0pt}
\setlength{\textheight}{24cm}
\else
\addtolength{\oddsidemargin}{-.875in}
\addtolength{\evensidemargin}{-.875in}
\addtolength{\textwidth}{1.75in}

\addtolength{\topmargin}{-.875in}
\addtolength{\textheight}{1.5in}
\fi

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\lfoot{{\footnotesize \textsc{\@author} \emph{\@title}}}
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

\newcommand{\makecover}[2]{
        \pdfpagewidth=#1
        \pdfpageheight=#2

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
        \addtolength{\PictVOffset}{-\pdfpageheight}

        \noindent\hspace*{-\PictHOffset}%
        \raisebox{\PictVOffset}[0pt][0pt]{\makebox[0pt][l]{%
            \includegraphics[height=\pdfpageheight,width=\pdfpagewidth]{cover.png}}}
        \clearpage

        \setlength{\pdfpagewidth}{210mm}
        \setlength{\pdfpageheight}{297mm}
}


\renewcommand{\maketitle}{
    {
    \thispagestyle{empty}
    \footnotesize
    \color{theme}

    \noindent \begin{minipage}[t]{.35\textwidth}\vspace{0pt}
        \href{http://www.wolnelektury.pl}{\xbox{\includegraphics[width=\textwidth]{wl-logo.png}}}
    \end{minipage}
    \begin{minipage}[t]{.65\textwidth}\vspace{0pt}

    \ifflaglessadvertising
    \else
        \href{\bookurl}{Ta lektura}, podobnie jak tysiące innych, jest dostępna on-line na stronie
        \href{https://wolnelektury.pl/}{wolnelektury.pl}.
        \vspace{.5em}
    \fi

    \ifdefined\thanknote
        \thanknote
        \vspace{.5em}
    \fi

    Utwór opracowany został w ramach projektu \href{https://wolnelektury.pl/}{Wolne Lektury}
    przez \href{https://fundacja.wolnelektury.pl}{fundację Wolne Lektury}.

    \end{minipage}
    \noindent \rule{\linewidth}{0.4pt}

    \vspace{.6em}
    \color{black}
    }
}

\newcommand{\editorialsection}{
  \begin{figure}[b!]
  {
    \footnotesize
    \color{theme}
    \noindent \rule{\linewidth}{0.4pt}

    \ifdefined\sponsors
        \marginnote{%
            \centering%
            \sponsors%
        }
    \fi

    Wszystkie zasoby Wolnych Lektur możesz swobodnie wykorzystywać,
    publikować i rozpowszechniać pod warunkiem zachowania warunków licencji i zgodnie
    z~\href{https://wolnelektury.pl/info/zasady-wykorzystania/}{Zasadami wykorzystania Wolnych Lektur}.

    \rightsinfo

    Wszystkie materiały dodatkowe (przypisy, motywy literackie) są udostępnione na
    \href{https://artlibre.org/licence/lal/pl/}{Licencji Wolnej Sztuki 1.3}.

    Fundacja Wolne Lektury zastrzega sobie prawa do wydania
    krytycznego zgodnie z art. Art.99(2) Ustawy o prawach autorskich
    i prawach pokrewnych. Wykorzystując zasoby z Wolnych Lektur,
    należy pamiętać o zapisach licencji oraz zasadach, które spisaliśmy
    w~\href{https://wolnelektury.pl/info/zasady-wykorzystania/}{Zasadach wykorzystania Wolnych Lektur}.
    Zapoznaj się z nimi, zanim udostępnisz dalej nasze książki.
    \vspace{.6em}

    E-book można pobrać ze strony: \href{\bookurl}{\bookurl}

    \vspace{.6em}
    \sourceinfo

    \publisherinfo

    \description
    \vspace{.6em}

    \editors

    \ifdefined\funders
        \vspace{.6em}
        \funders
    \fi

    \ifdefined\coverby
        \vspace{.6em}
        \coverby
    \fi

    \ifdefined\isbn
        \vspace{.6em}
        \isbn
    \fi

    \vspace{.6em}
    \emph{Wesprzyj Wolne Lektury!}

    Wolne Lektury to projekt fundacji Wolne Lektury – organizacji
    pożytku publicznego działającej na rzecz wolności korzystania
    z dóbr kultury.

    Co roku do domeny publicznej przechodzi twórczość kolejnych autorów.
    Dzięki Twojemu wsparciu będziemy je mogli udostępnić wszystkim bezpłatnie.

    \vspace{.6em}
    \emph{Jak możesz pomóc?}

    Przekaż 1,5\% podatku na rozwój Wolnych Lektur:
    Fundacja Wolne Lektury, KRS 0000070056.

    \href{https://wolnelektury.pl/pomagam/}{Wspieraj Wolne Lektury} i pomóż nam rozwijać bibliotekę.

    Przekaż darowiznę na konto:
    \href{https://fundacja.wolnelektury.pl/pomoz-nam/darowizna/}{szczegóły na stronie Fundacji}.

    \color{black}
  }
  \end{figure}
}


\newcommand{\typosubsubsection}[1]{%
\iflargefont
{\textsc{\scalefont{2}#1}}
\else
{\textsc{#1}}
\fi
}

\newcommand{\typosubsection}[1]{%
{\addfontfeature{
SizeFeatures={
  {Size={-10}, Scale=1.2, FakeStretch=1.00, LetterSpace=8.0 },
  {Size={10.5-12}, Scale=1.2, FakeStretch=1.00, LetterSpace=8.0 },
  {Size={12-}, FakeStretch=2.0, LetterSpace=8.0 }
},
Letters={Uppercase}
}
\iflargefont
\MakeUppercase{\scalefont{2}#1}
\else
\MakeUppercase{#1}
\fi}
}

\newcommand{\typosection}[1]{%
\iflargefont
{\addfontfeature{FakeStretch=0.96, LetterSpace=-4.0}\emph{\scalefont{4}#1}}
\else
{\addfontfeature{FakeStretch=0.96, LetterSpace=-4.0}\emph{\scalefont{2}#1}}
\fi
%{\addfontfeature{Scale=2.0, FakeStretch=0.98, LetterSpace=-2.0}\emph{#1}}
}


\DeclareRobustCommand\authortoctext[1]{%
{\addvspace{10pt}\nopagebreak\leftskip0em\relax
\rightskip \@tocrmarg\relax
\noindent\itshape#1\par}}

\newcommand\authortoc[1]{%
  \gdef\chapterauthor{#1}%
  \addtocontents{toc}{\authortoctext{#1}}}


\newcommand{\tytul}[1]{%
#1%
\vspace{1em}%
}

\newcommand{\nazwapodutworu}[2]{%
\vspace{5ex}%
\section*{\typosection{#1}}%
\addcontentsline{toc}{section}{#2}%
}

\newcommand{\nazwanadpodutworu}[2]{%
\authortoc{}%
\nazwapodutworu{#1}{#2}%
\authortoc{}%
}

\newcommand{\autorutworu}[1]{%
\subsection*{\typosubsection{#1}}%
}

\newcommand{\autorpodutworu}[1]{%
\vspace{5ex}%
\subsection*{\typosubsection{#1}}%
\authortoc{#1}%
}

\newcommand{\dzielonadrzedne}[1]{%
\subsection*{\typosubsubsection{#1}}%
}

\newcommand{\nazwautworu}[1]{%
\vspace{5ex}%
\section*{\typosection{#1}}%
}

\newcommand{\podtytul}[1]{%
\subsection*{\typosubsubsection{#1}}%
}

\newcommand{\translator}[1]{%
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
\par{\raggedleft \emph{#1}}%
\vspace{5ex}%
}

\newcommand{\dedykacja}[1]{%
\begin{em}%
\begin{flushright}%
#1%
\end{flushright}%
\end{em}%
}

\newlength{\fboxhsep}
\newlength{\fboxvsep}

\newlength{\fboxtoprule}
\newlength{\fboxbottomrule}
\newlength{\fboxleftrule}
\newlength{\fboxrightrule}

\ifshowthemes
\setlength{\fboxhsep}{5\fboxsep}
\setlength{\fboxvsep}{20\fboxsep}
\fi

\setlength{\fboxtoprule}{\fboxrule}
\setlength{\fboxleftrule}{\fboxrule}
\setlength{\fboxrightrule}{\fboxrule}
\setlength{\fboxbottomrule}{\fboxrule}



\def\@frameb@xother#1{%
  \@tempdima\fboxtoprule
  \advance\@tempdima\fboxvsep
  \advance\@tempdima\dp\@tempboxa
  \hbox{%
    \lower\@tempdima\hbox{%
      \vbox{%
        \hrule\@height\fboxtoprule
        \hbox{%
          \vrule\@width\fboxleftrule
          #1%
          \vbox{%
            \vskip\fboxvsep
            \box\@tempboxa
            \vskip\fboxvsep}%
          #1%
          \vrule\@width\fboxrightrule}%
        \hrule\@height\fboxbottomrule}%
    }%
  }%
}


\long\def\fboxother#1{%
  \leavevmode
  \setbox\@tempboxa\hbox{%
    \color@begingroup
    \kern\fboxhsep{#1}\kern\fboxhsep
    \color@endgroup}%
  \@frameb@xother\relax}

\newcommand{\myfbox}[3]{%
  \begingroup
  \setlength{\fboxhsep}{#1}
  \setlength{\fboxvsep}{#2}
  \fboxother{#3}

  \endgroup
}

\newcommand{\ramka}[1]{%
\par\vspace{1em}%
\edef\myindent{\the\parindent}%
\noindent\myfbox{1em}{1em}{%
\parbox{\dimexpr \textwidth - 2\fboxhsep - 2\fboxrule\relax}{%
\setlength{\parindent}{\myindent}%
#1%
}}%
\vspace{1em}%
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
\item[]{#1}%
}

\newcommand{\kwestia}[1]{%
\par{#1}%
}

\newcommand{\naglowekakt}[2]{%
\pagebreak
\subsection*{\typosubsection{\huge #1}}%
\addcontentsline{toc}{subsection}{#2}%
\vspace{5ex}%
}

\newcommand{\podtytulakt}[1]{%
\par{\typosubsubsection{\LARGE #1}}%
\vspace{5ex}%
}

\newcommand{\naglowekczesc}[2]{%
\pagebreak
\subsection*{\typosubsection{\huge #1}}%
\addcontentsline{toc}{subsection}{#2}%
\vspace{5ex}%
}

\newcommand{\podtytulczesc}[1]{%
\par{\typosubsubsection{\LARGE #1}}%
\vspace{5ex}%
}

\newcommand{\srodtytul}[1]{%
\subsection*{\typosubsection{#1}}%
}

\newcommand{\naglowekscena}[2]{%
\subsubsection*{\typosubsubsection{\LARGE #1}}%
\addcontentsline{toc}{subsubsection}{#2}%
\vspace{5ex}%
}

\newcommand{\podtytulscena}[1]{%
\par{\large #1}%
\vspace{5ex}%
}

\newcommand{\naglowekrozdzial}[2]{%
\subsubsection*{\typosubsubsection{\LARGE #1}}%
\addcontentsline{toc}{subsubsection}{#2}%
\vspace{5ex}%
}

\newcommand{\podtytulrozdzial}[1]{%
\par{\large #1}%
\vspace{5ex}%
}

\newcommand{\naglowekosoba}[1]{%
\medskip%
\par{\textsc{\MakeLowercase{#1}}}\nopagebreak%
}
\newcommand{\naglowekpodrozdzial}[1]{%
\vspace{5ex}\par{#1}\nopagebreak%
}

\newcommand{\podtytulpodrozdzial}[1]{%
\par{#1}\nopagebreak%
}

\newcommand{\miejsceczas}[1]{%
\par{\emph{#1}}%
}
\newcommand{\didaskalia}[1]{%
\par{\emph{#1}}%
}

\usepackage{framed}
\usepackage{intcalc}
\usepackage{color}
\definecolor{gray}{RGB}{200,200,200}
%\newcounter{parnum}
\newlength{\parnumwidth}
\setlength{\parnumwidth}{3em}
\newcommand{\N}{%
  \leavevmode\refstepcounter{parnum}\reversemarginpar%
  \marginnote{\textcolor{gray}{\small{\theparnum}}}%
  \reversemarginpar}
\newcommand{\Nw}{%
  \leavevmode\refstepcounter{parnum}\reversemarginpar%
  \ifnum\intcalcMod{\value{parnum}}{5}=0%
  \marginnote{\textcolor{gray}{\small{\theparnum}}}%
  \fi\reversemarginpar}
\renewcommand{\N}{}
\renewcommand{\Nw}{}

\newcommand{\akap}[1]{%
\par{\N#1}%
}
\newcommand{\akapdialog}[1]{%
\par{\N#1}%
}
\newcommand{\akapcd}[1]{%
\par{\N#1}%
}

\newcommand{\werset}[1]{%
\par{\noindent{\ignorespaces#1\vspace{1em}}}%
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

\newcommand{\wers}[1]{\Nw#1}

\newcommand{\wersakap}[1]{%
\Nw\hspace*{1em}#1%
}
\newcommand{\werscd}[1]{%
\Nw\hspace*{8em}#1%
}
\newcommand{\werswciety}[2][1em]{%
\Nw\hspace*{#1}#2%
}
\newcommand{\wersdoprawej}[1]{%
\Nw\hspace*{\fill}#1%
}

\ifshowfootnotes
  \ifendnotes
    \newcommand{\pa}[1]{\NoCaseChange{\endnote{#1 [przypis autorski]}}}
    \newcommand{\pe}[1]{\NoCaseChange{\endnote{#1 [przypis edytorski]}}}
    \newcommand{\pr}[1]{\NoCaseChange{\endnote{#1 [przypis redakcyjny]}}}
    \newcommand{\pt}[1]{\NoCaseChange{\endnote{#1 [przypis tłumacza]}}}
    \newcommand{\ptrad}[1]{\NoCaseChange{\endnote{#1 [przypis z tradycji]}}}
  \else
    \newcommand{\pa}[1]{\NoCaseChange{\footnote{#1 [przypis autorski]}}}
    \newcommand{\pe}[1]{\NoCaseChange{\footnote{#1 [przypis edytorski]}}}
    \newcommand{\pr}[1]{\NoCaseChange{\footnote{#1 [przypis redakcyjny]}}}
    \newcommand{\pt}[1]{\NoCaseChange{\footnote{#1 [przypis tłumacza]}}}
    \newcommand{\ptrad}[1]{\NoCaseChange{\footnote{#1 [przypis z tradycji]}}}
  \fi
\else
  \newcommand{\pa}[1]{}
  \newcommand{\pe}[1]{}
  \newcommand{\pr}[1]{}
  \newcommand{\pt}[1]{}
  \newcommand{\ptrad}[1]{}
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
\newcommand{\indeksdolny}[1]{%
\textsubscript{#1}%
}
\newcommand{\wiekszeodstepy}[1]{%
\spaceskip 3\fontdimen2\font plus 3\fontdimen3\font minus 3\fontdimen4\font \relax%
#1%
\spaceskip \fontdimen2\font plus \fontdimen3\font minus \fontdimen4\font \relax%
}

\newcommand{\osoba}[1]{%
{\scshape \MakeLowercase{#1}}%
}
\newcommand{\br}[1]{%
\\
}


\newcommand{\wllist}[1]{%
\begin{quotation}%
#1%
\end{quotation}%
}
  
\newcommand{\adresat}[1]{%
\par{\N#1}%
}
\newcommand{\miejscedata}[1]{%
\begin{flushright}%
\par{\N#1}%
\end{flushright}%
}
\newcommand{\nagloweklistu}[1]{%
\begin{center}%
\par{\N#1}%
\end{center}%
}
\newcommand{\pozdrowienie}[1]{%
\begin{flushright}%
\par{\N#1}%
\end{flushright}%
}
\newcommand{\podpis}[1]{%
\begin{flushright}%
\par{\N#1}%
\end{flushright}%
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

\newcommand{\ilustr}[2]{%
\vspace{1em}%
\par{\noindent\includegraphics[width=\linewidth]{#1}}%
\vspace{1em}
}
