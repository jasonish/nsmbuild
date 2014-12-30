all:

clean:
	@for d in */Makefile; do \
		$(MAKE) -C `dirname $$d` clean; \
	done
	find . -name \*~ -exec rm -f {} \;
