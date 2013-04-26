build() {
    install -D -d -m 755 ${WRKINST}/${PREFIX}/bin
    install -m 755 pulledpork.pl ${WRKINST}/${PREFIX}/bin/pulledpork
    
    cp -a doc ${WRKINST}/${PREFIX}/
    cp -a etc ${WRKINST}/${PREFIX}/
    cp -a contrib ${WRKINST}/${PREFIX}/
    
    touch ${WRKINST}/${PREFIX}/doc/.nolink
    touch ${WRKINST}/${PREFIX}/etc/.nolink
    touch ${WRKINST}/${PREFIX}/contrib/.nolink
}
