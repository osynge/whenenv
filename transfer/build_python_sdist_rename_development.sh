if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
cd $BUILD_SRC
for src in $(ls dist/*.tar.gz | grep -v .src.tar.gz )
do
newname=$( echo ${src} | sed -e "s/tar\.gz/rc${BUILD_NUMBER}\.src\.tar\.gz/")
mv $src $newname
done
