# nsmbuild

nsmbuild is a set of scripts to build various NSM applications (Snort,
Suricata, etc).  The idea is to record the requirements needed for
various platforms to make building quick and easy on a new system.

Each version of every package is installed into its own prefix making
it easy to keep multiple versions of a package installed. Package
binaries can be accessed directly in their prefix, or the may be
'linked' into the nsmbuild root for easier access.

## Example: Installing Suricata-1.4.7

* ./nsmbuild install suricata-1.4.7
* ./nsmbuild link suricata-1.4.7
* ./bin/suricata -V
