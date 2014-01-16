NAME :=		snort
VERSION :=	2.9.3.1
REV :=		1

SOURCE :=	http://www.snort.org/downloads/1862
SOURCE_FILE :=	$(NAME)-$(VERSION).tar.gz

include ../mk/build.mk

ifeq ($(call is_dist,fedora el),yes)
SYS_DEPENDS +=	libdnet-devel
endif

DAQ_VERSION := 2.0.0
DAQ_ROOT := $(PACKAGEROOT)/daq/$(DAQ_VERSION)
DAQ_INC := $(DAQ_ROOT)/include
CPPFLAGS += -I$(DAQ_INC)
PATH := $(PATH):$(DAQ_ROOT)/bin

# On CentOS, RedHat we need to tell how to link against
# libnetfilter_queue.
ifneq ($(filter el,$(DIST_NAME)),)
LDFLAGS += -L$(PACKAGEROOT)/libnetfilter_queue/1.0.0/lib
endif
