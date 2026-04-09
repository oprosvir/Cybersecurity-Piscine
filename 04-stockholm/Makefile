NAME		= stockholm
TARGETDIR	= infection
PYTHON		= python3

all:
	@if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi
	chmod +x $(NAME).py
	mkdir -p $$HOME/$(TARGETDIR)

run: all
	$(PYTHON) $(NAME).py --help

clean:
	rm -r $$HOME/${TARGETDIR}

.PHONY: all run clean