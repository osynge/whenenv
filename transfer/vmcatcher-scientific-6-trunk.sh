set -x
export CROOT_DIR="/root/sl6"
#chroot ${CROOT_DIR}
CHROOT_SCRIPT=${CROOT_DIR}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
yum install git  org_desy_grid_virt_sort_release \
  rpmbuild \
  python-setuptools \
  rpm-build \
  -y
GITLOCATION="git://github.com/hepix-virtualisation/vmcatcher.git"
rm -rf build
git clone \${GITLOCATION} build
cd build
python setup.py sdist
for src in \$(ls dist/*.tar\.gz | grep -v \.src\.tar\.gz )
do
newname=\$( echo \${src} | sed -e "s/tar\.gz/rc${BUILD_NUMBER}\.src\.tar\.gz/")
mv \$src \$newname
done
python setup.py bdist_rpm \
    --release rc${BUILD_NUMBER} \
    --requires  "smimeX509validation hepixvmitrust python-sqlalchemy fetch-crl"
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
chroot ${CROOT_DIR} /bin/bash /script
rm -rf build
mv ${CROOT_DIR}/build build
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
