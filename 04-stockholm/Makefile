NAME		:= stockholm
TARGETDIR	:= infection
TESTDATA	:= testdata
PYTHON		:= python3
VENV		:= $(shell echo $$VIRTUAL_ENV)

all:
ifdef VENV
	@echo "Virtual environment detected: installing via pip"
	pip3 install cryptography==41.0.7
	pip3 install argon2-cffi==21.1.0
else
	@echo "No virtual environment: installing system packages"
	sudo apt install python3-cryptography
	sudo apt install python3-argon2
endif
	chmod +x $(NAME).py
	mkdir -p $$HOME/$(TARGETDIR)
	cp -r $(TESTDATA)/* $$HOME/$(TARGETDIR)/

run: all
	$(PYTHON) $(NAME).py --help

clean:
	rm -rf $$HOME/${TARGETDIR}

.PHONY: all run clean