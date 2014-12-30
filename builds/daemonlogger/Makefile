NAME :=		daemonlogger
VERSION :=	1.2.1

SOURCE :=	http://downloads.sourceforge.net/project/daemonlogger/daemonlogger-1.2.1.tar.gz

include ../nsmbuild.mk

# Override PREFIX to not include version info.
PREFIX :=	$(INSTALL_DIR)/$(NAME)

build: fetch dep extract
	cd $(SRCDIR) && \
		./configure --prefix=$(PREFIX) \
		&& \
	make

install:
	cd $(SRCDIR) && make install


