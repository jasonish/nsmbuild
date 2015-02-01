#! /bin/sh

MK_DIR=$(dirname $0)
OS_NAME=$(${MK_DIR}/config.sh os-name)

check_rpm_deps() {
    rc=0
    for dep in $@; do
	if rpm -q $dep > /dev/null 2>&1; then
	    echo "ok: $dep installed."
	else
	    echo "error: $dep not installed."
	    rc=1
	fi
    done
    return $rc
}

case "${OS_NAME}" in

    fedora|centos)
	check_rpm_deps $@ && exit 0 || exit 1
	;;

esac
