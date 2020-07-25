.PHONY: all
all: good/black/noqa

good/black/noqa: good/black
	mkdir good/black/noqa
	cp good/noqa/*.py good/black/noqa/

good/black:
	mkdir good/black
	cp good/*.py good/black/

.PHONY: clean
clean:
	rm -rf good/black
