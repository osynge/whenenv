TOXCMD="tox"

if [ "X${WORKSPACE}" = "X" ] ; then
    WORKSPACE=$HOME
fi

if [ "X${WORKSPACE}" = "X" ] ; then
    echo "BUILD_SRC not defined"
    exit 1
fi

TOXDIR_PREFIX=${WORKSPACE}/tox
TOXDIR="${TOXDIR_PREFIX}/executor_${EXECUTOR_NUMBER}_dir"
export TOXCMD
export TOXDIR
