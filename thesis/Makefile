all:
	pdflatex thesis
	bibtex thesis
	pdflatex thesis
	chflags hidden *.aux
	open -b net.sourceforge.skim-app.skim thesis.pdf

clean:
	rm *.aux thesis.blg thesis.log thesis.out thesis.bbl thesis.lof \
		     thesis.lot thesis.pdf thesis.toc

.PHONY: all clean

