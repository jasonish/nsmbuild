NAME :=		snort
VERSION :=	2.9.6.2

SOURCE :=	http://downloads.sourceforge.net/project/snort.mirror/Snort%202.9.6.2/snort-2.9.6.2.tar.gz

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
