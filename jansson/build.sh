configure() {
    ./configure --prefix=${PREFIX}
}

build() {
    make
    make install DESTDIR=${WRKINST}
}
