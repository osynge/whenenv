export CROOT_DIR="/root/sl6"

python /root/chrootbuilder \
--input \
/var/cache/vmcatcher/endorsed/aa42ca85-179b-4873-b12e-32d549bf02b6 \
--dest  /root/sl6 \
--overlay /root/overlay.cpio.bz2 \
--build
#chroot ${CROOT_DIR}
CHROOT_SCRIPT=${CROOT_DIR}/script
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
SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.desy.grid-virt.sort.release/tags"
TAG=\$(svn ls \${SVNLOCATION} | org_desy_grid_virt_sort_release.py | tail -n 1)
rm -rf build
svn co \${SVNLOCATION}/\${TAG} build
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
chroot ${CROOT_DIR} /bin/bash /script
rm -rf build
mv ${CROOT_DIR}/build build
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist