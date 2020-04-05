#
# Use this Makefile as an example.
#
# It also builds the project for disctibution. This way, you can visualize how
# the project is built and distributed.
#

.PHONY: default
default:
	@echo 'This is just a dummy (but working) Makefile.'
	@echo 'It could be used as an input file for the makefile2dot visualizer'
	@echo 'Type "make all" to generate example output.png' 

VERSION := 0.1.0
LIB_FILES := makefile2dot/__init__.py

.PHONY: all
all: output.png

output.png: output.dot
	dot -Tpng < $< > $@

output.dot: Makefile $(LIB_FILES) .linted .checked
	scripts/makefile2dot < $< >$@

# Becomes invalidated if lint has to be re-run.
.linted: $(LIB_FILES) scripts/makefile2dot
	pycodestyle $(LIB_FILES) && touch .linted

# Becomes invalidated if tests have to be re-run.
.checked: $(LIB_FILES) makefile2dot/test_makefile2dot.py
	pytest && touch .checked

.PHONY: dist
dist: dist/makefile2dot-$(VERSION)-py3-none-any.whl

dist/makefile2dot-$(VERSION)-py3-none-any.whl: Makefile scripts/makefile2dot $(LIB_FILES) .linted .checked setup.py
	python -m setup bdist_wheel

dist/makefile2dot-$(VERSION).tar.gz: Makefile scripts/makefile2dot $(LIB_FILES) .linted .checked setup.py
	python -m setup sdist

.twine_checked: dist/makefile2dot-$(VERSION)-py3-none-any.whl dist/makefile2dot-$(VERSION).tar.gz
	twine check dist/* && touch .twine_checked

.PHONY: upload
upload: .twine_checked
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: clean
clean:
	rm -f $(ALL)
