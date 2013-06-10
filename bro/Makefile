NAME :=		bro
VERSION :=	2.1
REV :=		1

SOURCE :=	http://www.bro.org/downloads/release/$(NAME)-$(VERSION).tar.gz

define configure
cd $(WRKSRC); \
	./configure --prefix=$(PREFIX)
endef

define build
cd $(WRKSRC); \
	make; \
	make install DESTDIR=$(WRKINST)
endef

include ../mk/build.mk


