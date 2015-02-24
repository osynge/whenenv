ORIGINALDIR=`pwd`

cd $BUILD_SRC
export SRC_VERSION



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
tar -C ${BUILD_SRC}/bdist -zcvf build/dist/${PRODUCT}_${SRC_VERSION}.$(arch).bin.tar.gz .



tar -zcvf artifacts.tgz build/dist
rm -rf $BUILD_SRC
