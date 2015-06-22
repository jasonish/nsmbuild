NAME :=		snort
VERSION :=	2.9.7.3

SOURCE :=	https://www.snort.org/downloads/snort/$(NAME)-$(VERSION).tar.gz

include ../nsmbuild.mk

DAQ_VERSION :=	2.0.4
DAQ_ROOT :=	$(INSTALL_DIR)/daq-$(DAQ_VERSION)
PATH :=		$(DAQ_ROOT)/bin:$(PATH)
export PATH

# Common configuration args.
CONFIG_ARGS :=	--prefix=$(PREFIX) \
		--with-daq-includes=$(DAQ_ROOT)/include \
		--with-daq-libraries=$(DAQ_ROOT)/lib \
		--enable-sourcefire

DEPS :=		daq-$(DAQ_VERSION)

# Common system deps for Fedora, CentOS.
ifneq ($(filter fedora centos,$(OS_NAME)),)
SYS_DEPS :=	libpcap-devel \
		pcre-devel
endif

# On Fedora, require luajit.
ifeq ($(OS_NAME),fedora)
SYS_DEPS +=	luajit-devel
CONFIG_ARGS +=	--enable-open-appid
endif

ifeq (+profile,$(filter +profile,$(opts)))
CONFIG_ARGS +=	--enable-profile
endif

ifeq (+appid,$(filter +appid,$(opts)))
CONFIG_ARGS +=	--enable-open-appid
endif

build: dep fetch extract
	cd $(SRCDIR) && \
		./configure $(CONFIG_ARGS) && \
		make

install:
	cd $(SRCDIR) && \
		make install
