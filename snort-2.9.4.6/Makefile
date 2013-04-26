NAME :=		snort
VERSION :=	2.9.4.6
REV :=		1

SOURCE :=	http://www.snort.org/downloads/2320
SOURCE_FILE :=	$(NAME)-$(VERSION).tar.gz

DEPENDS :=	daq

export DAQ_VERSION = 2.0.0

CPPFLAGS +=	-I$(PACKAGEROOT)/daq/$(DAQ_VERSION)/include

# System dependendencies:
# libdnet-devel

include ../mk/build.mk
