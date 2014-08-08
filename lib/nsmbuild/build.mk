NSMBUILD := ../../../nsmbuild

all:

build install link:
	$(NSMBUILD) $@ .

clean:
	$(NSMBUILD) $@
