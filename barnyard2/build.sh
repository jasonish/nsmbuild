configure() {

    ARGS="--prefix ${PREFIX}"
    
    for opt in "${OPTS}"; do
	case "${opt}" in
	    +mysql)
		ARGS="${ARGS} --with-mysql"
		;;
	    +postgresql)
		ARGS="${ARGS} --with-postgresql"
		;;
	esac
    done

    ./autogen.sh
    ./configure ${ARGS}
}

build() {
    make
    make install DESTDIR=${WRKINST}
}
