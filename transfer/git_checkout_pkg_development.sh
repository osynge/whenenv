echo "GIT_PKG_SRC=${GIT_PKG_SRC}"
echo "GIT_PKG_DEST=${GIT_PKG_DEST}"

if [  "X${GIT_PKG_SRC}" = "X" ] ; then
    echo "GIT_PKG_SRC not defined"
    exit 1
fi


if [  "X${CHECKOUT_DATE}" = "X" ] ; then
    echo "CHECKOUT_DATE not defined"
    exit 1
fi


if [ "X${GIT_PKG_DEST}" = "X" ] ; then
    echo "GIT_PKG_DEST not defined"
    exit 1
fi

if [ "X${GIT_PKG_SRC_CLEANED}" = "X" ] ; then
    echo "GIT_PKG_SRC_CLEANED not defined"
    GIT_PKG_SRC_CLEANED=$(echo ${GIT_PKG_SRC} | sed -s 's/[\.:\/]/_/g')
fi


if [ "X${GIT_PKG_CLONE_DIR_BASE}" = "X" ] ; then
    
    GIT_PKG_CLONE_DIR_BASE="${HOME}/var/gitcache"
    echo "Defaulting GIT_PKG_CLONE_DIR : ${GIT_PKG_CLONE_DIR_BASE}"
fi



if [ "X${GIT_PKG_CLONE_DIR}" = "X" ] ; then
    GIT_PKG_CLONE_DIR="${GIT_PKG_CLONE_DIR_BASE}/${GIT_PKG_SRC_CLEANED}"
    echo "Defaulting GIT_PKG_CLONE_DIR : ${GIT_PKG_CLONE_DIR}"
fi


if [ ! -d ${GIT_PKG_CLONE_DIR} ] ; then
git clone --mirror ${GIT_PKG_SRC} ${GIT_PKG_CLONE_DIR}
fi




ORIGINALDIR=`pwd`

# Now we remove old checkout

rm -rf ${GIT_PKG_DEST}

set +e 
git clone  --reference ${GIT_PKG_CLONE_DIR} ${GIT_PKG_SRC} ${GIT_PKG_DEST}
GIT_PKG_rc=$?
if [ X"$GIT_PKG_rc" != X"0" ] ; then
sleep 120
git clone  --reference ${GIT_PKG_CLONE_DIR} ${GIT_PKG_SRC} ${GIT_PKG_DEST}
GIT_PKG_rc=$?
fi
set -e 

cd ${GIT_PKG_DEST}
GIT_PKG_TAG_LAST=$(git tag | grep "${GIT_PKG_TAG_FILTER}" | tail -n 1)

cd ${ORIGINALDIR}

SRC_VERSION=$(echo $GIT_PKG_TAG_LAST | sed -e "s/${GIT_PKG_TAG_FILTER}//")rc${CHECKOUT_DATE}
export SRC_VERSION

