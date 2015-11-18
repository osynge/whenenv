if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
cd $BUILD_SRC
for src in $(ls dist/*.tar.gz | grep -v .src.tar.gz )
do
newname=$( echo ${src} | sed -e "s/tar\.gz/src\.tar\.gz/")
mv $src $newname
if [ "X${DIR_ART_SRC}" != "X" ] ; then
cp $newname ${DIR_ART_SRC}
fi
done
