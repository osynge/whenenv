if [ "X${GIT_PKG_SRC}" = "X" ] ; then
    echo "GIT_SRC not defined"
    exit 1
fi

if [ "X${GIT_PKG_DEST}" = "X" ] ; then
    echo "GIT_DEST not defined"
    exit 1
fi
if [ "X${GIT_PKG_TAG_FILTER}" = "X" ] ; then
    echo "GIT_TAG_FILTER not defined"
    exit 1
fi

if [ "X${GIT_PKG_SRC_CLEANED}" = "X" ] ; then
    echo "GIT_SRC_CLEANED not defined"
    GIT_PKG_SRC_CLEANED=$(echo ${GIT_PKG_SRC} | sed -s 's/[\.:\/]/_/g')
fi



if [ "X${GIT_CLONE_DIR_BASE}" = "X" ] ; then
    
    GIT_CLONE_DIR_BASE="${HOME}/var/gitcache"
    echo "Defaulting GIT_CLONE_DIR : ${GIT_CLONE_DIR_BASE}"
fi


if [ "X${GIT_PKG_CLONE_DIR}" = "X" ] ; then
    GIT_PKG_CLONE_DIR="${GIT_CLONE_DIR_BASE}/${GIT_PKG_SRC_CLEANED}"
    echo "Defaulting GIT_CLONE_DIR : ${GIT_PKG_CLONE_DIR}"
fi


if [ ! -d ${GIT_PKG_CLONE_DIR} ] ; then
git clone --mirror ${GIT_PKG_SRC} ${GIT_PKG_CLONE_DIR}
fi

#git clone --mirror git://git.drupal.org/project/drupal.git ~/gitcaches/drupal.reference


# Now we remove old checkout
rm -rf ${GIT_PKG_DEST}

set +e 
git clone  --reference ${GIT_PKG_CLONE_DIR} ${GIT_PKG_SRC} ${GIT_PKG_DEST}
git_rc=$?
if [ X"$git_rc" != X"0" ] ; then
sleep 120
git clone ${GIT_PKG_SRC} ${GIT_PKG_DEST}
git_rc=$?
fi
set -e

cd ${GIT_PKG_DEST}

GIT_PKG_TAG_LAST=$(git tag | grep "${GIT_PKG_TAG_FILTER}" | sort --version-sort | tail -n 1)




if [ "X${GIT_PKG_TAG_LAST}" = "X" ] ; then
    echo "GIT_PKG_TAG_LAST could not be not defined"
    git tag
    exit 1
fi



export GIT_PKG_TAG_LAST
git checkout ${GIT_PKG_TAG_LAST}
export GIT_PKG_TAG_LAST
PKG_SRC_VERSION=$(echo $GIT_PKG_TAG_LAST | sed -e "s/${GIT_PKG_TAG_FILTER}//")
export SRC_VERSION

PKG_BUILD_SRC=${GIT_PKG_DEST}
export PKG_BUILD_SRC



