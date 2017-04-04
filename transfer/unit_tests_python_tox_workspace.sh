if [ "X${WORKSPACE_BASE}" = "X" ] ; then
    echo "WORKSPACE_BASE not defined"
    WORKSPACE_BASE="/tmp/workspace"
fi

if [ "X${TOXDIR_PREFIX}" = "X" ] ; then
    echo "TOXDIR_PREFIX not defined"
    TOXDIR_PREFIX="${WORKSPACE_BASE}/tox"
fi

if [ "X${TOXDIR}" = "X" ] ; then
    echo no TOXDIR set
    TOXDIR="${TOXDIR_PREFIX}/executor_${EXECUTOR_NUMBER}_dir"
fi
export TOXDIR
