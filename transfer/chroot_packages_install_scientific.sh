CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
set -x
http_proxy=http://192.168.89.41:3128
export http_proxy
yum clean all
yum update -y
yum upgrade -y
yum install epel-release -y
yum clean metadata
yum install -y ${BUILD_DEPS_RPM}
#rpm -qa | grep vmcatcher
EOF
echo xx
cat ${CHROOT_SCRIPT}
echo xxls

chroot ${CHROOT} /bin/bash /script
