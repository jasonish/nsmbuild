#! /bin/sh

DIST_NAME="unknown"
DIST_REL="unkonwn"

if test -e /etc/os-release; then
    . /etc/os-release
    if [ "${ID}" != "" ]; then
	DIST_NAME=${ID}
    fi
    if [ "${VERSION_ID}" != "" ]; then
	DIST_REL=${VERSION_ID}
    fi
elif test -e /etc/redhat-release; then
    case $(cat /etc/redhat-release) in
	"CentOS release 6"*)
	    DIST_NAME="centos"
	    DIST_REL="6"
	    ;;
	Fedora*)
	    # Fedora handled by /etc/os-release.
	    ;;
    esac
fi

case "$1" in

    --name)
	echo ${DIST_NAME}
	;;

    --release)
	echo ${DIST_REL}
	;;

esac
