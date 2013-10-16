SUBDIRS =	$(notdir $(abspath $(dir $(wildcard */Makefile))))

include mk/defaults.mk
include mk/config.mk

all:

clean:
	@for d in $(SUBDIRS); do \
		make -C $$d clean || exit 1; \
	done
	@echo "Cleaning scratch files..."
	@rm -f .config-* mk/config-*
	@find . -name \*~ -print0 | xargs -0 rm -f

# Target to run "make fetch" in each package directory to make sure we
# have all the distfiles in our cache.
fetch:
	@for d in $(SUBDIRS); do \
		make -C $$d fetch; \
	done

show-root:
	@echo $(NSMROOT)

# List the available packages.
list:
	@for d in $(SUBDIRS); do \
		$(MAKE) -s -C $$d print-package-name; \
	done | sort

# Update the source tree - just a git pull for now.
update:
	git pull
	$(MAKE) post-update

post-update:

show-config:
	@echo "UNAME_MACHINE = $(UNAME_MACHINE)"
	@echo "UNAME_RELEASE = $(UNAME_RELEASE)"
	@echo "UNAME_SYSTEM = $(UNAME_SYSTEM)"
	@echo "UNAME_VERSION = $(UNAME_VERSION)"
	@echo "DIST_NAME = $(DIST_NAME)"
	@echo "DIST_REL = $(DIST_REL)"


