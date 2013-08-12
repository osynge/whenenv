echo "GIT_SRC=${GIT_SRC}"
echo "GIT_DEST=${GIT_DEST}"

if [  "X${GIT_SRC}" = "XX" ] ; then
    echo "GIT_SRC not defined"
    exit 1
fi
if [ "X${GIT_DEST}" = "X" ] ; then
    echo "GIT_DEST not defined"
    exit 1
fi
ORIGINALDIR=`pwd`

# Now we remove old checkout

rm -rf ${GIT_DEST}
git clone ${GIT_SRC} ${GIT_DEST}
cd ${GIT_DEST}

BUILD_SRC=${GIT_DEST}
export BUILD_SRC

cd ${ORIGINALDIR}

SRC_VERSION=`date '+20%y%m%d%H'`
export SRC_VERSION

