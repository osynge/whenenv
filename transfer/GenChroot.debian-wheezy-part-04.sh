cd rootfs
find . -print |cpio -o -Hnewc |bzip2 -9 -z -q -f > ../debian-wheezy.cpio.bz2
cd ..
rm -rf rootfs
