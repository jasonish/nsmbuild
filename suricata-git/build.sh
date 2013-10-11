set -x

configure() {
    ./autogen.sh
    ./configure ${CONFIGURE_ARGS}
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
