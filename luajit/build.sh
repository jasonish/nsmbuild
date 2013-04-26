build() {
    make PREFIX=${PREFIX}
    make install PREFIX=${PREFIX} DESTDIR=${WRKINST}
}
