
ORIGINALDIR=`pwd`


id
hostname -f
yum install git \
  org-desy-grid-virt-sort-release \
  rpmbuild \
  python-setuptools \
  rpm-build \
  -y
GITLOCATION="git://github.com/grid-admin/vmcatcher_eventHndlExpl_ON.git"
rm -rf build
git clone ${GITLOCATION} build
cd build
latest_tag=$(git tag | org_desy_grid_virt_sort_release.py | tail -n 1)
git checkout ${latest_tag}
ls /dev/urandom
python setup.py sdist
for src in $(ls dist/*.tar\.gz | grep -v \.src\.tar\.gz )
do
newname=$( echo \${src} | sed -e "s/tar\.gz/src\.tar\.gz/")
mv $src $newname
done
python setup.py bdist_rpm \
    --requires  "vmcatcher"
python setup.py bdist
architecture=$(arch)
for src in $(ls dist/*.tar.gz | grep \$architecture )
do
newname=$( echo \${src} | sed -e "s/tar\.gz/bin\.tar\.gz/")
mv $src $newname
done
cd $ORIGINALDIR
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
