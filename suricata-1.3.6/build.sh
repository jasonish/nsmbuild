configure() {

    CONFIGURE_ARGS="--prefix ${PREFIX}"

    # Platform specific configuration arguments.
    case "${UNAME_SYSTEM}" in
	Linux)
	    CONFIGURE_ARGS="${CONFIGURE_ARGS} --enable-af-packet"
	    ;;
    esac

    for opt in "${OPTS}"; do
	case "${opt}" in
	    +nfqueue)
		CONFIGURE_ARGS="${CONFIGURE_ARGS} --enable-nfqueue"
		;;
	esac
    done

    ./configure ${CONFIGURE_ARGS}
}

build() {

    make
    make install DESTDIR=${WRKINST}

    install -d -m 0755 ${WRKINST}/${PREFIX}/share
    install -m 0644 suricata.yaml \
	classification.config \
	reference.config \
	${WRKINST}/${PREFIX}/share/

    install -d -m 0755 ${WRKINST}/${PREFIX}/share/rules
    for file in rules/*.rules; do
	install -m 0644 $file ${WRKINST}/${PREFIX}/share/rules/
    done

    touch ${WRKINST}/${PREFIX}/share/.nolink

}
