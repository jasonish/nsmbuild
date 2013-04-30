SUBDIRS =	$(notdir $(abspath $(dir $(wildcard */Makefile))))

include mk/defaults.mk

all:

clean:
	@for d in $(SUBDIRS); do \
		echo "Cleaning $$d."; \
		make -s -C $$d clean; \
	done
	@echo "Cleaning scratch files..."
	@rm -f mk/config.mk
	@find . -name \*~ -print0 | xargs -0 rm -f

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
