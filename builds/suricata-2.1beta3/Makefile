NAME :=		suricata
VERSION :=	2.1beta3

SOURCE :=	http://www.openinfosecfoundation.org/download/$(NAME)-$(VERSION).tar.gz

OPTIONS :=	+profiling
ifeq ($(OS_NAME),fedora)
OPTIONS +=	+lua
endif

include ../nsmbuild.mk

CONFIG_ARGS :=	--prefix=$(PREFIX)

# Common system deps for Fedora, CentOS.
ifneq ($(filter fedora centos,$(OS_NAME)),)
SYS_DEPS :=	libyaml-devel \
		libpcap-devel \
		jansson-devel \
		file-devel \
		curl
endif

ifeq ($(filter $(opts),+lua),+lua)
ifeq ($(OS_NAME),fedora)
SYS_DEPS +=	luajit-devel
CONFIG_ARGS +=	--enable-luajit
endif
endif

configure: dep fetch extract
	if [ ! -e $(WORKDIR)/configure_done ]; then \
		cd $(SRCDIR) && ./configure $(CONFIG_ARGS); \
		touch $(WORKDIR)/configure_done; \
	fi

build: dep fetch extract configure
	cd $(SRCDIR) && make
	cd $(SRCDIR) && make install-full
