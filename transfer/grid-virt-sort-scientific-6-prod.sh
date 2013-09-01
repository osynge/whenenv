set -x
CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
id
hostname -f
yum update -y
yum install git \
    org-desy-grid-virt-sort-release  \
    rpmbuild \
    python-setuptools \
    rpm-build \
    -y
#SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.desy.grid-virt.sort.release/tags"
GITLOCATION="https://github.com/osynge/grid_version_sort.git"
rm -rf build
git clone \${GITLOCATION} build
cd build
python setup.py sdist
for src in \$(ls dist/*.tar\.gz | grep -v \.src\.tar\.gz )
do
newname=\$( echo \${src} | sed -e "s/tar\.gz/src\.tar\.gz/")
mv \$src \$newname
done
python setup.py bdist_rpm
python setup.py bdist
architecture=\$(arch)
for src in \$(ls dist/*.tar.gz | grep \$architecture )
do
newname=\$( echo \${src} | sed -e "s/tar\.gz/bin\.tar\.gz/")
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
