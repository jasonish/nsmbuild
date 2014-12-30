# The top directory of all the nsm builds.
TOPDIR :=	$(realpath $(dir $(word 2,$(MAKEFILE_LIST))))

# The root of the installation directory.
INSTALL_ROOT :=	/opt/nsmbuild

# The install prefix for this build.
PREFIX :=	$(INSTALL_ROOT)/builds/$(NAME)-$(VERSION)

WORKDIR ?=	$(shell pwd)/work
SRCDIR ?=	$(WORKDIR)/$(NAME)-$(VERSION)

all: build

dep:
	@for dep in $(DEPS); do \
		if test -e $(INSTALL_ROOT)/builds/$$dep; then \
			echo "$$dep already installed."; \
		else \
			cd $(TOPDIR)/$$dep && $(MAKE) build; \
		fi \
	done

fetch:
	@if ! test -e `basename $(SOURCE)`; then \
		curl -f -O -L -# $(SOURCE); \
	fi

extract:
	if ! test -e $(SRCDIR); then \
		mkdir -p $(WORKDIR); \
		cd $(WORKDIR); \
		tar zxvf ../`basename $(SOURCE)`; \
	fi

clean:
	rm -rf $(WORKDIR)
