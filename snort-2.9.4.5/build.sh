PATH=${NSMROOT}/versions/daq/${DAQ_VERSION}/bin:$PATH

configure() {
    ./configure --prefix=${PREFIX}
}

build() {
    make
    make install DESTDIR=${WRKINST}
}
