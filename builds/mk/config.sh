#! /bin/sh

case "$1" in

    os-name)

	# This should catch CentOS 7, Fedora 20+ and others.
	if [ -e /etc/os-release ]; then
	    . /etc/os-release
	    echo ${ID}

	elif [ -e /etc/redhat-release ]; then
	    redhat_release=$(cat /etc/redhat-release)
	    case "${redhat_release}" in
		CentOS*)
		    echo "centos"
		    ;;
	    esac

	fi
	;;

    os-version)

	# This should catch CentOS 7, Fedora 20+ and others.
	if [ -e /etc/os-release ]; then
	    . /etc/os-release
	    echo ${VERSION_ID}

	elif [ -e /etc/redhat-release ]; then
	    redhat_release=$(cat /etc/redhat-release)
	    case "${redhat_release}" in
		"CentOS release 6*")
		    echo "6"
		    ;;
	    esac

	fi
	;;

esac
