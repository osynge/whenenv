set -x
CHROOT_SCRIPT=${CHROOT}/script
cat > ${CHROOT_SCRIPT} <<-EOF
#!/bin/bash
export http_proxy=http://squid:3128

id
hostname -f
yum install git \
  org-desy-grid-virt-sort-release \
  rpmbuild \
  python-setuptools \
  rpm-build \
  -y
GITLOCATION="https://github.com/osynge/dirvacua.git"
rm -rf build
git clone \${GITLOCATION} build
cd build
latest_tag=\$(git tag | org_desy_grid_virt_sort_release.py | tail -n 1)
git checkout \${latest_tag}
ls /dev/urandom
python setup.py sdist
for src in \$(ls dist/*.tar\.gz | grep -v \.src\.tar\.gz )
do
newname=\$( echo \${src} | sed -e "s/tar\.gz/src\.tar\.gz/")
mv \$src \$newname
done
python setup.py bdist_rpm \
    --requires  "m2crypto python-simplejson python-hashlib python-uuid"
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
