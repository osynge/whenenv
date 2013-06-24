set -x
export CROOT_DIR="/root/sl6"
python /root/chrootbuilder \
  --input /var/cache/vmcatcher/endorsed/aa42ca85-179b-4873-b12e-32d549bf02b6 \
  --dest  ${CROOT_DIR} \
  --overlay /var/cache/vmcatcher/endorsed/6b9384e5-5923-4d47-aaab-0fde0c52f8b8 \
  --build
#chroot ${CROOT_DIR}
CHROOT_SCRIPT=${CROOT_DIR}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
yum install git  org_desy_grid_virt_sort_release \
  rpmbuild \
  python-setuptools \
  rpm-build \
  -y
GITLOCATION="https://github.com/osynge/dirvacua.git"
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
