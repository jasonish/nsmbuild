ifndef MKPATH
MKPATH :=		$(realpath $(dir $(word 2,$(MAKEFILE_LIST))))
endif

# System information.
UNAME_MACHINE :=	$(shell uname -m 2>/dev/null || echo unknown)
UNAME_RELEASE :=	$(shell uname -r 2>/dev/null || echo unknown)
UNAME_SYSTEM :=		$(shell uname -s 2>/dev/null || echo unknown)
UNAME_VERSION :=	$(shell uname -v 2>/dev/null || echo unknown)

# Distribution information.
DIST_NAME ?=		$(shell $(MKPATH)/config.sh --name)
DIST_REL ?=		$(shell $(MKPATH)/config.sh --release)

# Deprecate these.
ifeq ($(DIST_NAME),centos)
export IS_RHEL := yes
export IS_CENTOS := yes
endif

ifeq ($(DIST_NAME),fedora)
export IS_FEDORA := yes
endif
