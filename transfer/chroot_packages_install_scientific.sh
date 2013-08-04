CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
cd build
ls
yum update -y
yum upgrade -y
yum install epel-release -y
yum install subversion \
    python \
    rpm-build \
    make \
    org-desy-grid-virt-sort-release \
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
