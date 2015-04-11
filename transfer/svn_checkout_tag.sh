echo "SVN_SRC=${SVN_SRC}"
echo "SVN_DEST=${SVN_DEST}"

if [  "X${SVN_SRC}" = "XX" ] ; then
    echo "SVN_SRC not defined"
    exit 1
fi
if [ "X${SVN_DEST}" = "X" ] ; then
    echo "SVN_DEST not defined"
    exit 1
fi
ORIGINALDIR=`pwd`

SVN_TAGS="${SVN_SRC}/tags"


TAG_LAST=$(svn ls ${SVN_TAGS} | sort --version-sort  | tail -n 1)

svn co ${SVN_SRC}/tags/${TAG_LAST} ${SVN_DEST}

BUILD_SRC=${SVN_DEST}
export BUILD_SRC
export SVN_TRUNK

