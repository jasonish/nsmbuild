NAME :=		suricata
VERSION :=	1.3.6
REV :=		1

SOURCE :=	http://www.openinfosecfoundation.org/download/$(NAME)-$(VERSION).tar.gz

OPTIONS :=	+nfqueue \
		+profiling \
		+debug

include ../mk/build.mk

ifeq ($(call is_dist,centos redhat fedora),yes)
SYS_DEPENDS +=	pcre-devel \
		libyaml-devel \
		file-devel \
		zlib-devel
endif

CONFIGURE_ARGS += --prefix=$(PREFIX)

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
