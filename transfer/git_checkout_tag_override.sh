if [ "X${GIT_SRC}" = "X" ] ; then
    echo "GITLOCATION not defined"
    exit 1
fi

if [ "X${GIT_DEST}" = "X" ] ; then
    echo "GITLOCATION not defined"
    exit 1
fi
if [ "X${GIT_TAG_FILTER}" = "X" ] ; then
    echo "GIT_TAG_FILTER not defined"
    exit 1
fi


# Now we remove old checkout
rm -rf ${GIT_DEST}
git clone ${GIT_SRC} ${GIT_DEST}
cd ${GIT_DEST}


BUILD_SRC=${GIT_DEST}
export BUILD_SRC



