# nsmbuild

nsmbuild is a set of makefiles and scripts to build various NSM
applications (Snort, Suricata, etc).  The idea is to record the
requirements needed for various platforms to make building quick and
easy on a new system.

Each version of every package is installed into its own prefix making
it easy to keep multiple versions of a package installed. Package
binaries can be accessed directly in their prefix, or the may be
'linked' into the NSMROOT for easier access.

## Example: Installing Suricata-1.4.x

* `cd suricata-1.4.x`
* `make install`
* `make link`

## Setup

Setup is simple as creating the directory /opt/nsm.  This can be
changed by copying local.mk.dist to local.mk and pointing the NSMROOT
to your desired location.

If your NSMROOT is not writable by the user doing the builds,
uncomment SUDO which will have nsmbuild use sudo to install the files
under NSMROOT allowing you to build as a non-root user.
