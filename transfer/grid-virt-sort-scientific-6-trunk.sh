set -x
if [ "X${CHROOT}" = "X" ] ; then
echo "no CHROOT set"
exit 1
fi
CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
id
hostname -f
yum install subversion \
    org-desy-grid-virt-sort-release  \
    rpmbuild \
    python-setuptools \
    rpm-build \
    -y
SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.desy.grid-virt.sort.release/trunk/"
rm -rf build
svn co \${SVNLOCATION} build
cd build
python setup.py sdist
for src in \$(ls dist/*.tar\.gz | grep -v \.src\.tar\.gz )
do
newname=\$( echo \${src} | sed -e "s/tar\.gz/rc${BUILD_NUMBER}\.src\.tar\.gz/")
mv \$src \$newname
done
python setup.py bdist_rpm --release rc${BUILD_NUMBER}
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
