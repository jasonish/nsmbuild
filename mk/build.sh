set -e

# Define a dummy configure function.
configure() {
    true
}

# Define a dummy build function.
build() {
    true
}

# Source in the package build script.
echo "${CURDIR}/build.sh"
if [ -e ${CURDIR}/build.sh ]; then
    . ${CURDIR}/build.sh
else
    echo "No package build.sh found."
fi

case "$1" in
    configure)
	configure
	;;

    build)
	build
	;;
esac
