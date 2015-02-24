ORIGINALDIR=`pwd`
export SRC_VERSION
cd $BUILD_SRC

BOOTSTRAPSCRIPT=""
if test -f bootstrap.sh ; then
BOOTSTRAPSCRIPT=bootstrap.sh
fi
if test -f ./autogen.sh ; then
BOOTSTRAPSCRIPT=autogen.sh
fi
if [ "x${BOOTSTRAPSCRIPT}" = "x" ] ; then
  echo Bootstrap not found
  exit 1
fi
# now run boot strap command
sh $BOOTSTRAPSCRIPT

./configure --prefix=/usr
make dist
mkdir dist
mv *.tar.gz dist
make
make install DESTDIR=`pwd`/bdist
# make apidoc
make rpm

# Now we make the artifacts

cd $ORIGINALDIR
rm -f artifacts.tgz


mkdir -p build/dist
tar -C ${BUILD_SRC}/bdist -zcvf build/dist/${PRODUCT}_${SRC_VERSION}.$(arch).bin.tar.gz .

BASEFILE=`ls build/*tar.gz`
NEWFILE=`echo ${BASEFILE} | sed -e 's/\.tar\.gz/\.src\.tar\.gz/g' | sed -e 's/build/build\/dist/' `
mv ${BASEFILE} ${NEWFILE}

cp build/RPMS/x86_64/* build/dist
cp build/SRPMS/* build/dist

tar -zcvf artifacts.tgz build/dist
rm -rf $BUILD_SRC
