%  Template for research notes
%  by Seth R. Johnson
% licensed under Creative Commons (attribution): http://creativecommons.org/licenses/by/3.0/us/ 
%
% Usage: \documentclass{SRJresearch}
% define \title and \author as usual, and also define \classname

\NeedsTeXFormat{LaTeX2e}[1995/12/01]
\ProvidesClass{SRJresearch}
[2008/09/02 v1.00 Report template class, Seth R. Johnson]

%%% OPTIONS %%%
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions

%%% REQUIRED CLASSES %%%
\RequirePackage{fix2col}
\LoadClass[letterpaper]{article}

\RequirePackage{geometry}
\RequirePackage{fourier}
% revert calligraphy math:
%Test $ \mathcal{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$
\SetMathAlphabet{\mathcal}{normal}{OMS}{xmdcmsy}{m}{n}%

\RequirePackage{microtype}
\RequirePackage{bm}
\RequirePackage{amsmath}
\RequirePackage[pdftex]{graphicx}
\RequirePackage[unicode,pdftex]{hyperref}
\RequirePackage{subfig}
\RequirePackage{fancyhdr}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\geometry{letterpaper,top=0.75in,left=0.75in,headheight=14pt}

\input{SRJinclude}
\newcommand{\units}[1]{\:\text{#1}}%

\AtBeginDocument{%
 \hypersetup{pdfauthor={\@author}, pdftitle={\@title}, pdfsubject={Research notes}}

 % need to use if \maketitle is used (which destroys \@title etc.)
 \let\@preservedTitle=\@title
 \let\@preservedDate=\today
 \let\@preservedAuthor=\@author

 %\let\and\@oldand


  \pagestyle{fancy}%
  \rhead{\@preservedTitle}%
  \lhead{\@preservedAuthor}%
  \lfoot{\@preservedDate}%
  \cfoot{}%
  \rfoot{\thepage}%
  \renewcommand{\headrulewidth}{0.4pt}%
  \renewcommand{\footrulewidth}{0.4pt}%

 % table of contents style
 \fancypagestyle{plain}{%
   \fancyhead{} % clear all header fields 
%   \fancyhead[CE,CO]{\fhFormat \@preservedTitle} %
   \fancyfoot{} % clear all footer fields 
   \cfoot{\thepage}%
   \renewcommand{\headrulewidth}{0.0pt}%
   \renewcommand{\footrulewidth}{0.4pt}%
 }

  % let ``align'' break anywhere
  \allowdisplaybreaks

 \maketitle
}

%%%%%%  VISUAL STUFF %%%%%%


% allow more floats
\renewcommand{\bottomfraction}{0.5}
%\renewcommand\floatpagefraction{.9}
%\renewcommand\topfraction{.9}
%\renewcommand\bottomfraction{.9}
%\renewcommand\textfraction{.1} 

%margin notes
\let\xxoldmarginpar\marginpar
\renewcommand\marginpar[1]{\xxoldmarginpar[\raggedleft\footnotesize #1]%
{\raggedright\footnotesize\sffamily #1}}
