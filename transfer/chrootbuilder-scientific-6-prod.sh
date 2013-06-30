export CROOT_DIR="/root/sl6"



#chroot ${CROOT_DIR}
CHROOT_SCRIPT=${CROOT_DIR}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
id
hostname -f

hostname -f
yum clean all
yum install git  org_desy_grid_virt_sort_release \
  rpmbuild \
  python-setuptools \
  rpm-build \
  -y
GITLOCATION="oms101@git//var/lib/git/chrootbuilder.git"
rm -rf build
git clone \${GITLOCATION} build
cd build
latest_tag=\$(git tag | org_desy_grid_virt_sort_release.py | tail -n 1)
git checkout \${latest_tag}
python setup.py bdist_rpm \
    --requires  "python"
EOF
echo xx
cat ${CHROOT_SCRIPT}
echo xx
chroot ${CROOT_DIR} /bin/bash /script
rm -rf build
mv ${CROOT_DIR}/build build
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
