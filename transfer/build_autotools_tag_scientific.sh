pwd
if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
if [ "X${RPM_DEPENDS}" = "X" ] ; then
    echo "RPM_DEPENDS not defined"
    exit 1
fi

ORIGINALDIR=`pwd`
rm -rf bdist
cd $BUILD_SRC
./autogen.sh 
./configure
make dist
make install DESTDIR=${ORIGINALDIR}/bdist
# make apidoc
make rpm

# Now we make the artifacts

cd $ORIGINALDIR
rm -f artifacts.tgz


mkdir -p build/dist
tar -C bdist -zcvf build/dist/${PRODUCT}_0.0.1.bin.tar.gz .

BASEFILE=`ls build/*tar.gz`
NEWFILE=`echo ${BASEFILE} | sed -e 's/\.tar\.gz/\.src\.tar\.gz/g' | sed -e 's/build/build\/dist/' `
mv ${BASEFILE} ${NEWFILE}

cp build/RPMS/x86_64/* build/dist
cp build/SOURCES/* build/dist
cp build/SRPMS/* build/dist

tar -zcvf artifacts.tgz build/dist
rm -rf $BUILD_SRC
