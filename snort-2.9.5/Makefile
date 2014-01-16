NAME :=		snort
VERSION :=	2.9.5
REV :=		1

SOURCE :=	http://www.snort.org/dl/snort-current/$(NAME)-$(VERSION).tar.gz

define configure
cd $(WRKSRC); \
	PATH=$(PATH):$(DAQ_ROOT)/bin ./configure --prefix=$(PREFIX) \
		--with-daq-includes=$(DAQ_ROOT)/include \
		--with-daq-libraries=$(DAQ_ROOT)/lib
endef

define build
cd $(WRKSRC); \
	make; \
	make install DESTDIR=$(WRKINST)
endef

include ../mk/build.mk

DEPENDS +=	daq

ifeq ($(call is_dist,fedora el),yes)
SYS_DEPENDS +=	libdnet-devel \
		pcre-devel \
		zlib-devel
endif

DAQ_VERSION := 2.0.0
DAQ_ROOT := $(PACKAGEROOT)/daq/$(DAQ_VERSION)

# On CentOS, RedHat we need to tell how to link against
# libnetfilter_queue.
ifneq ($(filter el,$(DIST_NAME)),)
LDFLAGS += -L$(PACKAGEROOT)/libnetfilter_queue/1.0.0/lib
endif
