#! /bin/sh

MK_DIR=$(dirname $0)
OS_NAME=$(${MK_DIR}/config.sh os-name)

check_rpm_deps() {
    not_installed=""
    rc=0
    for dep in $@; do
	if rpm -q $dep > /dev/null 2>&1; then
	    echo "ok: $dep installed."
	else
	    echo "error: $dep not installed."
	    not_installed="${not_installed}${dep} "
	    rc=1
	fi
    done
    if [ "${not_installed}" ]; then
	echo "please install ${not_installed}"
    fi
    return $rc
}

case "${OS_NAME}" in

    fedora|centos)
	check_rpm_deps $@ && exit 0 || exit 1
	;;

esac
