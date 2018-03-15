objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)
compile_cmd = ../venv/bin/pip-compile

.PHONY: all
all: $(outputs)

%.txt: %.in
	$(compile_cmd) -v --output-file $@ $<

# Dependency chain
test.txt: base.txt
dev.txt: test.txt
