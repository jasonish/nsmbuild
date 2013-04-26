JANSSON_VERSION=2.4
JANSSON_ROOT=${PACKAGEROOT}/jansson/${JANSSON_VERSION}
JANSSON_INC=${JANNSON_ROOT}/include
JANSSON_LIB=${JANNSON_ROOT}/lib

LUAJIT_VERSION=2.0.0
LUAJIT_ROOT=${PACKAGEROOT}/luajit/2.0.0
LUAJIT_INC=${LUAJIT_ROOT}/include/luajit-2.0
LUAJIT_LIB=${LUAJIT_ROOT}/lib

set -x

configure() {

    ARGS="--prefix ${PREFIX}
		--with-libjansson-includes=${JANSSON_INC}
		--with-libjansson-libraries=${JANSSON_LIB}
		--enable-luajit
		--with-libluajit-includes=${LUAJIT_INC}
		--with-libluajit-libraries=${LUAJIT_LIB}"

    # Platform specific configuration arguments.
    case "${UNAME_SYSTEM}" in
	Linux)
	    ARGS="${ARGS} --enable-af-packet"
	    LDFLAGS="${LDFLAGS} -Wl,-rpath -Wl,${PREFIX}/lib"
	    LDFLAGS="${LDFLAGS} -Wl,-rpath -Wl,${LUAJIT_LIB}"
	    ;;
    esac

    for opt in "${OPTS}"; do
	case "${opt}" in
	    +nfqueue)
		ARGS="${ARGS} --enable-nfqueue"
		;;
	esac
    done
    
    LDFLAGS="${LDFLAGS}" ./configure ${ARGS}
}

build() {

    make
    make install DESTDIR=${WRKINST}

    install -m 0644 suricata.yaml \
	classification.config \
	reference.config \
	threshold.config ${WRKINST}/${PREFIX}/share/

    install -d -m 0755 ${WRKINST}/${PREFIX}/share/rules
    for file in rules/*.rules; do
	install -m 0644 $file ${WRKINST}/${PREFIX}/share/rules/
    done

    touch ${WRKINST}/${PREFIX}/share/.nolink
}
