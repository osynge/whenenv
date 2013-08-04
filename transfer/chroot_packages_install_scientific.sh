CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
set -x
http_proxy=http://squid:3128
export http_proxy
yum update -y
yum upgrade -y
yum install epel-release -y
yum install -y ${BUILD_DEPS_RPM}
#rpm -qa | grep vmcatcher
EOF
echo xx
cat ${CHROOT_SCRIPT}
echo xxls

chroot ${CHROOT} /bin/bash /script
