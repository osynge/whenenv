pwd
if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
ORIGINALDIR=`pwd`
cd $BUILD_SRC

python setup.py sdist
for src in $(ls dist/*.tar.gz | grep -v .src.tar.gz )
do
newname=$( echo ${src} | sed -e "s/tar\.gz/rc${BUILD_NUMBER}\.src\.tar\.gz/")
mv $src $newname
done

python setup.py bdist
architecture=$(arch)
for src in $(ls dist/*.tar.gz | grep $architecture )
do
newname=$( echo ${src} | sed -e "s/tar\.gz/\.bin\.tar\.gz/")
mv $src $newname
done

python setup.py bdist_rpm \
    --requires  "python-sqlalchemy m2crypto python-magic smimeX509validation "

cd $ORIGINALDIR
rm -f artifacts.tgz
tar -zcvf artifacts.tgz build/dist
rm -rf $BUILD_SRC
