objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

.PHONY: all
all: $(outputs)

%.txt: %.in
	pip-compile --verbose --output-file $@ $<

# Dependency chain
dev.txt: ci.txt
