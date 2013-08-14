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

%\RequirePackage{geometry}
\RequirePackage{setspace}
\RequirePackage{type1cm}
\RequirePackage{amssymb}
\RequirePackage{amsmath}

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
\newif\ifafivepaper \afivepaperfalse
\DeclareOption{a5paperdd}{%
  \setlength{\paperheight}{225mm}%
  \setlength{\paperwidth}{160mm}%
  \afivepapertrue
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

\ifafivepaper
  \usepackage[%
    paperwidth=160mm,%
    paperheight=225mm,%
    text={117mm,162mm},% 
    top=30mm,% 
    headsep=8mm,%
    left=23mm,%
    right=30mm]{geometry}%
\fi

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

\usepackage[overload]{textcase}
\usepackage{scalefnt}
\usepackage[colorlinks=true,linkcolor=black,setpagesize=false,urlcolor=black,xetex]{hyperref}


\setmainfont [
ItalicFont = CrimsonText-Italic,
BoldFont = CrimsonText-Bold,
BoldItalicFont = CrimsonText-BoldItalic,
Ligatures={Common, Contextual},
Mapping=tex-text
]{CrimsonText-Roman}
\newfontface\sb{CrimsonText-Semibold}

\renewcommand{\baselinestretch}{1.1}

\pagestyle{plain}
\usepackage{fancyhdr}
\usepackage[explicit]{titlesec}

\makeatletter



% bottom figure below footnotes
\usepackage{fnpos}
\makeFNabove

\usepackage{color}
\definecolor{theme}{gray}{.3}


%%%%%%%%%%%%%%%%%%%%%% Headings.

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

%\lfoot{{\footnotesize \textsc{\@author} \emph{\@title}}}
\cfoot{}
%\rfoot{{\footnotesize \thepage}}
\renewcommand{\chaptermark}[1]{\markboth{\MakeUppercase{#1}}{}}
\fancyhead[CE]{{\textsc{\MakeUppercase{\@title}}}}
\fancyhead[CO]{{\textsc{\leftmark}}}
\fancyhead[LE,RO]{{\thepage}}

%%%%%%%%%%%%%%%%%%%%%% Section title styles.
%% Sections
\titleformat{\chapter}%
{\raggedright\Huge\sc\addfontfeature{LetterSpace=0.0, Letters={Uppercase}}}%
{}{0pt}{\MakeUppercase{#1}}
\titlespacing*{\chapter}{0pt}{0pt}{40pt}

%% Subsections
\titleformat{\section}%
{\bf\large\addfontfeature{Scale=1.0}}%
{\thesection\enskip}{0pt}{#1}
\renewcommand{\thesection}{\Roman{section}}

\titleformat{\subsection}%
{\sc}%
{\thesubsection}{0pt}{#1}

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

%%%%% Footnotes %%%%%%%%5
%% \makeatletter
%% \renewcommand\@makefntext[1]{%
%%   \noindent\parbox[t][\height][l]{3em}{\@thefnmark.}\parbox[t][\height][l]{6cm}{#1}\vskip3pt}
%% \makeatother
\makeatletter

\renewcommand\@makefnmark{%
\hbox{{\normalfont\@thefnmark}}%
}
\renewcommand\thefootnote{[\arabic{footnote}]}

\long\def\@makefntext#1{%
  \parindent 1em\noindent \hb@xt@ 1.8em{\hss \@makefnmark \enskip}#1.
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

 
%% Strona tytułowa %% XXX
       \hspace{-36mm}\parbox{16cm}{
        {\addfontfeature{LetterSpace=-4.0}{\scalefont{4}%
            \noindent Philippe Aigrain}}

       {\addfontfeature{LetterSpace=-4.0}{\scalefont{2.5}%
            przy współpracy Suzanne Aigrain
        }}

        \vspace{2em}
        {\addfontfeature{LetterSpace=-4.0}{\scalefont{6}%
            Dzielenie się
        }}
        
        \vspace{2em}
        {\addfontfeature{LetterSpace=-4.0}{\scalefont{3}%
            Kultura i gospodarka epoki internetu
        }}
        }

       \setlength{\pdfpagewidth}{210mm}
       \setlength{\pdfpageheight}{297mm}
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

\usepackage{printlen}

\newcommand{\editorialsection}{
%% XXX % sprawdzic czy czegos nie zgubilem z master
%% szczegolnie jesli chodzi o makra wstawiajace dane z DC, jak np \editors
%% coś tu nie dizała, do zmiany ogólnie

%% \clearpage
%%         \thispagestyle{empty}

%% % Pusta strona 
%% \clearpage
%%         \thispagestyle{empty}

%% \vspace{2em}
%%       \hspace{0mm}\parbox{16cm}{
%% \centering
%%       {\addfontfeature{LetterSpace=-4.0}{\scalefont{6}%
%%            Dzielenie się
%%       }}

%%   \vspace{2em}
%%          {\addfontfeature{LetterSpace=-4.0}{\scalefont{3}%
%%              Kultura i gospodarka epoki internetu
%%          }}
%% }

%% \clearpage
%%         \thispagestyle{empty}

%% \clearpage
%%         \thispagestyle{empty}

%% %\parbox{10cm}{
%% %  \centering

%%   \hspace{-36mm}\parbox{16cm}{
%% \centering

%%   {\addfontfeature{LetterSpace=-4.0}{\scalefont{4}%
%%       \noindent Philippe Aigrain
%%   }}

%%   {\addfontfeature{LetterSpace=-4.0}{\scalefont{2.5}%
%%       przy współpracy Suzanne Aigrain
%%   }}
  
%%   \vspace{2em}
%%          {\addfontfeature{LetterSpace=-4.0}{\scalefont{6}%
%%              Dzielenie się
%%          }}
         
%%   \vspace{2em}
%%          {\addfontfeature{LetterSpace=-4.0}{\scalefont{4}%
%%              Kultura i gospodarka epoki internetu
%%          }}

%%   \vspace{2em}
%%          {\addfontfeature{LetterSpace=-4.0}{\scalefont{2}%
%%              Z języka angielskiego przełożył \\
%%              \emph{Wojciech Pędzich}
%%          }}

%% \vspace{22em}

%% \includegraphics[scale=.2]{logo.eps}
%% }

%%     Przekaż darowiznę na konto:
%%     \href{http://nowoczesnapolska.org.pl/pomoz-nam/wesprzyj-nas/}{szczegóły na stronie Fundacji}.

%% \clearpage
%%         \thispagestyle{empty}

%% \noindent Tytuł oryginału

%% \noindent \emph{Sharing. Culture and the Economy in the Internet Age}

%% \vspace{1em}

%% \noindent \editors

%% \vspace{1em}


%% \noindent \rightsinfo

%% \vspace{1em}

%% \noindent \coverby


%% %\set\textwidth=450pt
%% %\printlength\textwidth


%% %% {\scalefont{1.5}Drogi czytelniku!}



%% %% \vspace{1em}

%% \vspace{1em}

%% \noindent Tłumaczenie książki powstało w ramach projektu "Przyszłość prawa autorskiego" finansowanego przez {\it Trust for Civil Society in Central and Eastern Europe}.

%% \vspace{1em}

%% \noindent \includegraphics[scale=.4]{cce_trust.eps}

%% \vspace{1em}

%% \noindent Wydawca: Fundacja Nowoczesna Polska, Warszawa 2012

%% \vspace{1em}
%% \includegraphics[scale=.2]{logo.eps}
%% \vspace{1em}

%% \noindent \href{http://nowoczesnapolska.org.pl/}{http://nowoczesnapolska.org.pl/}



%% %\vspace{4em}
%% %\box{\tableofcontents}

%% %%   \begin{figure}[b!]
%% %%   {
%% %%     \footnotesize
%% %%     \color{theme}
%% %%     \noindent \rule{\linewidth}{0.4pt}

%% %%     \rightsinfo
%% %% %    \vspace{.6em}

%% %%     %Źródło: \href{\bookurl}{\bookurl}

%% %%     %\vspace{.6em}
%% %%     %\sourceinfo

%% %%     %\description
%% %%     %\vspace{.6em}

%% %%     Opublikowano przez \href{http://nowoczesnapolska.org.pl}{Fundację Nowoczesna Polska}, 2012.

%% %%     \editors

%% %%     %\vspace{.6em}
%% %%     \coverby
    
%% %%     \color{black}
%% %%   }
%% %%   \end{figure}
%% \clearpage
%% }
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
\part{#1}%
}
\newcommand{\srodtytul}[1]{%
\subsection*{\typosubsection{#1}}%
}

\newcommand{\naglowekscena}[1]{%
\subsubsection*{\typosubsubsection{#1}}%
}
\newcommand{\naglowekrozdzial}[1]{%
\chapter{#1}%
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

