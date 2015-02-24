rm -rf debian-wheezy.cpio.bz2 rootfs
mkdir rootfs
# Using DE repository
# debootstrap wheezy rootfs http://ftp.de.debian.org/debian
debootstrap wheezy rootfs http://ftp.de.debian.org/debian
