export CROOT_DIR="/root/sl6"
python /root/chrootbuilder \
--input \
/var/cache/vmcatcher/endorsed/aa42ca85-179b-4873-b12e-32d549bf02b6 \
--dest  /root/sl6 \
--overlay /root/trunk.overlay.cpio.bz2 \
--build

#chroot ${CROOT_DIR}
CHROOT_SCRIPT=${CROOT_DIR}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
set -x
env
export HOME=/root
yum clean all
yum update -y
yum clean all
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
    subversion \
    lcg-CA \
    ca_BitFace \
    fetch-crl \
    vmcatcher \
    m2crypto \
    ntp \
    -y
id
hostname -f
ntpdate pool.ntp.org
rpm -qa | grep hepix
rpm -qa | grep smime
rpm -qa | grep vmcatcher
SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.hepix.testing.hepixvmitrust/trunk"
rm -rf build
svn co \${SVNLOCATION}/ build
cd build
echo \`fetch-crl\`
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
chroot ${CROOT_DIR} /bin/bash /script
