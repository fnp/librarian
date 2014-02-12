% -*- coding: utf-8 -*-
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fnprep}[2011/11/28 Modern Poland Foundation Report style]


%\RequirePackage{geometry}
\RequirePackage{setspace}
\RequirePackage{type1cm}
\RequirePackage{amssymb}
\RequirePackage{amsmath}
\RequirePackage{paralist}
\RequirePackage[normalem]{ulem}
\RequirePackage{xifthen}
\RequirePackage{environ} % environments with \BODY, for wyimek


\DeclareOption*{\PassOptionsToClass{\CurrentOption}{report}}
\ProcessOptions\relax
\LoadClass{report}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usepackage{multicol}
%\usepackage[landscape]{geometry}
\usepackage[explicit]{titlesec}
\usepackage{titletoc}
\usepackage{fancyhdr}
\usepackage[MeX]{polski}

\usepackage{trace}
\usepackage{caption}
\usepackage{tabularx}
\usepackage{icomma}
\usepackage[xetex]{graphicx}
\usepackage[silent]{fontspec} % silent - no warnings, quiet - warn only to log
\usepackage{xunicode}
\usepackage{xltxtra}
%\usepackage{trimspaces} % imported by something else?
\usepackage{xcolor}
\usepackage[overload]{textcase}
\usepackage{scalefnt}
\usepackage[colorlinks=false,linkcolor=white,pdfborder={0,0,0},setpagesize=false,urlcolor=black,xetex,linktocpage]{hyperref}
%\usepackage{hyperref}
\usepackage{endnotes}
%\usepackage{fnpos}
\usepackage{printlen}
\usepackage{calc}
\usepackage[stable]{footmisc}

%http://tex.stackexchange.com/questions/40510/set-first-paragraph-no-indentation-after-re-definition-of-section#40512

\usepackage{chngcntr}
\counterwithout{footnote}{chapter}
\usepackage{microtype}


%%% Hyphenation opts:
%\pretolerance=10000
\tolerance=2600
\emergencystretch=30pt




%%%%%%%%%%%%%%%%%%%%%%% Paper size
%\setlength\baselineskip{7.14pt}
%% \ifcutafivepaper
%%   \usepackage[%
%%     paperwidth=160mm,%
%%     paperheight=225mm,%
%%     text={117mm,162mm},%
%%     top=30mm,%
%%     headsep=8mm,%
%%     left=23mm,%
%%     right=30mm]{geometry}%
%% \else
%%   \usepackage[%
%%     top=\dimexpr14.5mm+\baselineskip-16pt\relax, % margin will be smaller to accomodate for bigger header (16pt)
%%     headsep=3\baselineskip,
%%     headheight=16pt,
%%     bottom=26.3mm,%
%%     inner=14.5mm,%
%%     outer=22.5mm,%
%%     textheight=\dimexpr7.14pt*(32*2+1)\relax,%
%%     includehead]{geometry}
%% \fi

\usepackage[%
  paperwidth=297mm,%
  paperheight=210mm,%
  top=22.578mm,%
  left=15mm,%
  right=20mm,%
  bottom=24.439mm,%
  headsep=19pt,% 2x grid(14) - 9 (text font size)
]{geometry}%
\setlength\columnsep{10mm}


%%%%%%%%%%%%%%%%%%%%%%%% Fonts

\setmainfont[
ItalicFont = Lato-Italic,
BoldFont = Lato-Bold,
BoldItalicFont = Lato-BoldItalic,
Ligatures={Common, Contextual},
SmallCapsFont = Lato-Regular,
SmallCapsFeatures={Letters=SmallCaps},
Mapping=tex-text
]{Lato-Regular}
\newfontface\latoblack{Lato-Black}
\newfontface\headfont{LeagueGothic-Regular}
%% Lato Light 

\setlength{\parindent}{3mm}
\setlength{\parskip}{0mm}

% \normalsize – normalny tekst 
% \large - normalny tekst headingowy (nie wiem czy jest inny niz normalsize?)
% \Large - troche większy tekst headingowy (spis treści)
% \huge - pagina tytuł rozdziału
% \Huge - naglowek na szarym tle

% grid 14, normal 9/12, 
% sródtytuły leage 10/8 14
% XXXX pagina: (mała? nie uzywana!)league 8, kerning 60 -› (30, 90), przy nowoczesna polska 100
% pagina: 28pt od top: 10mm  CMY 0 75 100
% kolumna-›teskt base 2xgrid
% tabela header 14pt, LEAGE GOT RE [pad: left:3mm, 1,41mm od góry 
% tabela  rynna 5mm
% tabela kreska 0.7pt pomarancz, potem 0.5pt też pomarańcz
% tabela tekst: 8.5/11pt lato regular (wtedy pomaranczem wyróżnienia)
% kern 5
% (bez gridu) (abo 8.5/11pt reglar) , poza interlinią 1mm odpycha enter
% 
% footer: --||-- 
% footer LATO BLACK 15 -- pagina(strona) TYLKO Z PRAWEJ
% footer srodek. league gothic  10  k70 
% toc:wstep leag gothic 38  kern 75
% toc: 11pkt na grid 7 
% marginesy: top: 22.578 mm bottom 24.439mm rynna 10; out 20mm, ins
% 15mm
% sród->text base 2xgrid
% toc: wstep->text 3xgrid,
% toc: left: 25mm  right: 25mm
% toc długość tytułu (łamanie) 10m od końca 
% toc: od numeru enspace (indent)
% footer 2xgrid od dołu 9.7mm
% master toc: margin left: -width - 10 / 2 ; 136mm [3x łam]
% footnotes SOURCE SANS PRO 8/11pt semibold na gridzie (ale nie musi) spacing
% 100 
% master toc: 11pt/21pt leage na pół-grid (jak ejst mniejsze
% --licencja to 10pt!)
% master toc head 15pt, 
% master toc wpisy: 11pt - (można 11pt + black)
% TYtUL leag gothi  46pt
% 
% sponsorzy np 9pt
\newcommand{\headingbig}{\fontsize{28}{28}\selectfont}
\renewcommand{\Huge}{\fontsize{38}{42}\selectfont}
\renewcommand{\huge}{\fontsize{15}{21}\selectfont}
\renewcommand{\LARGE}{\fontsize{14}{14}\selectfont}
\renewcommand{\large}{\fontsize{10}{21}\selectfont}
\renewcommand{\Large}{\fontsize{11}{14}\selectfont}
\newcommand{\TOCtext}{\fontsize{11}{21}\selectfont}
\renewcommand{\normalsize}{\fontsize{9}{14}\selectfont}
\renewcommand{\footnotesize}{\fontsize{8}{10.5}\selectfont} % 
\renewcommand{\scriptsize}{\fontsize{8.5}{11}\selectfont}
\newcommand{\titlesize}{\fontsize{46}{46}\selectfont}
\newcommand{\footerbig}{\fontsize{15}{15}\selectfont}
\newcommand{\footernormal}{\fontsize{10}{10}\selectfont}


%% \renewcommand{\normalsize}{\fontsize{10.4}{14.28}\addfontfeature{LetterSpace=3.0}\selectfont}
%% \renewcommand{\large}{\fontsize{14}{14.28}\addfontfeature{LetterSpace=3.0,Letters=Uppercase}\selectfont} % srodtytul
%% \renewcommand{\small}{\fontsize{8}{14.28}\addfontfeature{LetterSpace=5.0}\selectfont} % paginy
%% \renewcommand{\Large}{\fontsize{15}{21.42}\addfontfeature{LetterSpace=0.0}\selectfont} % tytuł rozdziału
%% \renewcommand{\huge}{\fontsize{18}{28.56}\addfontfeature{LetterSpace=1.0}\selectfont} % wyimek
%% \renewcommand{\Huge}{\fontsize{24}{40}\selectfont} % cover
%% \renewcommand{\footnotesize}{\addfontfeature{LetterSpace=1.0}\fontsize{9}{10.74}\selectfont}



% • • • • • • • • • COLORS • •
\definecolor{stoK}{cmyk}{0,0,0,1}
\definecolor{theme}{gray}{.3}
\definecolor{headcolor}{HTML}{EA5F21}
\definecolor{graybg}{cmyk}{0,0,0,0.55}
%\color{stoK}

% • • • • • • • • METADATA • •

\makeatletter
\newcommand{\@address}{}
\newcommand{\address}[1]{\renewcommand{\@address}{#1}}
\makeatother

% • • • • • • • • HEADINGS • •
%% this will go to \leftmark

\makeatletter
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\chaptermark}[1]{\markboth{\MakeTextUppercase{#1}}{}}
% on the odd right : chapter title
\fancyhead[LE,RO]{{\color{headcolor}\headfont\headingbig\leftmark}}
\fancyfoot[RO]{{\color{gray}\latoblack\footerbig\thepage}}
\fancyfoot[RE]{{\color{gray}\headfont\footernormal\MakeTextUppercase{\@title}}}
\fancyfoot[LO]{{\color{gray}\headfont\footernormal\MakeTextUppercase{\@address}}}

\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\makeatother

%%%%%%%%%% Nagłówek pierwszej strony rozdziału
\makeatletter
\fancypagestyle{plain}{%
\fancyhf{}
\fancyfoot[RO]{{\color{gray}\latoblack\footerbig\thepage}}
\fancyfoot[LO]{{\color{gray}\headfont\footernormal\MakeTextUppercase{\@address}}}
}
\makeatother

% • • • • • • • • TITLES • • •
% no chapter numbers and no ``Rozdział'' word
%\renewcommand{\thechapter}{}
%\renewcommand{\chaptername}{}

% • chapter • • • • • • • • • •
\makeatletter\newenvironment{chaptertitlebox}{   \begin{lrbox}{\@tempboxa}\begin{minipage}[t][\dimexpr\textheight-0.5cm\relax]{\dimexpr\linewidth-0.5\columnsep\relax}}{\end{minipage}\end{lrbox}%
   \colorbox{graybg}{\raisebox{1cm}{\usebox{\@tempboxa}}}
}

\newcommand{\nochapternumbers}{
  \renewcommand{\thesection}{\@arabic \c@section .}
}
\makeatother

\nochapternumbers
\startcontents[chapter]
\titleformat{\chapter}[block]%
{\begin{chaptertitlebox}}%
{}{0pt}%
{\Huge{}\headfont\color{white}#1%
\newline\printcontents[chapter]{}{1}{}%
}%
[\end{chaptertitlebox}]

\titlespacing*{\chapter}{0pt}{0pt}{0pt}


% • section • • • • • • • • • • • • • • • 
\titleformat{\section}[runin]%
{\large\headfont%\nochapternumbers
}%
{}{0pt}{\makebox[\linewidth][l]{\color{headcolor}\raggedright{}\thesection
    #1}%
% this is just to make the spacing between section and following
% text right (newlines produce strange amount of space
\\\makebox[\linewidth][l]{~}}%

\titlecontents{section}[0pt]{\headfont\large\color{white}}%
{\thecontentslabel}{\contentsmargin{0pt}}%
{\hfill\color{white}{\thecontentspage }}


% \fboxsep=0pt % for framebox
% ramki wkokół elementów \fbox{}
%\titlespacing*{\section}{0pt}{0pt}{2\baselineskip}


%% \titleformat{\chapter}[block]%
%% {\Large\intro\addfontfeature{LetterSpace=0.5,Kerning={Uppercase}}}%
%% {}{0pt}{\parbox{80mm}{\raggedright#1}}
%% \newlength{\chapterposcorrection}\newlength{\chapterspaceafter}
%% \setlength{\chapterposcorrection}{-\headsep-2\baselineskip-2.352mm} % 2.352 is a measured correction:
%% \setlength{\chapterspaceafter}{14\baselineskip-14pt+2.352mm}%\f@size of large
%% \titlespacing*{\chapter}{0pt}{\chapterposcorrection}{\chapterspaceafter}

%% %% Sections
%% \titleformat{\section}%
%% {\addfontfeature{LetterSpace=0.3}\large}%
%% {\thesection{}.}{.5em}{\MakeTextUppercase{#1}}
%% \renewcommand{\thesection}{\Roman{section}}
%% \titlespacing*{\section}{0pt}{\baselineskip}{0em}

%% \titleformat{\subsection}[block]%
%% {}%
%% {\thesubsection{}.}{.5em}{\MakeTextUppercase{#1}.}[]

%% \renewcommand{\thesubsection}{\Alph{subsection}}
%% \titlespacing*{\subsection}{0pt}{\baselineskip}{0em}

%% \newcommand{\typosubsubsection}[1]{%
%% {\textsc{#1}}
%% }


%%%%% Footnotes (works with footmisc) %%%%%%%%
\newlength{\footnoteindent}\newlength{\footnoteprespace}
\setlength{\footnoteindent}{8mm}%{3.5mm}
\setlength{\footnoteprespace}{0em}
\makeatletter

\renewcommand\@makefnmark{%
\hspace{\footnoteprespace}
\hbox{{\normalfont \@thefnmark}}%
}
\renewcommand\thefootnote{[\arabic{footnote}]}

\setlength{\footnotemargin}{-\footnoteindent-\footnoteprespace-.3em}
\renewcommand\footnotelayout[1]{%
  \setlength{\leftskip}{\footnoteindent}#1}

%% \long\def\@makefntext#1{%
%% \setlength{\leftskip}{\footnoteindent}%
%% \setlength{\hskip}{-\footnoteindent-\footnoteprespace-.1em}%
%% \hb@xt@ \dimexpr\footnoteindent+\footnoteprespace%
%% {\@makefnmark}#1
%% %  \parindent 1em\noindent \hb@xt@ 1.8em{\hss \@makefnmark \enskip}#1
%% }

%%%%% Endnotes
\newlength{\myendnoteprespace}\setlength{\myendnoteprespace}{.5em}
\newlength{\myendnoteindent}\setlength{\myendnoteindent}{14mm+.5em}

\renewcommand\theendnote{[\roman{endnote}]}
\renewcommand\makeenmark{\hspace{\myendnoteprespace}\theenmark}
\renewcommand{\notesname}{}
\newcommand{\authornotes}{
%  \newpage
    \cleardoublepage
    \chapter{Przypisy autora}
    \setlength{\parindent}{0pt}
    \def\enotesize{\normalsize}
    \theendnotes
}
%% \newcommand{\@makeentext}[1]{%
%% \noindent\theenmark\hspace{\footnoteindent}#1
%% }

%% \def\enoteformat{\rightskip\z@ \parindent=0em
%%  \makebox[\myendnoteindent][l]{\makeenmark}} % 12.4mm - measured biggest endnote marker (in Moglen text [xxxviii])
\def\enoteformat{\rightskip\z@ \setlength{\leftskip}{\myendnoteindent-\myendnoteprespace} \parindent=0em
  \leavevmode\llap{\makebox[\myendnoteindent][l]{\makeenmark}}}


% make public
\def\trimspace#1{\trim@spaces{#1}}

\makeatother

%%%%%%%%%%%%%%%%%%%%%% Wyimki
%% \floatstyle{plain}
%% \newfloat{wyimekbox}{p}{wmk}
%% \floatname{wyimekbox}{Wyimek}

\NewEnviron{wyimek}{%
  \checkoddpage
  \ifoddpage
    \PackageWarning{wlpub}{Wyimek on odd page, omitting it ( \BODY )}
  \else
    \begin{figure}[tp]
      \begin{center}
        \begin{minipage}[t][\textheight][c]{70mm}
          \huge\it\BODY
        \end{minipage}
      \end{center}
    \end{figure}
  \fi
  \BODY
}

%% wyimek that doesn't leave text in text flow
%% TODO: reduce code duplication
\NewEnviron{wyimekextra}{%
  \checkoddpage
  \ifoddpage
    \PackageWarning{wlpub}{Wyimek on odd page, omitting it ( \BODY )}
  \else
    \begin{figure}[tp]
      \begin{center}
        \begin{minipage}[t][\textheight][c]{70mm}
          \huge\it\BODY
        \end{minipage}
      \end{center}
    \end{figure}
  \fi
}




%%%%%%%%%%%%%%%%%%%%%%%%%%


\clubpenalty=700
\widowpenalty=700
\hyphenpenalty=3500
\doublehyphendemerits=9000
\finalhyphendemerits=6000


% see http://osdir.com/ml/tex.xetex/2005-10/msg00003.html
\newsavebox{\ximagebox}\newlength{\ximageheight}
\newsavebox{\xglyphbox}\newlength{\xglyphheight}
\newcommand{\xbox}[1]
{\savebox{\ximagebox}{#1}\settoheight{\ximageheight}{\usebox {\ximapgebox}}%
\savebox{\xglyphbox}{\char32}\settoheight{\xglyphheight}{\usebox {\xglyphbox}}%
\raisebox{\ximageheight}[0pt][0pt]{%\raisebox{-\xglyphheight}[0pt] [0pt]{%
\makebox[0pt][l]{\usebox{\xglyphbox}}}%}%
\usebox{\ximagebox}%
\raisebox{0pt}[0pt][0pt]{\makebox[0pt][r]{\usebox{\xglyphbox}}}}


\newcommand{\makecover}{
  %% \paperwidth=297mm


  %% \paperheight=210mm

  \newgeometry{paperwidth=297mm,paperheight=210mm}
  \pdfpageheight=210mm
  \pdfpagewidth=297mm

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
      \includegraphics[height=\pdfpageheight,width=\pdfpagewidth]{cover.pdf}}}

  \restoregeometry
  \pdfpageheight=210mm
  \pdfpagewidth=148mm

  }

\renewcommand{\maketitle}{
  %\vspace{\paperheight}
  \thispagestyle{empty}
  \cleardoublepage
  \setcounter{page}{1}
  \thispagestyle{empty}
  \begin{center}
  \intro
  {
    \begin{spacing}{1.4}
    \Huge \noindent \thetitle
    \end{spacing}
  }
  \end{center}

  \vspace{\baselineskip}

  \begin{center}
    \intro
    {
      \huge \noindent
      \theauthor

    }
  \end{center}
                  %\emph{\thankyou}\\
                  %\indent\emph{You made this book possible.}
  \vspace{7\baselineskip}

  \begin{center}
    \includegraphics[scale=.2]{logo.eps}
  \end{center}

}


\newcommand{\editorialsection}{
  \clearpage
  \thispagestyle{empty}
  {
    \setlength{\parindent}{0mm}
    \small
  \input{editorial}
  }
}

\renewcommand*\contentsname{Spis treści}
\newcommand{\spistresci}{
{
  \intro
  \setcounter{tocdepth}{0}
  \tableofcontents
  \newpage
}
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


\newcommand{\dedykacja}[1]{%
\begin{em}%
\begin{flushright}%
#1%
\end{flushright}%
\end{em}%
}

\newcommand{\dlugicytat}[1]{%
\begin{quotation}%
\noindent{}\ignorespaces#1%
\end{quotation}%
\hspace{\parindent}
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
\subsection{#1}%
}

\newcommand{\naglowekscena}[1]{%
\subsubsection*{\typosubsubsection{#1}}%
}

\newcommand{\theautorrozdzialu}{}

\newcommand{\autorrozdzialu}[1]{%
\renewcommand{\theautorrozdzialu}{{\normalfont\normalsize\newline{}\newline{}\parbox{\textwidth}{\normalsize\it #1}}}
}


\newcommand{\naglowekrozdzial}[1]{%
\startcontents[chapter]
%
\chapter[#1]{\MakeUppercase{#1}\theautorrozdzialu{}}%
\renewcommand{\theautorrozdzialu}{}%
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
#1

% newline here needed, we don't use \par cause it ignores \noindent before
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
#1\vspace{\baselineskip}%
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


\newcommand{\mat}[1]{$#1$}

\newcommand{\didasktekst}[1]{%
\emph{#1}%
}
\newcommand{\slowoobce}[1]{%
\emph{#1}%
}
\makeatletter

\newif\ifinnota \innotafalse

\newcommand{\tytuldziela}[1]{%
  \ifinnota
   #1%
  \else
   \emph{#1}%
  \fi
}
\makeatother

\newcommand{\wyroznienie}[1]{%
\emph{#1}%
}

\newcommand{\nota}[1]{%
%\sekcjaasterysk{}
\begin{em}%
  \innotatrue
%\begin{flushleft}%
  \noindent{}\small{}#1%
  \innotafalse
%\end{flushleft}%
\end{em}%
}


\newcommand{\osoba}[1]{%
#1%
}

\newcommand{\sekcjaswiatlo}{%
\vspace{\baselineskip}%
}

\newcommand{\sekcjaasterysk}{%
\vspace{\baselineskip}%
\begin{center}%
\par{*}%
\end{center}%
}

\newcommand{\separatorlinia}{%
\vspace{10pt}%
\hrule{}%
\vspace{10pt}%
}

\newcommand{\ilustrscale}[0]{1}
\newcommand{\setilustrscale}[1]{\renewcomand{\ilustrscale}{#1}}

\newcommand{\ilustr}[3][]{
  \begin{center}%
    \ifthenelse{\isempty{#1}}%
    {\par{\includegraphics{\trimspace{#2}}\\#3}}%
    {\par{\includegraphics[#1]{\trimspace{#2}}\\#3}}%
  \end{center}%
}


\newcommand{\lista}[1]{%
\begin{compactenum}
%\setlength{\parskip}{\parindent}
#1
\end{compactenum}
}

\newcommand{\punkt}[1]{%
\item #1
}
\newcommand{\link}[2]{\href{#1}{\uline{#2}\footnote{#1}}}

\newcommand{\www}[1]{{\normalfont\href{#1}{#1}}}
