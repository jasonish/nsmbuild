NAME :=		suricata
VERSION :=	2.0.7

SOURCE :=	http://www.openinfosecfoundation.org/download/$(NAME)-$(VERSION).tar.gz

include ../nsmbuild.mk

CONFIG_ARGS :=	--prefix=$(PREFIX)

# Common system deps for Fedora, CentOS.
ifneq ($(filter fedora centos,$(OS_NAME)),)
SYS_DEPS :=	libyaml-devel \
		libpcap-devel \
		jansson-devel \
		file-devel \
		pcre-devel \
		curl \
		zlib-devel \
		nss-devel \
		nspr-devel \
		libnfnetlink-devel \
		libnetfilter_queue-devel
CONFIG_ARGS +=	--enable-nfqueue
endif

configure: dep fetch extract
	if [ ! -e $(WORKDIR)/configure_done ]; then \
		cd $(SRCDIR) && ./configure $(CONFIG_ARGS); \
		touch $(WORKDIR)/configure_done; \
	fi

build: dep fetch extract configure
	cd $(SRCDIR) && make
	cd $(SRCDIR) && make install-full
