# Some basic uname stuff.
echo "UNAME_SYSTEM := $(uname -s)"
echo "UNAME_ARCH := $(uname -m)"

DIST_NAME="unknown"
DIST_REL="unknown"
if [[ -e /etc/redhat-release ]]; then
    RELEASE_INFO=$(cat /etc/redhat-release)
    case ${RELEASE_INFO} in
	"CentOS release 6"*)
	    DIST_NAME="centos"
	    DIST_REL="6"
	    ;;
	"Fedora release 17"*)
	    DIST_NAME="fedora"
	    DIST_REL="17"
	    ;;
	"Fedora release 18"*)
	    DIST_NAME="fedora"
	    DIST_REL="18"
	    ;;
    esac
fi

echo "DIST_NAME := ${DIST_NAME}"
echo "DIST_REL := ${DIST_REL}"
