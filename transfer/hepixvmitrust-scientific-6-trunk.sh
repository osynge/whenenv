set -x
#chroot ${CHROOT}
CHROOT_SCRIPT=${CHROOT}/script
GITLOCATION="git://github.com/hepix-virtualisation/hepixvmitrust.git"
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
yum install git \
  org-desy-grid-virt-sort-release \
  rpmbuild \
  python-setuptools \
  rpm-build \
  m2crypto \
  -y
rm -rf build
git clone ${GITLOCATION} build
cd build
python setup.py sdist
for src in \$(ls dist/*.tar\.gz | grep -v \.src\.tar\.gz )
do
newname=\$( echo \${src} | sed -e "s/tar\.gz/rc${BUILD_NUMBER}\.src\.tar\.gz/")
mv \$src \$newname
done
python setup.py bdist_rpm \
    --release rc${BUILD_NUMBER}
python setup.py bdist
architecture=\$(arch)
for src in \$(ls dist/*.tar.gz | grep \$architecture )
do
newname=\$( echo \${src} | sed -e "s/tar\.gz/rc${BUILD_NUMBER}\.bin\.tar\.gz/")
mv \$src \$newname
done

EOF
echo xx
cat ${CHROOT_SCRIPT}
echo xx
chroot ${CHROOT} /bin/bash /script
rm -rf build
mv ${CHROOT}/build build
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
