default:	forward.png backward.png

forward.png:	forward.pdf
		convert -density 150 forward.pdf forward.png

backward.png:	backward.pdf
		convert -density 150 backward.pdf backward.png

html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."