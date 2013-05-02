# Figure out where we live.
TOPDIR :=	$(realpath $(dir $(word 2,$(MAKEFILE_LIST)))..)
NSMBUILDROOT :=	$(TOPDIR)

# Directory where the build infrastructure makefiles and scripts live.
MKPATH :=	$(TOPDIR)/mk

# Pull in default settings that can be overridden by user settings.
include $(MKPATH)/defaults.mk

# Pull in configuration parameters that are dynamically created by a
# script.  Do this before pulling in local settings just in case they
# need to be overrided.
-include $(MKPATH)/config.mk

# Now pull in user overrides.
-include $(TOPDIR)/local.mk

# Where packages are installed.
PACKAGEROOT :=	$(NSMROOT)/packages

# Where distfiles will be saved.
DISTDIR :=	$(TOPDIR)/distfiles

# Directory where building activity takes place.
WRKDIR :=	$(CURDIR)/work

# Subdirectory of $(WRKDIR) where actual source is.
WRKSRC ?=	$(WRKDIR)/$(NAME)-$(VERSION)

# The "fake" location the package should install to.
WRKINST :=	$(WRKDIR)/fakeroot

# Prefix for the package to use (ie: --prefix).
PREFIX =	$(PACKAGEROOT)/$(NAME)/$(VERSION)-$(REV)

# Compute the filename of the source if not explicitly provided.
SOURCE_FILE ?=	$(notdir $(SOURCE))

# Variables that will be export to child processes.
EXPORTS =	CURDIR=$(CURDIR) \
		NSMROOT=$(NSMROOT) \
		NSMBUILDROOT=$(NSMBUILDROOT) \
		PACKAGEROOT=$(PACKAGEROOT) \
		PREFIX=$(PREFIX) \
		WRKINST=$(WRKINST) \
		OPTS="$(OPTS)" \
		UNAME_SYSTEM=$(UNAME_SYSTEM)
EXPORTS +=	DIST_NAME=$(DIST_NAME)
EXPORTS +=	DIST_REL=$(DIST_REL)
EXPORTS +=	CPPFLAGS=$(CPPFLAGS)
EXPORTS +=	LDFLAGS=$(LDFLAGS)

EXPORTS +=	CONFIGURE_ARGS="$(CONFIGURE_ARGS)"

# Prevent make from trying to generate a file named build from build.sh.
.PHONY:		build $(MKPATH)/config.mk

-include options

# By default we'll just build, but not install the package.
all: build

$(MKPATH)/config.mk:
	@/bin/sh $(MKPATH)/config.sh > $@

info:
	@echo "Name:     $(NAME)"
	@echo "Version:  $(VERSION)"
	@echo "Revision: $(REV)"
	@echo "Options: $(OPTIONS)"
	@echo "NSM Dependencies: $(DEPENDS)"
	@echo "System Dependencies: $(SYS_DEPENDS)"

check-deps:
ifdef SKIP_SYS_DEPS
	@echo "Skipping system dependency check."
else
	@$(EXPORTS) /bin/sh $(MKPATH)/check-deps $(SYS_DEPENDS)
endif

# Target to install dependencies.
install-deps:
	@for dep in $(DEPENDS); do \
		if ! make -C $(TOPDIR)/$$dep install; then \
			echo "Failed to install dependency $$dep."; \
			exit 1; \
		fi \
	done

$(DISTDIR)/$(SOURCE_FILE):
	@echo "Downloading $(SOURCE_FILE):"
	@curl -# -L -o $(DISTDIR)/$(SOURCE_FILE) $(SOURCE)

fetch: $(DISTDIR)/$(SOURCE_FILE)

clean:
	@echo "Cleaning $(NAME)..."
	@rm -rf $(CURDIR)/work
	@rm -f *~

$(WRKSRC): $(DISTDIR)/$(SOURCE_FILE)
	@echo "Extracting $(SOURCE_FILE)..."
	@mkdir -p $(WRKDIR)
	@cd $(WRKDIR) && python $(MKPATH)/extract.py \
		$(addprefix $(DISTDIR)/,$(SOURCE_FILE))

# Touch the new directory to make sure it newer than the source file.
	@touch $@

extract: $(WRKSRC)

$(WRKDIR)/patch_done:
	@if test -d patches; then \
		for p in patches/*; do \
	 		echo "Applying patch $$p."; \
	 		(cd $(WRKSRC) && patch -p1 < $(CURDIR)/$$p); \
	 	done \
	fi
	@touch $@

patch: extract $(WRKDIR)/patch_done

$(WRKDIR)/configure_done:
	@cd $(WRKSRC); $(EXPORTS) /bin/sh $(MKPATH)/build.sh configure
ifdef OPTS
	@echo "Caching OPTS to ./options."
	@echo "OPTS=$(OPTS)" > $(CURDIR)/options
else
	@rm -f $(CURDIR)/options
endif
	@touch $@

configure: patch $(WRKDIR)/configure_done

$(WRKDIR)/build_done:
	@echo "Building $(NAME)..."
	@cd $(WRKSRC); $(EXPORTS) /bin/sh $(MKPATH)/build.sh build
	@touch $@

build: check-deps install-deps configure $(WRKDIR)/build_done

# This does the actual install.
$(PREFIX): build
	@echo "Installing $(NAME)-$(VERSION)..."
	@$(SUDO) mkdir -p $@
	@(cd $(WRKINST)$(PREFIX) && tar cf - *) | \
		(cd $(PREFIX) && $(SUDO) tar xf -)
ifdef SUDO
	@$(SUDO) chown root:root $(PREFIX)
endif
	@$(SUDO) rm -f $(dir $(PREFIX))/$(VERSION)
	@$(SUDO) ln -s $(VERSION)-$(REV) $(dir $(PREFIX))/$(VERSION)

install:
	@if test -e $(PREFIX); then \
		echo "Package $(NAME)-$(VERSION)-$(REV) already installed."; \
	else \
		$(MAKE) $(PREFIX); \
	fi

uninstall: unlink
	@echo "Uninstalling $(NAME)-$(VERSION)-$(REV)..."
	@$(SUDO) rm -rf $(PREFIX)
	@test -e $(dir $(PREFIX))/$(VERSION) || \
		$(SUDO) rm -f $(dir $(PREFIX))/$(VERSION)
	@if [ -z "`ls -A $(dir $(PREFIX))`" ]; then \
		$(SUDO) rmdir $(dir $(PREFIX)); \
	fi

unlink:
	@$(SUDO) python $(TOPDIR)/nsmbuild -v unlink $(NAME)

link:
	@$(SUDO) python $(TOPDIR)/nsmbuild -v link $(NAME)/$(VERSION)

print-package-name:
	@echo $(NAME)-$(VERSION)-$(REV)
