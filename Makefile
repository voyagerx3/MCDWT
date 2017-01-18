default:	forward.png backward.png

forward.png:	forward.pdf
		convert -density 150 forward.pdf forward.png

backward.png:	backward.pdf
		convert -density 150 backward.pdf backward.png
