CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
export http_proxy=http://squid:3128
apt-get update -y
apt-get upgrade -y
apt-get install git \
    python \
    make \
    swig \
    gcc \
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
