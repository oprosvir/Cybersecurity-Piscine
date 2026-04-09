NAME		= stockholm
TARGETDIR	= infection
TESTDATA	= testdata
PYTHON		= python3

all:
# 	pip3 install cryptography==46.0.7 (in venv)
	sudo apt install python3-cryptography 
	chmod +x $(NAME).py
	mkdir -p $$HOME/$(TARGETDIR)
	cp -r $(TESTDATA)/* $$HOME/$(TARGETDIR)/

run: all
	$(PYTHON) $(NAME).py --help

clean:
	rm -rf $$HOME/${TARGETDIR}

.PHONY: all run clean