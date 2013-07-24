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

SVN_TRUNK="${SVN_SRC}/trunk"

svn co ${SVN_TRUNK} ${SVN_DEST}

BUILD_SRC=${SVN_DEST}
export BUILD_SRC
export SVN_TRUNK

