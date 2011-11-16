#!/bin/bash

TEXFILES="adDerivation aponeDerivation conclusion flatland implementation introduction simpleNumericalResults trtBackground trtNumericalResults"

for f in ${TEXFILES}; do
	echo "Compiling $f"
	pdflatex -draftmode -interaction=batchmode $f
	bibtex -terse $f
	pdflatex -synctex=1 -interaction=batchmode $f
	grep 'Rerun to get cross-references right' $f.log
	if [ $? -eq 0 ]; then
		pdflatex -synctex=1 -interaction=batchmode $f
	fi
done
chflags hidden *.aux *.blg *.bbl
grep -in Warning *.log || echo "No warnings found!"

