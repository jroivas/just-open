VERSION=2021.11.1
DESTDIR:=$(HOME)

all:
	@echo "Please run: make install"

install:
	mkdir -p "$(DESTDIR)/bin"
	cp just-open.py "$(DESTDIR)/bin"
	ln -sf "$(DESTDIR)/bin/just-open.py" "$(DESTDIR)/bin/just-open"
	ln -sf "$(DESTDIR)/bin/just-open.py" "$(DESTDIR)/bin/jo"

dist:
	mkdir -p "just-open-$(VERSION)"
	cp just-open.py "just-open-$(VERSION)"
	cp just-open.sample.json "just-open-$(VERSION)"
	cp README.md "just-open-$(VERSION)"
	tar czvf "just-open-$(VERSION).tar.gz" "just-open-$(VERSION)"
	rm -rf "just-open-$(VERSION)"

test:
	python -m doctest just-open.py
	flake8 just-open.py
