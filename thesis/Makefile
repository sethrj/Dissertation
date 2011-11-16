SHELL := /bin/bash

all:
	pdflatex -draftmode -interaction=batchmode thesis 
	bibtex -terse thesis
	pdflatex -synctex=1 -interaction=batchmode thesis
	$(if -n $(grep "Rerun to get cross-references right" thesis.log), \
		pdflatex -synctex=1 -interaction=batchmode thesis, \
		@echo "No third run necessary")
	@chflags hidden *.aux *.log
	@open -b net.sourceforge.skim-app.skim thesis.pdf
	grep -n Warning thesis.log || echo "No warnings found! Yay!"

clean:
	rm -f *.aux thesis.blg thesis.log thesis.out thesis.bbl thesis.lof \
		     thesis.lot thesis.pdf thesis.toc

finalAbstract.pdf: finalAbstract.tex
	pdflatex -synctex=1 -interaction=batchmode finalAbstract

individual:
	cd _individual && ./make.sh

.PHONY: all clean individual

