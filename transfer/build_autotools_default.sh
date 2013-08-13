ORIGINALDIR=`pwd`

cd $BUILD_SRC
./autogen.sh 
./configure
make dist
mkdir dist
mv *.tar.gz dist
make
make install DESTDIR=`pwd`/bdist
# make apidoc

# Now we make the artifacts

cd $ORIGINALDIR
rm -f artifacts.tgz


mkdir -p build/dist
tar -C ${BUILD_SRC}/bdist -zcvf build/dist/${PRODUCT}_${SRC_VERSION}.bin.tar.gz .

BASEFILE=`ls build/*tar.gz`
NEWFILE=`echo ${BASEFILE} | sed -e 's/\.tar\.gz/\.src\.tar\.gz/g' | sed -e 's/build/build\/dist/' `
mv ${BASEFILE} ${NEWFILE}


tar -zcvf artifacts.tgz build/dist
rm -rf $BUILD_SRC
