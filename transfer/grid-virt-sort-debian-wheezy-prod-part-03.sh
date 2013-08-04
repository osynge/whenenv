pwd
id
hostname -f
GIT_DEST=build
#SVNLOCATION="https://svnsrv.desy.de/public/grid-virt/org.desy.grid-virt.sort.release/tags"
GIT_SRC="git://github.com/osynge/grid_version_sort.git"
#TAG=`svn ls ${SVNLOCATION} | tail -n 1`
rm -rf build
#svn co ${SVNLOCATION}/${TAG} build
git clone ${GIT_SRC} ${GIT_DEST}
cd ${GIT_DEST}
GIT_TAG_LAST=$(git tag | grep "${GIT_TAG_FILTER}" | tail -n 1)

if [ "X${GIT_TAG_LAST}" = "X" ] ; then
    echo "GIT_TAG_LAST could not be not defined"
    git tag
    exit 1
fi
export GIT_TAG_LAST
git checkout ${GIT_TAG_LAST}

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
