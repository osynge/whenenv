if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi

if [  "X${CHECKOUT_DATE}" = "X" ] ; then
    echo "CHECKOUT_DATE not defined"
    sleep 4
    exit 1
fi

cd $BUILD_SRC
for src in $(ls dist/*.tar.gz | grep -v .src.tar.gz )
do
    newname=$( echo ${src} | sed -e "s/tar\.gz/src\.tar\.gz/")
    mv $src $newname
done

for src in $(ls dist/*.src.tar.gz | grep -v ${CHECKOUT_DATE} )
do
    newname=$( echo ${src} | sed -e "s/src\.tar\.gz/rc${CHECKOUT_DATE}\.src\.tar\.gz/")
    mv $src $newname
done

for src in $(ls dist/*.src.tar.gz | grep ${CHECKOUT_DATE} )
do
    if [ "X${DIR_ART_SRC}" != "X" ] ; then
        cp ${src} ${DIR_ART_SRC}
    fi
done
