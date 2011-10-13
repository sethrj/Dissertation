#!/bin/bash

TEXFILES="adDerivation aponeDerivation conclusion flatland implementation introduction simpleNumericalResults trtBackground trtNumericalResults"

for f in ${TEXFILES}; do
	echo "Compiling $f"
	#	pdflatex -draftmode -interaction=batchmode $f
	#	bibtex -terse $f
	#	pdflatex -interaction=batchmode $f
	if [ -n $(grep "Rerun to get cross-references right" $f.log) ]; then
		pdflatex -interaction=batchmode $f
		echo "No third run necessary"
	fi
done
chflags hidden *.aux *.blg *.bbl
grep -in Warning *.log || echo "No warnings found!"

