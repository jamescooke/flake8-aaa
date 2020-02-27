objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

.PHONY: all
all: $(outputs)

%.txt: %.in
	pip-compile --verbose --output-file $@ $<

# Dependency chain
test.txt: base.txt
dev.txt: test.txt
