NAME :=		daemonlogger
VERSION :=	1.2.1
REV :=		1

SOURCE :=	http://www.snort.org/downloads/463
SOURCE_FILE :=	$(NAME)-$(VERSION).tar.gz

include ../mk/build.mk

ifeq ($(call is_dist,el fedora),yes)
SYS_DEPENDS +=	libpcap-devel \
		libdnet-devel
endif
