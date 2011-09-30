SHELL := /bin/bash

all:
	pdflatex -draftmode -interaction=batchmode thesis 
	bibtex -terse thesis
	pdflatex -interaction=batchmode thesis
	$(if $(grep "Rerun to get cross-references right" thesis.log), \
		pdflatex -interaction=batchmode thesis, \
		@echo "no third run necessary")
	@chflags hidden *.aux *.log
	@open -b net.sourceforge.skim-app.skim thesis.pdf
	grep -n Warning thesis.log || @echo "No warnings found! :)"

clean:
	rm -f *.aux thesis.blg thesis.log thesis.out thesis.bbl thesis.lof \
		     thesis.lot thesis.pdf thesis.toc

.PHONY: all clean

