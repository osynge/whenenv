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
yum install git  org_desy_grid_virt_sort_release \
  rpmbuild \
  python-setuptools \
  rpm-build \
  -y
GITLOCATION="git://github.com/hepix-virtualisation/vmcatcher.git"
rm -rf build
git clone \${GITLOCATION} build
cd build
#latest_tag=$(git tag | org_desy_grid_virt_sort_release.py | tail -n 1)
latest_tag=$(git tag | grep vmcatcher | tail -n 1)
git checkout ${latest_tag}
python setup.py bdist_rpm \
    --requires  "smimeX509validation hepixvmitrust python-sqlalchemy fetch-crl"


EOF
echo xx
cat ${CHROOT_SCRIPT}
echo xx
chroot ${CROOT_DIR} /bin/bash /script
rm -rf build
mv ${CROOT_DIR}/build build
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
