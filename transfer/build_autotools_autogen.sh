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
