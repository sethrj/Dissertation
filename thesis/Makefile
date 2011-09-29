all:
	pdflatex thesis
	bibtex thesis
	pdflatex thesis
	pdflatex finalAbstract
	chflags hidden *.aux *.log
	open -b net.sourceforge.skim-app.skim thesis.pdf
	grep -n Warning thesis.log

clean:
	rm *.aux thesis.blg thesis.log thesis.out thesis.bbl thesis.lof \
		     thesis.lot thesis.pdf thesis.toc

.PHONY: all clean

