if [ "X${GIT_SRC}" == "X" ] ; then
    echo "GITLOCATION not defined"
    exit 1
fi

if [ "X${GIT_DEST}" == "X" ] ; then
    echo "GITLOCATION not defined"
    exit 1
fi
if [ "X${GIT_TAG_FILTER}" == "X" ] ; then
    echo "GIT_TAG_FILTER not defined"
    exit 1
fi


# Now we remove old checkout
rm -rf ${GIT_DEST}
git clone ${GIT_SRC} ${GIT_DEST}
cd ${GIT_DEST}
GIT_TAG_LAST=$(git tag | grep "${GIT_TAG_FILTER}" |  tail -n 1)

if [ "X${GIT_TAG_LAST}" == "X" ] ; then
    echo "GIT_TAG_LAST could not be not defined"
    exit 1
fi



export GIT_TAG_LAST
git checkout ${GIT_TAG_LAST}


BUILD_SRC=${GIT_DEST}
export BUILD_SRC



