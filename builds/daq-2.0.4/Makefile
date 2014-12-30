NAME :=		daq
VERSION :=	2.0.4

SOURCE :=	https://www.snort.org/downloads/snort/$(NAME)-$(VERSION).tar.gz

include ../nsmbuild.mk

build: fetch dep extract
	cd $(SRCDIR) && \
		./configure --prefix=$(PREFIX) && \
		make

install: build
	cd $(SRCDIR) && \
		make install
