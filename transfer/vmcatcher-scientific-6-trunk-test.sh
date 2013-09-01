set -x
CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
set -x
env
export HOME=/root
export http_proxy=http://squid:3128
yum clean all
yum update -y
yum clean all
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
GITLOCATION="git://git.fritz.box/imagelist_functional_tests.git"
rm -rf build
git clone \${GITLOCATION}/ build
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
chroot ${CHROOT} /bin/bash /script
