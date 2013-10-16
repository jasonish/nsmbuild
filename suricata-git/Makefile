NAME :=		suricata
VERSION =	$(shell python $(MKPATH)/git-last-commit-date.py \
			--default git --prefix git. sources/suricata)
REV :=		1

OPTIONS =	+nfqueue \
		+profiling \
		+debug

WRKSRC =	$(WRKDIR)/$(NAME)

FETCH_TARGET =	local-fetch
EXTRACT_TARGET = local-extract

include ../mk/build.mk

DEPENDS =	jansson

ifneq ($(filter fedora redhat centos,$(DIST_NAME)),)
SYS_DEPENDS +=	pcre-devel \
		libyaml-devel \
		file-devel \
		zlib-devel \
		libpcap-devel

# For the git version...
SYS_DEPENDS +=	libtool \
		automake \
		autoconf
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
		libmagic-dev \
		autoconf \
		automake
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

  ifeq ($(call is_dist,redhat centos),yes)
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

SURICATA_GIT =	https://github.com/inliniac/suricata.git
LIBHTP_GIT =	https://github.com/ironbee/libhtp.git
LIBHTP_BRANCH =	0.5.x

local-fetch:
	@if [ ! -e sources/suricata ]; then \
		echo "Cloning $(SURICATA_GIT)..."; \
		git clone $(SURICATA_GIT) sources/suricata; \
	else \
		echo "Updating suricata..."; \
		(cd sources/suricata && git pull); \
	fi

	@if [ ! -e sources/libhtp ]; then \
		echo "Cloning $(LIBHTP_GIT) (branch $(LIBHTP_BRANCH))..."; \
		git clone https://github.com/ironbee/libhtp.git -b 0.5.x \
			sources/libhtp; \
	else \
		echo "Updating suricata/libhtp..."; \
		(cd sources/libhtp && git pull); \
		(cd sources/libhtp && git checkout $(LIBHTP_BRANCH)); \
	fi

EXTRACTED_VERSION :=	$(shell python $(MKPATH)/git-last-commit-date.py \
				--default 0 $(WRKSRC))
CURRENT_VERSION :=	$(shell python $(MKPATH)/git-last-commit-date.py \
				--default 1 sources/suricata)
local-extract: fetch
	@if [ "$(EXTRACTED_VERSION)" != "$(CURRENT_VERSION)" ]; then \
		rm -rf $(WRKDIR); \
		mkdir -p $(WRKDIR); \
		echo "Copying sources/suricata to $(WRKDIR)/suricata..."; \
		cp -a sources/suricata $(WRKDIR)/; \
		echo "Copying sources/libhtp to $(WRKDIR)/suricata/libhtp..."; \
		cp -a sources/libhtp $(WRKDIR)/suricata/; \
	fi
