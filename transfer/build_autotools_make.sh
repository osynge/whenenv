if [ "X${DIR_ART_BIN}" = "X" ] ; then
echo "DIR_ART_RPMS not defined"
sleep 1
exit 1
fi

if [ "X${DIR_ART_SRC}" = "X" ] ; then
echo "DIR_ART_SRPMS not defined"
sleep 1
exit 1
fi

if [ "X${BUILD_SRC}" = "X" ] ; then
echo "DIR_ART_SRPMS not defined"
sleep 1
exit 1
fi

ORIGINALDIR=`pwd`
cd $BUILD_SRC
make dist
mkdir dist
FILENAME=`ls -t *tar.gz | head -n 1`
NEWNAME=`echo ${FILENAME} | sed -e 's/\.tar\.gz/\.src\.tar\.gz/g'`
mv $FILENAME ${DIR_ART_SRC}/$NEWNAME
make
make install DESTDIR=`pwd`/bdist/${PRODUCT}-${SRC_VERSION}
tar -C bdist -zcvf ${DIR_ART_BIN}/${PRODUCT}_${SRC_VERSION}.$(arch).bin.tar.gz .
# make apidoc
