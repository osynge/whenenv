chroot chroot

id
hostname -f

SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.desy.grid-virt.sort.release/tags"
TAG=`svn ls ${SVNLOCATION} | tail -n 1`
rm -rf build
svn co ${SVNLOCATION}/${TAG} build
cd build
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
