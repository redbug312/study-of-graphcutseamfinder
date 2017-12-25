.PHONY: start debug test

MAIN = ./main.py

start:
	$(MAIN) duck.jpg

debug:
	ipdb3 $(MAIN) duck.jpg --cut

test:
	$(MAIN) duck.jpg --cut

