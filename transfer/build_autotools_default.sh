ORIGINALDIR=`pwd`

cd $BUILD_SRC
./autogen.sh 
./configure
make dist
mkdir dist
FILENAME=`ls -t *tar.gz | head -n 1`
NEWNAME=`echo ${FILENAME} | sed -e 's/\.tar\.gz/\.src\.tar\.gz/g'`
mv $FILENAME dist/$NEWNAME
make
make install DESTDIR=`pwd`/bdist
# make apidoc

# Now we make the artifacts

cd $ORIGINALDIR
rm -f artifacts.tgz


mkdir -p build/dist
tar -C ${BUILD_SRC}/bdist -zcvf build/dist/${PRODUCT}_${SRC_VERSION}.bin.tar.gz .



tar -zcvf artifacts.tgz build/dist
rm -rf $BUILD_SRC
