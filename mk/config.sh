# Some basic uname stuff.
echo "UNAME_SYSTEM := $(uname -s)"
echo "UNAME_ARCH := $(uname -m)"

DIST_NAME="unknown"
DIST_REL="unknown"

if [[ -e /etc/redhat-release ]]; then
    case $(cat /etc/redhat-release) in
	"CentOS release 6"*)
	    DIST_NAME="centos"
	    DIST_REL="6"
	    echo "export IS_RHEL := yes"
	    echo "export IS_CENTOS := yes"
	    ;;
	"Fedora release 17"*)
	    DIST_NAME="fedora"
	    DIST_REL="17"
	    echo "export IS_FEDORA := yes"
	    ;;
	"Fedora release 18"*)
	    DIST_NAME="fedora"
	    DIST_REL="18"
	    echo "export IS_FEDORA := yes"
	    ;;
    esac
fi

echo "DIST_NAME := ${DIST_NAME}"
echo "DIST_REL := ${DIST_REL}"
