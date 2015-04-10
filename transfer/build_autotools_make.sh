ORIGINALDIR=`pwd`
cd $BUILD_SRC
make dist
mkdir dist
FILENAME=`ls -t *tar.gz | head -n 1`
NEWNAME=`echo ${FILENAME} | sed -e 's/\.tar\.gz/\.src\.tar\.gz/g'`
mv $FILENAME dist/$NEWNAME
make
make install DESTDIR=`pwd`/bdist
mkdir -p dist
tar -C bdist -zcvf dist/${PRODUCT}_${SRC_VERSION}.$(arch).bin.tar.gz .
# make apidoc
