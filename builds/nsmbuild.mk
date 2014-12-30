# The top directory of all the nsmbuild tree.
TOPDIR :=	$(realpath $(dir $(word 2,$(MAKEFILE_LIST)))..)

# The directory where the builds are found.
BUILD_DIR :=	$(TOPDIR)/builds

# The root of the installation directory.
INSTALL_DIR :=	$(TOPDIR)/installed

# The install prefix for this build.
PREFIX :=	$(INSTALL_DIR)/$(NAME)-$(VERSION)

WORKDIR ?=	$(shell pwd)/work
SRCDIR ?=	$(WORKDIR)/$(NAME)-$(VERSION)

all: build

dep:
	@for dep in $(DEPS); do \
		if test -e $(INSTALL_DIR)/$$dep; then \
			echo "$$dep already installed."; \
		else \
			cd $(BUILD_DIR)/$$dep && $(MAKE) build install; \
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
