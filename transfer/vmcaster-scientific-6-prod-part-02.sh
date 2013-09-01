#chroot ${CHROOT}
CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
id
hostname -f
export http_proxy=http://squid:3128
hostname -f
yum clean all
yum install git  org_desy_grid_virt_sort_release \
  rpmbuild \
  python-setuptools \
  rpm-build \
  -y
GITLOCATION="git://github.com/hepix-virtualisation/vmcaster.git"
rm -rf build
git clone \${GITLOCATION} build
cd build
latest_tag=\$(git tag | org_desy_grid_virt_sort_release.py | tail -n 1)
git checkout \${latest_tag}
python setup.py bdist_rpm \
    --requires  "python-sqlalchemy m2crypto python-magic"
EOF
echo xx
cat ${CHROOT_SCRIPT}
echo xx
chroot ${CHROOT} /bin/bash /script
rm -rf build
mv ${CHROOT}/build build
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
