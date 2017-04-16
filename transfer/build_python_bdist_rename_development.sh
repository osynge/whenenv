if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    sleep 4
    exit 1
fi

if [  "X${CHECKOUT_DATE}" = "X" ] ; then
    echo "CHECKOUT_DATE not defined"
    sleep 4
    exit 1
fi

cd $BUILD_SRC
architecture=$(arch)

for src in $(ls dist/*.tar.gz | grep $architecture )
do
    newname=$( echo ${src} | sed -e "s/tar\.gz/bin\.tar\.gz/")
    mv $src $newname
done

for src in $(ls dist/*bin.tar.gz | grep -v ${CHECKOUT_DATE} )
do
    newname=$( echo ${src} | sed -e "s/bin\.tar\.gz/rc${CHECKOUT_DATE}\.bin\.tar\.gz/")
    mv $src $newname
done

for src in $(ls dist/*bin.tar.gz | grep $architecture | grep ${CHECKOUT_DATE} )
do
    if [ "X${DIR_ART_BIN}" != "X" ] ; then
        cp ${src} ${DIR_ART_BIN}
    fi
done
