CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
set -x
http_proxy=http://squid:3128
export http_proxy
yum update -y
yum upgrade -y
yum install epel-release -y
yum install git \
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
rpm -qa | grep vmcatcher
chroot ${CHROOT} /bin/bash /script
