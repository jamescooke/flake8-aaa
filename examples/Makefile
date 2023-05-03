.PHONY: all
all: black/noqa

black/noqa: black
	mkdir black/noqa
	cp good/noqa/*.py black/noqa/

black:
	mkdir black
	cp good/*.py black/

.PHONY: clean
clean:
	rm -rf black
