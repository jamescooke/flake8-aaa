objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)
compile_cmd = ../venv/bin/pip-compile
compile_cmd2 = ../venv2/bin/pip-compile

.PHONY: all
all: $(outputs)

%.txt: %.in
	$(compile_cmd) -v --output-file $@ $<

# Dependency chain
test.txt: base.txt
dev.txt: test.txt

# Special command for python 2 requirements
test2.txt: base.txt test.in
	$(compile_cmd2) -v --output-file test2.txt test.in
