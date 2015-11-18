if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
cd $BUILD_SRC
architecture=$(arch)
for src in $(ls dist/*.tar.gz | grep $architecture )
do
newname=$( echo ${src} | sed -e "s/tar\.gz/bin\.tar\.gz/")
mv $src $newname
if [ "X${DIR_ART_BIN}" != "X" ] ; then
cp $newname ${DIR_ART_BIN}
fi
done
