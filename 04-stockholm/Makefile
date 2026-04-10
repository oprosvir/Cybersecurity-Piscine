NAME		= stockholm
TARGETDIR	= infection
TESTDATA	= testdata
PYTHON		= python3

all:
	pip3 install cryptography
	pip3 install argon2-cffi
	chmod +x $(NAME).py
	mkdir -p $$HOME/$(TARGETDIR)
	cp -r $(TESTDATA)/* $$HOME/$(TARGETDIR)/

run: all
	$(PYTHON) $(NAME).py --help

clean:
	rm -rf $$HOME/${TARGETDIR}

.PHONY: all run clean