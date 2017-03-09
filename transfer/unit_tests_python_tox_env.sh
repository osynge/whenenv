TOXCMD="tox"
if [ "X${TOXDIR_PREFIX}" = "X" ] ; then
    echo "TOXDIR_PREFIX not defined"
    TOXDIR_PREFIX=${HOME}/workspace/tox
fi
TOXDIR="${TOXDIR_PREFIX}/executor_${EXECUTOR_NUMBER}_dir"
export TOXCMD
export TOXDIR
