echo "GIT_SRC=${GIT_SRC}"
echo "GIT_DEST=${GIT_DEST}"

if [  "X${GIT_SRC}" = "X" ] ; then
    echo "GIT_SRC not defined"
    exit 1
fi


if [  "X${CHECKOUT_DATE}" = "X" ] ; then
    echo "CHECKOUT_DATE not defined"
    exit 1
fi


if [ "X${GIT_DEST}" = "X" ] ; then
    echo "GIT_DEST not defined"
    exit 1
fi

if [ "X${GIT_SRC_CLEANED}" = "X" ] ; then
    echo "GIT_SRC_CLEANED not defined"
    GIT_SRC_CLEANED=$(echo ${GIT_SRC} | sed -s 's/[\.:\/]/_/g')
fi


if [ "X${GIT_CLONE_DIR_BASE}" = "X" ] ; then
    
    GIT_CLONE_DIR_BASE="${HOME}/var/gitcache"
    echo "Defaulting GIT_CLONE_DIR : ${GIT_CLONE_DIR_BASE}"
fi



if [ "X${GIT_CLONE_DIR}" = "X" ] ; then
    GIT_CLONE_DIR="${GIT_CLONE_DIR_BASE}/${GIT_SRC_CLEANED}"
    echo "Defaulting GIT_CLONE_DIR : ${GIT_CLONE_DIR}"
fi


if [ ! -d ${GIT_CLONE_DIR} ] ; then
git clone --mirror ${GIT_SRC} ${GIT_CLONE_DIR}
fi




ORIGINALDIR=`pwd`

# Now we remove old checkout

rm -rf ${GIT_DEST}

set +e 
git clone  --reference ${GIT_CLONE_DIR} ${GIT_SRC} ${GIT_DEST}
git_rc=$?
if [ X"$git_rc" != X"0" ] ; then
sleep 120
git clone  --reference ${GIT_CLONE_DIR} ${GIT_SRC} ${GIT_DEST}
git_rc=$?
fi
set -e 

cd ${GIT_DEST}
GIT_TAG_LAST=$(git tag | grep "${GIT_TAG_FILTER}" | tail -n 1)
BUILD_SRC=${GIT_DEST}
export BUILD_SRC

cd ${ORIGINALDIR}

SRC_VERSION=$(echo $GIT_TAG_LAST | sed -e "s/${GIT_TAG_FILTER}//")rc${CHECKOUT_DATE}
export SRC_VERSION

