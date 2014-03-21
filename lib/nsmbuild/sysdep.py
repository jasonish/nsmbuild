import subprocess

def check_rpm(package):
    rc = subprocess.call(
        ["rpm", "-q", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return True if rc == 0 else False

def check_dpkg(package):
    pass

def check(config, package):
    if config["dist-name"] in ["el", "fedora"]:
        return check_rpm(package)
    elif config["dist-name"] in ["debian", "ubuntu"]:
        return check_dpkg(package)
