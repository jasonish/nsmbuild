NAME :=		barnyard2
VERSION :=	1.13
REV :=		1

SOURCE :=	https://github.com/firnsy/barnyard2/archive/v2-$(VERSION).tar.gz
SOURCE_FILE :=	$(NAME)-$(VERSION).tar.gz

WRKSRC =	$(WRKDIR)/$(NAME)-2-$(VERSION)

OPTIONS :=	+mysql \
		+postgresql

include ../mk/build.mk

CONFIGURE_ARGS += --prefix=$(PREFIX)

# Extra configure options, may apply to more than just RedHat,CentOS,Fedora.
ifeq ($(call is_dist,el fedora), yes)
CONFIGURE_ARGS+=--enable-ipv6 \
		--enable-gre \
		--enable-mpls

SYS_DEPENDS +=	libtool
endif

# +mysql
ifeq ($(call has_opt,+mysql),yes)

  CONFIGURE_ARGS += --with-mysql

  # RedHat/CentOS/Fedora
  ifeq ($(call is_dist,el fedora),yes)
    SYS_DEPENDS += mysql-libs mysql-devel
    ifeq ($(UNAME_MACHINE),x86_64)
      CONFIGURE_ARGS+=--with-mysql-libraries=/usr/lib64/mysql
    endif
  endif
endif

# +postgresql
ifeq ($(call has_opt,+postgresql),yes)

  CONFIGURE_ARGS += --with-postgresql

  # RedHat/CentOS/Fedora
  ifeq ($(call is_dist,el fedora),yes)
    SYS_DEPENDS += postgresql-libs
  endif
endif

