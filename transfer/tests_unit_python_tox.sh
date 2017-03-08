if [ "X${BUILD_SRC}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi
tox_path=`which tox`

TOXDIR_PREFIX=/workspace/tox

if [ "X${TOXDIR}" = "X" ] ; then
    echo no TOXDIR set
    TOXDIR="${TOXDIR_PREFIX}/executor_${EXECUTOR_NUMBER}_dir"
fi

if [ "X${TOXCMD}" = "X" ] ; then
    echo no TOXCMD set
    exit 3
fi



rm -rf ${TOXDIR}
mkdir -p ${TOXDIR}
cp -r ${BUILD_SRC}/* ${TOXDIR}


echo found tox at $tox_path
ORIGINALDIR=`pwd`
cd ${TOXDIR}
# this is not cross platform
#tox --skip-missing-interpreters
${TOXCMD}
cd $ORIGINALDIR
cp ${TOXDIR}/*.xml .
