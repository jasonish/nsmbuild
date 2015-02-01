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

OS_NAME :=	$(shell $(BUILD_DIR)/mk/config.sh os-name)
OS_VER :=	$(shell $(BUILD_DIR)/mk/config.sh os-version)

all: build

dep:
	@if [ "$(SYS_DEPS)" ]; then \
		$(BUILD_DIR)/mk/check-sys-deps.sh $(SYS_DEPS) || echo failed; \
	fi

	@if [ "$(DEPS)" ]; then \
		for dep in "$(DEPS)"; do \
			if test -e $(INSTALL_DIR)/$$dep; then \
	 			echo "$$dep already installed."; \
		 	else \
		 		cd $(BUILD_DIR)/$$dep && \
					$(MAKE) build install; \
	 		fi \
		done \
	fi

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
