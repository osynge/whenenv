CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
export http_proxy=http://squid:3128
apt-get update -y
apt-get upgrade -y
apt-get install ${BUILD_DEPS_DPKG} \
    -y

EOF
echo xx
cat ${CHROOT_SCRIPT}
echo xx
chroot ${CHROOT} /bin/bash /script
