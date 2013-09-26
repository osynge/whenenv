pwd
if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
if [ "X${RPM_DEPENDS}" = "X" ] ; then
    echo "RPM_DEPENDS not defined"
    exit 1
fi

ORIGINALDIR=`pwd`
cd $BUILD_SRC

python setup.py sdist
for src in $(ls dist/*.tar.gz | grep -v .src.tar.gz )
do
newname=$( echo ${src} | sed -e "s/tar\.gz/src\.tar\.gz/")
mv $src $newname
done

python setup.py bdist
architecture=$(arch)
for src in $(ls dist/*.tar.gz | grep $architecture )
do
newname=$( echo ${src} | sed -e "s/tar\.gz/bin\.tar\.gz/")
mv $src $newname
done

cd $ORIGINALDIR
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
rm -rf $BUILD_SRC