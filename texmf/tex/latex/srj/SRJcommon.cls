%  Common classes and definitions for SRJhomework etc.
%  by Seth R. Johnson
% licensed under Creative Commons (attribution): http://creativecommons.org/licenses/by/3.0/us/ 

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{SRJcommon}
[2008/09/02 v1.00 Common classes and definitions, Seth R. Johnson]

%%% OPTIONS %%%

\newif\ifusesubfig
\usesubfigfalse

\newif\if@usetinyunits
\@usetinyunitsfalse

\newif\ifusefancyvrb
\usefancyvrbfalse

\newif\ifusecolor
\usecolorfalse

\DeclareOption{tinyunits}{%
	\@usetinyunitstrue
	\usecolortrue}
\DeclareOption{fancyvrb}{%
	\usefancyvrbtrue}
\DeclareOption{subfig}{%
	\usesubfigtrue}
\DeclareOption{color}{%
	\usecolortrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions

%%% REQUIRED CLASSES %%%
\LoadClass{article}
\RequirePackage{geometry}
\RequirePackage{fancyhdr}

\RequirePackage{amsmath}
\RequirePackage{amssymb}
\RequirePackage{amsthm}
\RequirePackage{bm}      %bold math symbols for vectors
\RequirePackage[pdftex]{graphicx}
\RequirePackage{caption}

\captionsetup{width=.75\textwidth,font=small,labelfont=bf}
%\captionsetup{width=.75\textwidth,font=small,format=hang}

%%% CLASS NAME AND TITLES %%%
\def\@classname{\PackageWarning{SRJcommon}{No `classname' given.}}
\newcommand{\classname}[1]{\def\@classname{#1}}

%%% MISC PACKAGE DEFS
% colors
\ifusecolor
  \RequirePackage{color}
  \definecolor{halfgray}{gray}{0.5}
  \definecolor{lightblue}{rgb}{0.4,0.4,0.80} 
  \definecolor{red}{rgb}{1,0,0} 
\fi

% set up subfigures
\ifusesubfig
	%\typeout{Using subfig}
	\RequirePackage{subfig}%
%
	\renewcommand{\thesubfigure}{\alph{subfig}}%
	\renewcommand{\@thesubfigure}{{\subcaplabelfont(\thesubfigure)}\space}%
\fi

%set up fancyvrb
\ifusefancyvrb
	\usepackage{fancyvrb}%
%
	\newcommand{\VerbCode}[2]{\fvset{frame=single,%
		fontsize=\small,%
		xleftmargin=0.5in,%
		xrightmargin=0.5in,%
		label={#1},%
		labelposition=topline%
	}%
	\VerbatimInput{#2}%
	}%
\fi

% REQUIRED CLASSES (load hyperref last because of dependencies)
\RequirePackage[unicode,pdftex]{hyperref}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%        COMMAND SHORTCUTS        %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\input{SRJinclude}

%Units: first is the tiny blue offset label, second is the more formal way
\if@usetinyunits%
	\newcommand{\units}[1]{\raisebox{0.3ex}{\color{lightblue}\tiny{[{#1}]}}}%
	\newcommand{\ohms}{\units{ohm}}%
\else%
	\newcommand{\units}[1]{\:\text{#1}}%
%	\newcommand{\ohms}{\ensuremath{\Omega}}%
	\newcommand{\ohms}{\units{$\Omega$}}%
\fi

\theoremstyle{definition} \newtheorem{defn}{Definition}
\theoremstyle{definition} \newtheorem{fact}{Fact}
\theoremstyle{definition} \newtheorem{example}{Example}

