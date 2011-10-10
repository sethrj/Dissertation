SHELL := /bin/bash
TEXFILES = adDerivation aponeDerivation conclusion flatland implementation \
	introduction simpleNumericalResults trtBackground trtNumericalResults

all:
	for f in ${TEXFILES}; do \
		echo "Compiling $$f"; \
		pdflatex -draftmode -interaction=batchmode $$f; \
		bibtex -terse $$f; \
		pdflatex -interaction=batchmode $$f; \
		$(if -n $(grep "Rerun to get cross-references right" $$f.log), \
			pdflatex -interaction=batchmode $$f, \
			@echo "No third run necessary"); \
	done
	@chflags hidden *.aux *.log
	grep -in Warning *.log || echo "No warnings found!"

.PHONY: all

