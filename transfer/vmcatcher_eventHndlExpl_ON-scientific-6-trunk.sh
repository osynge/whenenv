CHROOT="/tmp/chroot/executor_${EXECUTOR_NUMBER}"
export CHROOT
chrootbuilder \
  --input \
  /var/cache/vmcatcher/endorsed/aa42ca85-179b-4873-b12e-32d549bf02b6 \
  --dest  ${CHROOT} \
  --overlay /root/overlay.cpio.bz2 \
  --build
#chroot ${CHROOT}
CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
yum install git  org_desy_grid_virt_sort_release \
  rpmbuild \
  python-setuptools \
  rpm-build \
  -y
GITLOCATION="git://github.com/grid-admin/vmcatcher_eventHndlExpl_ON.git"
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
    --requires  "vmcatcher"
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
