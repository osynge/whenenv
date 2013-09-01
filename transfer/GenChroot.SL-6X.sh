hostname -f
#unset http_proxy
#yum clean all
yum update -y
yum upgrade -y
export http_proxy=http://squid:3128
export CROOT_DIR="/tmp/foo/diskless"
rm -f sl6.cpio.bz2
dirStart=`pwd`
# This would be needed to get the centos-release or sl-release RPM.
#unset http_proxy
rm -f sl-release*.rpm
yumdownloader sl-release

# Make a clean chroot.
rm -rf ${CROOT_DIR}
mkdir -p ${CROOT_DIR}
# Install the release data for yum
rpm -i --root="${CROOT_DIR}" --nodeps sl-release*.rpm
#Now install the essentials.
#echo `yum --installroot=${CROOT_DIR} -y -q install basesystem filesystem bash kernel passwd yum`
yum --installroot=${CROOT_DIR} -y -d 1 install basesystem filesystem bash kernel passwd yum
pushd ${CROOT_DIR}
	
# This next line is important, your system won't boot without it
ln -s ./sbin/init ./init 
echo NETWORKING=yes > etc/sysconfig/network
#	chroot .
#	pwconv
# Set your root password
#	passwd
#	exit
# find . -depth -print0 | cpio -ovc0 | gzip -7 > ${dirStart}/sl6.cpio.gz
# find . -depth -print0 | cpio -oc0 | gzip -7 > ${dirStart}/sl6.cpio.gz
#chroot . /usr/bin/yum clean all
find . -print |cpio -o -Hnewc |bzip2 -9 -z -q -f > ${dirStart}/sl6.cpio.bz2

popd
rm -rf ${CROOT_DIR}
du -h sl6.cpio.bz2

