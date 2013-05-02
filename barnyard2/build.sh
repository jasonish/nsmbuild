configure() {
    ./autogen.sh
    ./configure ${CONFIGURE_ARGS}
}

build() {
    make
    make install DESTDIR=${WRKINST}
}
