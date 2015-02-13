NAME :=		suricata
VERSION :=	git

SURICATA_GIT :=	https://github.com/inliniac/suricata.git
LIBHTP_GIT :=	https://github.com/ironbee/libhtp

SRCDIR =	$(WORKDIR)/suricata

NO_FETCH :=	yes
NO_CLEAN :=	yes

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

fetch::
	@mkdir -p $(WORKDIR)
	@if [ -e "$(SRCDIR)" ]; then \
		echo "Updating $(SRCDIR)."; \
		cd $(SRCDIR) && git pull; \
	else \
		echo "Cloning $(SURICATA_GIT)."; \
		cd $(WORKDIR) && git clone $(SURICATA_GIT); \
	fi

	@if [ -e "$(SRCDIR)/libhtp" ]; then \
		echo "Updating $(SRCDIR)/libhtp."; \
		cd $(SRCDIR)/libhtp && git pull; \
	else \
		echo "Cloning $(LIBHTP_GIT)."; \
		cd $(SRCDIR) && git clone $(LIBHTP_GIT); \
	fi

configure: dep fetch extract
	cd $(SRCDIR) && ./autogen.sh && \
		./configure $(CONFIG_ARGS)

build: dep fetch extract configure
	cd $(SRCDIR) && make
	cd $(SRCDIR) && make install-full

clean::
	test -e $(SRCDIR)/libhtp && cd $(SRCDIR)/libhtp && git clean -xdf
	test -e $(SRCDIR) && cd $(SRCDIR) && git clean -xdf
