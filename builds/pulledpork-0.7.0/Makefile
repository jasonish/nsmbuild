NAME :=		pulledpork
VERSION :=	0.7.0

SOURCE :=	https://$(NAME).googlecode.com/files/$(NAME)-$(VERSION).tar.gz

include ../nsmbuild.mk

ifeq ($(filter $(OS_NAME),fedora),fedora)
SYS_DEPS :=	perl-libwww-perl \
		perl-Crypt-SSLeay \
		perl-Archive-Tar \
		perl-Sys-Syslog \
		perl-Switch \
		perl-LWP-Protocol-https
endif

build: dep fetch extract

	install -D -d -m 755 $(PREFIX)/bin
	install -m 755 $(SRCDIR)/pulledpork.pl ${PREFIX}/bin/

	install -D -d -m 755 $(PREFIX)/share/pulledpork
	cp -a $(SRCDIR)/doc $(PREFIX)/share/pulledpork/
	cp -a $(SRCDIR)/etc $(PREFIX)/share/pulledpork/
	cp -a $(SRCDIR)/contrib $(PREFIX)/share/pulledpork/
