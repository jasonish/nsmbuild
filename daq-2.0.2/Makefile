NAME :=		daq
VERSION :=	2.0.2
REV :=		1

SOURCE :=	http://www.snort.org/dl/snort-current/$(NAME)-$(VERSION).tar.gz

define configure
cd $(WRKSRC); \
	./configure --prefix=$(PREFIX) --enable-static --disable-shared
endef

define build
cd $(WRKSRC); \
	make; \
	make install DESTDIR=$(WRKINST)
endef

include ../mk/build.mk

# Fedora, CentOS and RedHat share some common dependencies.
ifneq ($(filter fedora el,$(DIST_NAME)),)
SYS_DEPENDS =	flex \
		bison \
		libpcap-devel \
		libdnet-devel
endif

# Fedora has libnetfilter_queue-devel, so require it.
ifeq ($(DIST_NAME),fedora)
SYS_DEPENDS +=	libnetfilter_queue-devel
endif

# We provide libnetfilter_queue for CentOS/RedHat.
ifneq ($(filter el,$(DIST_NAME)),)
DEPENDS +=	libnetfilter_queue
CPPFLAGS +=	-I$(PACKAGEROOT)/libnetfilter_queue/1.0.0/include
LDFLAGS +=	-L$(PACKAGEROOT)/libnetfilter_queue/1.0.0/lib
endif
