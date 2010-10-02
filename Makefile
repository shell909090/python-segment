#!/usr/bin/make -f

all: build-deb

build-deb: build
	dpkg-buildpackage -rfakeroot

build:

clean:
	rm -rf build
	rm -f python-build-stamp*
	rm -rf debian/python-segment
	rm -f debian/python-segment*
	rm -rf debian/python-module-stampdir

test:
	python test.py
