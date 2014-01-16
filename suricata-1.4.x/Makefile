NAME :=		suricata
VERSION :=	1.4.7
REV :=		1

SOURCE :=	http://www.openinfosecfoundation.org/download/$(NAME)-$(VERSION).tar.gz

OPTIONS =	+nfqueue \
		+profiling \
		+debug

include ../mk/build.mk

DEPENDS =	jansson

# Fedora, CentOS/RedHat (w/EPEL) dependencies.
ifneq ($(filter fedora el,$(DIST_NAME)),)
SYS_DEPENDS +=	pcre-devel \
		libyaml-devel \
		file-devel \
		zlib-devel \
		libpcap-devel \
		python-simplejson
endif

# Ubuntu dependencies.
ifeq ($(DIST_NAME),ubuntu)
SYS_DEPENDS +=	libpcre3 \
		libpcre3-dev \
		build-essential \
		libtool \
		libpcap-dev \
		libnet1-dev \
		libyaml-0-2 \
		libyaml-dev \
		zlib1g \
		zlib1g-dev \
		libcap-ng-dev \
		libcap-ng0 \
		libmagic-dev
endif

CONFIGURE_ARGS += --prefix=$(PREFIX)

# Enable luajit.
# - So far not working on Mac.
ifeq ($(filter Darwin,$(UNAME_SYSTEM)),)
DEPENDS += luajit
LUAJIT_VERSION = 2.0.2
LUAJIT_ROOT = $(PACKAGEROOT)/luajit/$(LUAJIT_VERSION)
LUAJIT_INC = $(LUAJIT_ROOT)/include/luajit-2.0
LUAJIT_LIB = $(LUAJIT_ROOT)/lib
CONFIGURE_ARGS += --enable-luajit \
	--with-libluajit-includes=$(LUAJIT_INC) \
	--with-libluajit-libraries=$(LUAJIT_LIB)
LDFLAGS += -Wl,-rpath -Wl,$(LUAJIT_LIB)
endif

# Jansson
JANSSON_VERSION = 2.4
JANSSON_ROOT = $(PACKAGEROOT)/jansson/$(JANSSON_VERSION)
JANSSON_INC = $(JANSSON_ROOT)/include
JANSSON_LIB = $(JANSSON_ROOT)/lib
CONFIGURE_ARGS += --with-libjansson-includes=$(JANSSON_INC) \
	--with-libjansson-libraries=$(JANSSON_LIB)

# Linux specific settings.
ifeq ($(UNAME_SYSTEM),Linux)
CONFIGURE_ARGS += --enable-af-packet
LDFLAGS += -Wl,-rpath -Wl,$(PREFIX)/lib
endif

# +nfqueue
ifeq ($(call has_opt,+nfqueue),yes)

  CONFIGURE_ARGS+=--enable-nfqueue

  ifeq ($(call is_dist,el),yes)
    DEPENDS += libnetfilter_queue
    CONFIGURE_ARGS+=--with-libnetfilter_queue-includes=$(PACKAGEROOT)/libnetfilter_queue/1.0.0/include
    CONFIGURE_ARGS+=--with-libnetfilter_queue-libraries=$(PACKAGEROOT)/libnetfilter_queue/1.0.0/lib
  endif

  ifeq ($(call is_dist,fedora),yes)
    SYS_DEPENDS += libnfnetlink-devel
  endif

endif

# +profiling
ifeq ($(call has_opt,+profiling),yes)
CONFIGURE_ARGS += --enable-profiling
endif

# +debug
ifeq ($(call has_opt,+profiling),yes)
CONFIGURE_ARGS += --enable-debug
endif
