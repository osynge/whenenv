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
GIT_TAG_LAST=$(git tag | grep "${GIT_TAG_FILTER}" | org_desy_grid_virt_sort_release.py  | tail -n 1)
BUILD_SRC=${GIT_DEST}
export BUILD_SRC

cd ${ORIGINALDIR}

SRC_VERSION=${GIT_TAG_LAST}rc${BUILD_NUMBER}
export SRC_VERSION

