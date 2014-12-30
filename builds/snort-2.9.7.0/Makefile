NAME :=		snort
VERSION :=	2.9.7.0

SOURCE :=	https://www.snort.org/downloads/snort/$(NAME)-$(VERSION).tar.gz

include ../nsmbuild.mk

DAQ_VERSION :=	2.0.4
DAQ_ROOT :=	$(INSTALL_DIR)/daq-$(DAQ_VERSION)
PATH :=		$(DAQ_ROOT)/bin:$(PATH)
export PATH

DEPS :=		daq-$(DAQ_VERSION)

build: fetch dep extract
	cd $(SRCDIR) && \
		./configure --prefix=$(PREFIX) \
			--with-daq-includes=$(DAQ_ROOT)/include \
			--with-daq-libraries=$(DAQ_ROOT)/lib \
			--enable-sourcefire \
			&& \
		make

install:
	cd $(SRCDIR) && \
		make install
