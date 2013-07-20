
if [ "X" = "X${CHROOT}" ]
then 
    echo "No CHROOT set"
    exit 1
fi
chroot ${CHROOT}
echo "now in the chroot"
pwd
id
hostname -f
GITLOCATION="https://github.com/osynge/dirvacua.git"
rm -rf build
git clone ${GITLOCATION} build
cd build
latest_tag=$(git tag | org_desy_grid_virt_sort_release.py | tail -n 1)
#latest_tag=`git tag | tail -n 1`
git checkout ${latest_tag}
python setup.py sdist
for src in $(ls dist/*.tar\.gz | grep -v .src.tar.gz )
do
  newname=$( echo ${src} | sed -e "s/tar.gz/src.tar.gz/")
  mv $src $newname
done
python setup.py bdist
architecture=$(arch)
for src in $(ls dist/*.tar.gz | grep $architecture )
do
  newname=`echo ${src} | sed -e "s/tar\.gz/bin\.tar\.gz/"`
  mv $src $newname
done
cd ..
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
