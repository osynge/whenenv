CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
cd build
ls
apt-get update -y
apt-get upgrade -y
apt-get install git \
    python \
    rpm-build \
    make \
    openssl-devel \
    python-devel \
    pkgconfig \
    swig \
    gcc \
    pexpect \
    lcg-CA \
    ca_BitFace \
    fetch-crl \
    vmcatcher \
    ntp \
    -y
EOF
echo xx
cat ${CHROOT_SCRIPT}
echo xx
chroot ${CHROOT} /bin/bash /script
