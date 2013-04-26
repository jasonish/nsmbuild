configure() {
    ./configure --prefix=${PREFIX} --enable-static --disable-shared
}

build() {
    make
    make install DESTDIR=${WRKINST}
}
