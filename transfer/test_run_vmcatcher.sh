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

echo \$(fetch-crl)
cp /etc/yokel/hepix_tests_keydetails.py keydetails.py
python test_vmilisttool.py
python test_smimeX509validation.py
python test_vmlisub_endorser.py
python test_vmlisub_sub.py
python test_vmlisub_cache.py
EOF
echo xx
cat ${CHROOT_SCRIPT}
echo xx
chroot ${CHROOT} /bin/bash /script