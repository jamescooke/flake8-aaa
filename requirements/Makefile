objects = $(wildcard *.in)
outputs := $(objects:.in=.txt)

.PHONY: all
all: $(outputs)

%.txt: %.in
	pip-compile --verbose --output-file $@ $<

# Temporary helper: remove when py36 goes
examples-py36.txt: examples.in
	pip-compile examples.in --output-file examples-py36.txt
test-py36.txt: test.in
	pip-compile test.in --output-file test-py36.txt

# Dependency chain
test.txt: base.txt
dev.txt: test.txt
